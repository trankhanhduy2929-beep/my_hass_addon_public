from flask import Flask, Response, abort, jsonify, render_template, request, send_from_directory, stream_with_context
import contextlib
import hmac
import ipaddress
import importlib.metadata
import json
import logging
import math
import os
import queue as queue_module
import random
import re
import secrets
import shutil
import socket
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

import requests
import websocket
import yt_dlp
from license_client import LicenseManager
from requests.adapters import HTTPAdapter
from yt_dlp.version import __version__ as YTDLP_VERSION


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("youtube_pro")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

APP_VERSION = "5.4.0"
INTEGRATION_API_VERSION = 2
PORT = 2032
DATA_DIR = os.getenv("YOUTUBE_PRO_DATA_DIR", "/data")
HA_URL = "http://supervisor/core/api"
SUPERVISOR_URL = "http://supervisor"
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN", "")

PLAYLIST_FILE = os.path.join(DATA_DIR, "playlists_v11.json")
QUEUE_FILE = os.path.join(DATA_DIR, "queue_v12013.json")
HISTORY_FILE = os.path.join(DATA_DIR, "recent_history_v12014.json")
SEARCH_HISTORY_FILE = os.path.join(DATA_DIR, "search_history_v320.json")
SLEEP_FILE = os.path.join(DATA_DIR, "sleep_timer_v12013.json")
TIMER_FILE = os.path.join(DATA_DIR, "timers_v11.json")
LEGACY_SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule_rules_v12016.json")
OPTIONS_FILE = os.path.join(DATA_DIR, "options.json")
COOKIE_FILE = os.path.join(DATA_DIR, "cookies.txt")
EXTRACTOR_PREF_FILE = os.path.join(DATA_DIR, "extractor_preference.json")
CAST_PREF_FILE = os.path.join(DATA_DIR, "cast_preferences.json")
PLAYBACK_FILE = os.path.join(DATA_DIR, "playback_sessions_v300.json")
INTEGRATION_TOKEN_FILE = os.path.join(DATA_DIR, "integration_api_token")
LISTENER_PROFILE_FILE = os.path.join(DATA_DIR, "listener_profiles_v520.json")

INGRESS_IPS = {"172.30.32.2", "::ffff:172.30.32.2", "127.0.0.1", "::1"}
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"}
STREAM_SUFFIXES = (".googlevideo.com", ".youtube.com", ".googleusercontent.com")
STREAM_TTL = 12 * 60 * 60
STREAM_LIMIT = 256
SEARCH_TTL = 5 * 60
SEARCH_CACHE_LIMIT = 32
SEARCH_INITIAL_BATCH = 40
RESOLVE_TTL = 60 * 60
RESOLVE_LIMIT = 128
RESOLVE_WAIT_TIMEOUT = 60
SEARCH_MAX_RESULTS = 300
VIDEO_SEARCH_MAX_RESULTS = 200
EXTRACTOR_FAILURE_THRESHOLD = 2
EXTRACTOR_COOLDOWN = 10 * 60
EXTRACTOR_PREF_GENERATION = 2
CAST_PREF_GENERATION = 2
CAST_FAILURE_THRESHOLD = 2
CAST_DIRECT_COOLDOWN = 6 * 60 * 60
CAST_RELAY_COOLDOWN = 30 * 60
RELAY_RESUME_ATTEMPTS = 3
RELAY_STALL_WINDOW = 15.0
RELAY_STALL_SAMPLES = 6
INTERRUPTION_RESUME_DELAY = 3.0
INTERRUPTION_RESUME_MAX = 5
INTERRUPTION_MAX_HOLD = 30 * 60
AUTO_SKIP_MAX_FAILURES = 3
STALL_WATCHDOG_INTERVAL = 20.0
STALL_WATCHDOG_FROZEN = 60.0
SLEEP_FADE_SECONDS = 20
PLAYLIST_IMPORT_MAX = 500
LYRICS_TTL = 24 * 60 * 60
LYRICS_CACHE_LIMIT = 128
PLAYBACK_MAX_TRACKS = 300
MEDIA_BROWSER_MAX_TRACKS = 200
PLAYBACK_END_GRACE = 6
RADIO_DEFAULT_LIMIT = 24
RADIO_MAX_LIMIT = 30
RADIO_REFILL_LIMIT = 12
RADIO_REFILL_THRESHOLD = 5
PERSONAL_MIX_DEFAULT_LIMIT = 24
PERSONAL_MIX_MAX_LIMIT = 30
PERSONAL_MIX_CACHE_TTL = 5 * 60
LISTENER_PROFILE_GENERATION = 1
LISTENER_PROFILE_MAX = 8
LISTENER_PROFILE_TRACK_LIMIT = 500
LISTENER_PROFILE_UNDO_LIMIT = 50
VIDEO_RESOLVE_TTL = 45 * 60
VIDEO_RESOLVE_LIMIT = 64
ENTITY_PROFILE_TTL = 120
TIMER_RETRY_SECONDS = 30
COOKIE_MAX_BYTES = 512 * 1024
COOKIE_HEADERS = {"# HTTP Cookie File", "# Netscape HTTP Cookie File"}
COOKIE_AUTH_NAMES = {
    "SID",
    "APISID",
    "SAPISID",
    "LOGIN_INFO",
    "__Secure-1PSID",
    "__Secure-3PSID",
    "__Secure-1PAPISID",
    "__Secure-3PAPISID",
}

state_lock = threading.RLock()
extractor_save_lock = threading.Lock()
stream_cache = {}
resolve_cache = {}
resolve_inflight = {}
video_resolve_cache = {}
video_resolve_inflight = {}
search_cache = {}
personal_mix_cache = {}
media_base_cache = {"value": None, "expires_at": 0}
entity_profile_cache = {"items": {}, "expires_at": 0}
pot_provider_cache = {"url": None, "available": False, "version": None, "error": None, "expires_at": 0}
extractor_preferences = {"generation": EXTRACTOR_PREF_GENERATION, "preferred": None, "strategies": {}}
cast_preferences = {"generation": CAST_PREF_GENERATION, "entities": {}}
last_error = None
last_extractor = {
    "strategy": None,
    "format_id": None,
    "used_cookies": False,
    "cache_hit": False,
    "elapsed_ms": None,
    "attempts": [],
    "resolved_at": None,
}
active_cast = {
    "entity_id": None,
    "token": None,
    "title": None,
    "started_at": None,
    "transport": None,
    "media_type": None,
    "media_url": None,
    "duration": 0,
    "position": 0,
    "position_updated_at": 0,
    "expected_state": None,
}
active_casts = {}
playback_sessions = {}
playback_locks = {}
playback_advance_pending = set()
playback_interruptions = {}
radio_refill_pending = set()
listener_profiles = {}
active_listener_profile_id = "default"
event_subscribers = set()
lyrics_cache = {}
ha_ws_status = {"connected": False, "last_connected_at": None, "last_event_at": None, "last_error": None}
integration_token_cache = {"value": None}
license_manager = None

relay_session = requests.Session()
relay_adapter = HTTPAdapter(pool_connections=24, pool_maxsize=24, max_retries=0)
relay_session.mount("http://", relay_adapter)
relay_session.mount("https://", relay_adapter)

try:
    EJS_VERSION = importlib.metadata.version("yt-dlp-ejs")
except importlib.metadata.PackageNotFoundError:
    EJS_VERSION = None

try:
    POT_PLUGIN_VERSION = importlib.metadata.version("bgutil-ytdlp-pot-provider")
except importlib.metadata.PackageNotFoundError:
    POT_PLUGIN_VERSION = None


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def save_json(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = f"{path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, separators=(",", ":"))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp_path, path)

def write_private_text(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = f"{path}.{uuid.uuid4().hex}.tmp"
    descriptor = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        os.chmod(path, 0o600)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

def valid_integration_api_token(value):
    token = str(value or "").strip()
    return 48 <= len(token) <= 160 and all(char.isalnum() or char in "-_" for char in token)

def integration_api_token():
    with state_lock:
        cached = integration_token_cache.get("value")
        if valid_integration_api_token(cached):
            return cached
        try:
            with open(INTEGRATION_TOKEN_FILE, "r", encoding="utf-8") as handle:
                stored = handle.read(256).strip()
        except OSError:
            stored = ""
        if not valid_integration_api_token(stored):
            stored = secrets.token_urlsafe(48)
            write_private_text(INTEGRATION_TOKEN_FILE, stored + "\n")
        else:
            try:
                os.chmod(INTEGRATION_TOKEN_FILE, 0o600)
            except OSError:
                pass
        integration_token_cache["value"] = stored
        return stored

def rotate_integration_api_token():
    token = secrets.token_urlsafe(48)
    with state_lock:
        write_private_text(INTEGRATION_TOKEN_FILE, token + "\n")
        integration_token_cache["value"] = token
    return token

def integration_token_status():
    token = integration_api_token()
    try:
        updated_at = datetime.fromtimestamp(os.path.getmtime(INTEGRATION_TOKEN_FILE)).isoformat(timespec="seconds")
    except OSError:
        updated_at = None
    return {"ready": bool(token), "updated_at": updated_at}


def parse_cookie_text(raw):
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("cookies.txt phải dùng mã hóa UTF-8") from error
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    if not lines or lines[0].strip() not in COOKIE_HEADERS:
        raise ValueError("File phải ở định dạng Netscape cookies.txt")

    now = int(time.time())
    kept = ["# Netscape HTTP Cookie File", "# Chỉ chứa cookie YouTube do YouTube Pro lọc tự động."]
    count = 0
    active = 0
    authenticated = False
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped or (stripped.startswith("#") and not stripped.startswith("#HttpOnly_")):
            continue
        fields = line.split("\t")
        if len(fields) != 7:
            continue
        domain = fields[0]
        if domain.startswith("#HttpOnly_"):
            domain = domain[len("#HttpOnly_"):]
        normalized_domain = domain.lstrip(".").lower()
        if normalized_domain != "youtube.com" and not normalized_domain.endswith(".youtube.com"):
            continue
        try:
            expires = int(fields[4] or 0)
        except ValueError:
            continue
        is_active = expires == 0 or expires > now
        count += 1
        active += int(is_active)
        if is_active and fields[5] in COOKIE_AUTH_NAMES and fields[6]:
            authenticated = True
        kept.append(line)

    if not count:
        raise ValueError("Không tìm thấy cookie thuộc youtube.com")
    if not active:
        raise ValueError("Toàn bộ cookie YouTube đã hết hạn")
    return {
        "content": ("\n".join(kept) + "\n").encode("utf-8"),
        "count": count,
        "active": active,
        "authenticated": authenticated,
    }


def cookie_status():
    if not os.path.isfile(COOKIE_FILE):
        return {"installed": False, "valid": False, "count": 0, "active": 0, "authenticated": False}
    try:
        with open(COOKIE_FILE, "rb") as handle:
            parsed = parse_cookie_text(handle.read(COOKIE_MAX_BYTES + 1))
        if os.path.getsize(COOKIE_FILE) > COOKIE_MAX_BYTES:
            raise ValueError("cookies.txt vượt quá 512 KB")
        return {
            "installed": True,
            "valid": True,
            "count": parsed["count"],
            "active": parsed["active"],
            "authenticated": parsed["authenticated"],
            "updated_at": datetime.fromtimestamp(os.path.getmtime(COOKIE_FILE)).isoformat(timespec="seconds"),
        }
    except (OSError, ValueError) as error:
        return {
            "installed": True,
            "valid": False,
            "count": 0,
            "active": 0,
            "authenticated": False,
            "error": str(error),
        }


def clear_youtube_session():
    with state_lock:
        stream_cache.clear()
        resolve_cache.clear()
        video_resolve_cache.clear()
        video_resolve_inflight.clear()
        search_cache.clear()
    shutil.rmtree(os.path.join(DATA_DIR, "yt-dlp-cache"), ignore_errors=True)
    shutil.rmtree(os.path.join("/tmp", "yt-dlp-cache"), ignore_errors=True)


def public_ydl_error(error):
    message = str(error)
    normalized = message.lower().replace("’", "'")
    if "sign in to confirm you're not a bot" in normalized or "confirm you're not a bot" in normalized:
        return "YouTube yêu cầu xác thực đối với client phát này."
    if "cookies" in normalized and any(word in normalized for word in ("expired", "invalid", "fresh", "login")):
        return "Cookie YouTube không còn hợp lệ. Hãy xuất và nhập lại cookies.txt mới."
    return message[:1200]


def safe_list(value, limit):
    return value[-limit:] if isinstance(value, list) else []


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        number = float(value)
        return number if math.isfinite(number) else default
    except (TypeError, ValueError):
        return default


def safe_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().casefold() in {"1", "true", "yes", "on"}


def safe_text(value, limit):
    return str(value or "").replace("\x00", "").strip()[:limit]


def normalize_media_kind(value):
    return "video" if str(value or "").strip().casefold() in {"video", "watch", "movie"} else "audio"


def sanitize_track(value):
    if not isinstance(value, dict):
        return None
    source_url = str(value.get("url") or value.get("source_url") or "").strip()
    if not valid_youtube_url(source_url):
        return None
    return {
        "id": str(value.get("id") or "")[:32],
        "title": str(value.get("title") or "Không rõ tên")[:300],
        "url": source_url,
        "media_kind": normalize_media_kind(value.get("media_kind") or value.get("kind")),
        "thumbnail": safe_https_url(value.get("thumbnail")),
        "duration": max(0, safe_int(value.get("duration"), 0)),
        "channel": safe_text(value.get("channel") or value.get("uploader"), 200),
        "channel_url": safe_https_url(value.get("channel_url") or value.get("uploader_url")),
        "view_count": max(0, safe_int(value.get("view_count"), 0)),
        "like_count": max(0, safe_int(value.get("like_count"), 0)),
        "comment_count": max(0, safe_int(value.get("comment_count"), 0)),
        "upload_date": safe_text(value.get("upload_date"), 16),
        "description": safe_text(value.get("description"), 12000),
        "is_live": bool(value.get("is_live")),
        "played_at": str(value.get("played_at") or "")[:40],
    }


def sanitize_playlists(value):
    if not isinstance(value, dict):
        return {}
    result = {}
    for raw_name, raw_items in list(value.items())[:100]:
        name = normalize_name(raw_name)
        if not name or not isinstance(raw_items, list):
            continue
        tracks = [track for track in (sanitize_track(item) for item in raw_items[:1000]) if track]
        result[name] = tracks
    return result

def sanitize_search_history(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        query = safe_text(item, 160)
        if query and query.casefold() not in {existing.casefold() for existing in result}:
            result.append(query)
        if len(result) >= 12:
            break
    return result

def record_search_query(value):
    global search_history
    query = safe_text(value, 160)
    if not query:
        return
    with state_lock:
        updated = [item for item in search_history if item.casefold() != query.casefold()]
        updated.insert(0, query)
        updated = updated[:12]
        if updated == search_history:
            return
        search_history = updated
        save_json(SEARCH_HISTORY_FILE, search_history)


playlists = {}
queue = []
history = []
search_history = []
sleep_timer = {"enabled": False}
timers = []

MEDIA_BROWSER_DISCOVERY = (
    {"title": "Mix dành cho bạn", "query": "nhạc hay mới nhất"},
    {"title": "Nhạc Việt thịnh hành", "query": "nhạc Việt thịnh hành"},
    {"title": "Chill & lofi", "query": "lofi chill mix"},
    {"title": "Acoustic nhẹ nhàng", "query": "acoustic chill playlist"},
    {"title": "Tập trung làm việc", "query": "deep focus music"},
    {"title": "Năng lượng tập luyện", "query": "workout music mix"},
)

VIDEO_DISCOVERY = (
    {"title": "Thịnh hành", "query": "video thịnh hành Việt Nam"},
    {"title": "Âm nhạc", "query": "music video Việt Nam mới nhất"},
    {"title": "Giải trí", "query": "video giải trí Việt Nam"},
    {"title": "Tin tức", "query": "tin tức mới nhất Việt Nam"},
    {"title": "Công nghệ", "query": "video công nghệ mới nhất"},
    {"title": "Gaming", "query": "gaming Việt Nam thịnh hành"},
)


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def normalize_name(value):
    name = str(value or "").strip()[:80]
    if not name or any(char in name for char in ("/", "\\")) or any(ord(char) < 32 for char in name):
        return None
    return name


def normalize_listener_profile_id(value):
    profile_id = safe_text(value, 32).casefold()
    if profile_id == "default":
        return profile_id
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,31}", profile_id):
        return None
    return profile_id


def listener_channel_key(value):
    if isinstance(value, dict):
        value = value.get("channel_url") or value.get("channel") or value.get("uploader")
    text = safe_text(value, 240).casefold()
    if not text:
        return ""
    if text.startswith(("http://", "https://")):
        try:
            parsed = urlparse(text)
            text = f"{parsed.hostname or ''}{parsed.path}".rstrip("/")
        except Exception:
            pass
    return re.sub(r"\s+", " ", text).strip()


def listener_track_key(track):
    clean = sanitize_track(track)
    return clean.get("url", "") if clean else ""


def new_listener_profile(profile_id="default", name="Mặc định"):
    current = now_iso()
    return {
        "id": profile_id,
        "name": safe_text(name, 60) or "Mặc định",
        "created_at": current,
        "updated_at": current,
        "tracks": {},
        "blocked_tracks": [],
        "blocked_channels": [],
        "undo": [],
    }


def normalize_listener_stat(raw, fallback_url=""):
    if not isinstance(raw, dict):
        return None
    url = str(raw.get("url") or fallback_url or "").strip()
    if not valid_youtube_url(url):
        return None
    return {
        "url": url,
        "title": safe_text(raw.get("title"), 300),
        "channel": safe_text(raw.get("channel"), 200),
        "channel_url": safe_https_url(raw.get("channel_url")),
        "plays": max(0, safe_int(raw.get("plays"), 0)),
        "likes": max(0, min(1, safe_int(raw.get("likes"), 0))),
        "dislikes": max(0, min(1, safe_int(raw.get("dislikes"), 0))),
        "skips": max(0, safe_int(raw.get("skips"), 0)),
        "last_played": safe_text(raw.get("last_played"), 40),
        "last_feedback": safe_text(raw.get("last_feedback"), 24),
        "last_event_at": max(0, safe_float(raw.get("last_event_at"), 0)),
    }


def normalize_listener_profile(raw, profile_id=None):
    if not isinstance(raw, dict):
        return None
    normalized_id = normalize_listener_profile_id(profile_id or raw.get("id"))
    if not normalized_id:
        return None
    name = safe_text(raw.get("name"), 60) or (
        "Mặc định" if normalized_id == "default" else normalized_id
    )
    profile = {
        "id": normalized_id,
        "name": name,
        "created_at": safe_text(raw.get("created_at"), 40) or now_iso(),
        "updated_at": safe_text(raw.get("updated_at"), 40) or now_iso(),
        "tracks": {},
        "blocked_tracks": [],
        "blocked_channels": [],
        "undo": [],
    }
    raw_tracks = raw.get("tracks") if isinstance(raw.get("tracks"), dict) else {}
    for fallback_url, raw_stat in list(raw_tracks.items())[:LISTENER_PROFILE_TRACK_LIMIT]:
        stat = normalize_listener_stat(raw_stat, fallback_url)
        if stat:
            profile["tracks"][stat["url"]] = stat
    for raw_url in raw.get("blocked_tracks") or []:
        url = str(raw_url or "").strip()
        if valid_youtube_url(url) and url not in profile["blocked_tracks"]:
            profile["blocked_tracks"].append(url)
        if len(profile["blocked_tracks"]) >= LISTENER_PROFILE_TRACK_LIMIT:
            break
    for raw_channel in raw.get("blocked_channels") or []:
        channel = listener_channel_key(raw_channel)
        if channel and channel not in profile["blocked_channels"]:
            profile["blocked_channels"].append(channel)
        if len(profile["blocked_channels"]) >= LISTENER_PROFILE_TRACK_LIMIT:
            break
    for raw_entry in (raw.get("undo") or [])[-LISTENER_PROFILE_UNDO_LIMIT:]:
        if not isinstance(raw_entry, dict):
            continue
        action = safe_text(raw_entry.get("action"), 24)
        track_url = str(raw_entry.get("track_url") or "").strip()
        if action not in {"like", "dislike", "block_track", "block_channel"} or not valid_youtube_url(track_url):
            continue
        previous = normalize_listener_stat(raw_entry.get("previous_stat"), track_url)
        before_tracks = [
            item
            for item in (str(value or "").strip() for value in raw_entry.get("blocked_tracks") or [])
            if valid_youtube_url(item)
        ][:LISTENER_PROFILE_TRACK_LIMIT]
        before_channels = [
            item
            for item in (listener_channel_key(value) for value in raw_entry.get("blocked_channels") or [])
            if item
        ][:LISTENER_PROFILE_TRACK_LIMIT]
        profile["undo"].append(
            {
                "action": action,
                "track_url": track_url,
                "previous_stat": previous,
                "blocked_tracks": before_tracks,
                "blocked_channels": before_channels,
            }
        )
    return profile


def normalize_listener_profiles(value):
    envelope = value if isinstance(value, dict) else {}
    raw_profiles = envelope.get("profiles") if isinstance(envelope.get("profiles"), dict) else envelope
    profiles = {}
    for raw_id, raw_profile in list(raw_profiles.items())[:LISTENER_PROFILE_MAX]:
        profile = normalize_listener_profile(raw_profile, raw_id)
        if profile:
            profiles[profile["id"]] = profile
    if "default" not in profiles:
        profiles["default"] = new_listener_profile()
    active = normalize_listener_profile_id(envelope.get("active_profile_id"))
    if active not in profiles:
        active = "default"
    return profiles, active


def listener_profile_public(profile):
    if not isinstance(profile, dict):
        return None
    stats = profile.get("tracks") if isinstance(profile.get("tracks"), dict) else {}
    return {
        "id": profile.get("id"),
        "name": profile.get("name"),
        "created_at": profile.get("created_at"),
        "updated_at": profile.get("updated_at"),
        "plays": sum(max(0, safe_int(item.get("plays"), 0)) for item in stats.values() if isinstance(item, dict)),
        "liked_count": sum(1 for item in stats.values() if isinstance(item, dict) and safe_int(item.get("likes"), 0) > 0),
        "disliked_count": sum(1 for item in stats.values() if isinstance(item, dict) and safe_int(item.get("dislikes"), 0) > 0),
        "skipped_count": sum(max(0, safe_int(item.get("skips"), 0)) for item in stats.values() if isinstance(item, dict)),
        "blocked_track_count": len(profile.get("blocked_tracks") or []),
        "blocked_channel_count": len(profile.get("blocked_channels") or []),
        "liked_urls": [
            item.get("url")
            for item in stats.values()
            if isinstance(item, dict) and safe_int(item.get("likes"), 0) > 0 and item.get("url")
        ][:LISTENER_PROFILE_TRACK_LIMIT],
        "disliked_urls": [
            item.get("url")
            for item in stats.values()
            if isinstance(item, dict) and safe_int(item.get("dislikes"), 0) > 0 and item.get("url")
        ][:LISTENER_PROFILE_TRACK_LIMIT],
        "blocked_tracks": list(profile.get("blocked_tracks") or [])[:LISTENER_PROFILE_TRACK_LIMIT],
        "blocked_channels": list(profile.get("blocked_channels") or [])[:LISTENER_PROFILE_TRACK_LIMIT],
        "can_undo": bool(profile.get("undo")),
    }


def listener_preferences_public():
    with state_lock:
        active = listener_profiles.get(active_listener_profile_id) or listener_profiles.get("default")
        return {
            "success": True,
            "version": LISTENER_PROFILE_GENERATION,
            "active_profile_id": active.get("id") if active else "default",
            "active_profile": listener_profile_public(active),
            "profiles": [
                listener_profile_public(profile)
                for profile in sorted(listener_profiles.values(), key=lambda item: item.get("created_at", ""))
            ],
        }


def persist_listener_profiles():
    with state_lock:
        snapshot = {
            "version": LISTENER_PROFILE_GENERATION,
            "active_profile_id": active_listener_profile_id,
            "profiles": {
                profile_id: profile
                for profile_id, profile in listener_profiles.items()
                if isinstance(profile, dict)
            },
        }
    try:
        save_json(LISTENER_PROFILE_FILE, snapshot)
    except OSError as error:
        logger.warning("Unable to save listener profiles: %s", error)


def invalidate_personal_mix_cache(profile_id=None):
    with state_lock:
        if profile_id:
            for key in list(personal_mix_cache):
                if key[0] == profile_id:
                    personal_mix_cache.pop(key, None)
        else:
            personal_mix_cache.clear()


def listener_profile_snapshot(profile_id=None):
    with state_lock:
        selected = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        profile = listener_profiles.get(selected) or listener_profiles.get("default")
        return json.loads(json.dumps(profile, ensure_ascii=False)) if profile else None


def listener_feedback_state(track, profile_id=None):
    clean = sanitize_track(track)
    if not clean:
        return None
    with state_lock:
        selected_id = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        profile = listener_profiles.get(selected_id) or listener_profiles.get("default")
        if not profile:
            return None
        stats = profile.get("tracks") if isinstance(profile.get("tracks"), dict) else {}
        stat = stats.get(clean["url"], {})
        channel = listener_channel_key(clean)
        return {
            "profile_id": profile.get("id"),
            "liked": safe_int(stat.get("likes"), 0) > 0,
            "disliked": safe_int(stat.get("dislikes"), 0) > 0,
            "blocked_track": clean["url"] in set(profile.get("blocked_tracks") or []),
            "blocked_channel": bool(channel and channel in set(profile.get("blocked_channels") or [])),
            "plays": safe_int(stat.get("plays"), 0),
            "skips": safe_int(stat.get("skips"), 0),
            "last_feedback": safe_text(stat.get("last_feedback"), 24),
        }


def set_active_listener_profile(profile_id):
    global active_listener_profile_id
    normalized_id = normalize_listener_profile_id(profile_id)
    if not normalized_id:
        raise ValueError("Hồ sơ nghe không hợp lệ")
    with state_lock:
        if normalized_id not in listener_profiles:
            raise ValueError("Không tìm thấy hồ sơ nghe")
        active_listener_profile_id = normalized_id
    invalidate_personal_mix_cache()
    persist_listener_profiles()
    return listener_preferences_public()


def create_listener_profile(name):
    profile_name = safe_text(name, 60)
    if not profile_name:
        raise ValueError("Tên hồ sơ không hợp lệ")
    with state_lock:
        if len(listener_profiles) >= LISTENER_PROFILE_MAX:
            raise ValueError(f"Chỉ hỗ trợ tối đa {LISTENER_PROFILE_MAX} hồ sơ")
        if any(profile.get("name", "").casefold() == profile_name.casefold() for profile in listener_profiles.values()):
            raise ValueError("Tên hồ sơ đã tồn tại")
        profile_id = f"profile-{secrets.token_hex(4)}"
        while profile_id in listener_profiles:
            profile_id = f"profile-{secrets.token_hex(4)}"
        listener_profiles[profile_id] = new_listener_profile(profile_id, profile_name)
    persist_listener_profiles()
    return set_active_listener_profile(profile_id)


def delete_listener_profile(profile_id):
    global active_listener_profile_id
    normalized_id = normalize_listener_profile_id(profile_id)
    if not normalized_id or normalized_id == "default":
        raise ValueError("Không thể xóa hồ sơ mặc định")
    with state_lock:
        if normalized_id not in listener_profiles:
            raise ValueError("Không tìm thấy hồ sơ nghe")
        listener_profiles.pop(normalized_id, None)
        if active_listener_profile_id == normalized_id:
            active_listener_profile_id = "default"
    invalidate_personal_mix_cache(normalized_id)
    persist_listener_profiles()
    return listener_preferences_public()


def record_listener_event(track, action="play", profile_id=None):
    clean = sanitize_track(track)
    if not clean:
        return None
    action = safe_text(action, 24).casefold()
    if action not in {"play", "skip", "like", "dislike", "block_track", "block_channel"}:
        raise ValueError("Phản hồi nghe không hợp lệ")
    global active_listener_profile_id
    with state_lock:
        selected_id = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        if selected_id not in listener_profiles:
            selected_id = "default"
        profile = listener_profiles[selected_id]
        key = clean["url"]
        existing = profile["tracks"].get(key)
        previous_stat = json.loads(json.dumps(existing, ensure_ascii=False)) if existing else None
        previous_blocked_tracks = list(profile["blocked_tracks"])
        previous_blocked_channels = list(profile["blocked_channels"])
        stat = existing or {
            "url": clean["url"],
            "title": clean.get("title", ""),
            "channel": clean.get("channel", ""),
            "channel_url": clean.get("channel_url", ""),
            "plays": 0,
            "likes": 0,
            "dislikes": 0,
            "skips": 0,
            "last_played": "",
            "last_feedback": "",
            "last_event_at": 0,
        }
        stat.update(
            {
                "url": clean["url"],
                "title": clean.get("title", "") or stat.get("title", ""),
                "channel": clean.get("channel", "") or stat.get("channel", ""),
                "channel_url": clean.get("channel_url", "") or stat.get("channel_url", ""),
            }
        )
        if action == "play":
            current_time = time.time()
            if current_time - safe_float(stat.get("last_event_at"), 0) < 2:
                return listener_profile_public(profile)
            stat["plays"] = safe_int(stat.get("plays"), 0) + 1
            stat["last_played"] = now_iso()
            stat["last_event_at"] = current_time
        elif action == "skip":
            stat["skips"] = safe_int(stat.get("skips"), 0) + 1
            stat["last_feedback"] = action
        elif action == "like":
            stat["likes"] = 0 if safe_int(stat.get("likes"), 0) else 1
            stat["dislikes"] = 0
            stat["last_feedback"] = "like" if stat["likes"] else "unlike"
        elif action == "dislike":
            stat["dislikes"] = 0 if safe_int(stat.get("dislikes"), 0) else 1
            stat["likes"] = 0
            stat["last_feedback"] = "dislike" if stat["dislikes"] else "undislike"
        elif action == "block_track":
            if key in profile["blocked_tracks"]:
                profile["blocked_tracks"].remove(key)
                stat["last_feedback"] = "unblock_track"
            else:
                profile["blocked_tracks"].append(key)
                profile["blocked_tracks"] = profile["blocked_tracks"][-LISTENER_PROFILE_TRACK_LIMIT:]
                stat["last_feedback"] = action
        elif action == "block_channel":
            channel = listener_channel_key(clean)
            if not channel:
                raise ValueError("Bài hát chưa có thông tin kênh")
            if channel in profile["blocked_channels"]:
                profile["blocked_channels"].remove(channel)
                stat["last_feedback"] = "unblock_channel"
            else:
                profile["blocked_channels"].append(channel)
                profile["blocked_channels"] = profile["blocked_channels"][-LISTENER_PROFILE_TRACK_LIMIT:]
                stat["last_feedback"] = action
        if action != "skip":
            profile["undo"].append(
                {
                    "action": action,
                    "track_url": key,
                    "previous_stat": previous_stat,
                    "blocked_tracks": previous_blocked_tracks,
                    "blocked_channels": previous_blocked_channels,
                }
            )
            profile["undo"] = profile["undo"][-LISTENER_PROFILE_UNDO_LIMIT:]
        profile["tracks"][key] = stat
        if len(profile["tracks"]) > LISTENER_PROFILE_TRACK_LIMIT:
            removable_candidates = [
                value for value in profile["tracks"] if value != key
            ] or [key]
            removable = min(
                removable_candidates,
                key=lambda value: (
                    safe_float(profile["tracks"][value].get("last_event_at"), 0),
                    safe_int(profile["tracks"][value].get("plays"), 0),
                ),
            )
            profile["tracks"].pop(removable, None)
        profile["updated_at"] = now_iso()
    persist_listener_profiles()
    invalidate_personal_mix_cache(selected_id)
    return listener_profile_public(profile)


def undo_listener_feedback(profile_id=None):
    with state_lock:
        selected_id = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        profile = listener_profiles.get(selected_id) or listener_profiles.get("default")
        if not profile or not profile.get("undo"):
            raise ValueError("Không có phản hồi nào để hoàn tác")
        entry = profile["undo"].pop()
        key = entry.get("track_url")
        previous = normalize_listener_stat(entry.get("previous_stat"), key)
        if previous:
            profile["tracks"][key] = previous
        else:
            profile["tracks"].pop(key, None)
        profile["blocked_tracks"] = [
            value for value in entry.get("blocked_tracks", []) if valid_youtube_url(value)
        ][:LISTENER_PROFILE_TRACK_LIMIT]
        profile["blocked_channels"] = [
            value for value in (listener_channel_key(item) for item in entry.get("blocked_channels", [])) if value
        ][:LISTENER_PROFILE_TRACK_LIMIT]
        profile["updated_at"] = now_iso()
    persist_listener_profiles()
    invalidate_personal_mix_cache(selected_id)
    return listener_profile_public(profile)


def normalize_time(value):
    text = str(value or "").strip()
    if ":" not in text:
        return None
    try:
        hour, minute = (int(part) for part in text.split(":", 1))
    except (TypeError, ValueError):
        return None
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        return None
    return f"{hour:02d}:{minute:02d}"


def valid_entity(entity_id):
    return (
        isinstance(entity_id, str)
        and entity_id.startswith("media_player.")
        and all(char.isalnum() or char in "._-" for char in entity_id)
    )


def media_player_profile(entity_id, attributes=None, registry=None, device=None, state=None):
    attributes = attributes if isinstance(attributes, dict) else {}
    registry = registry if isinstance(registry, dict) else {}
    device = device if isinstance(device, dict) else {}
    name_parts = [
        entity_id,
        attributes.get("friendly_name"),
        attributes.get("device_class"),
        attributes.get("platform"),
        attributes.get("integration"),
        attributes.get("model"),
        attributes.get("manufacturer"),
        registry.get("platform"),
        registry.get("original_device_class"),
        device.get("name"),
        device.get("model"),
        device.get("manufacturer"),
        device.get("sw_version"),
    ]
    haystack = " ".join(str(item or "") for item in name_parts).casefold()
    device_class = safe_text(attributes.get("device_class") or registry.get("original_device_class"), 80).casefold()
    registry_platform = safe_text(registry.get("platform"), 80).casefold()
    is_airplay = any(term in haystack for term in ("airplay", "pyatv", "apple airplay"))
    is_homepod = "homepod" in haystack or (
        registry_platform == "apple_tv" and device_class == "speaker"
    )
    is_apple_tv = (registry_platform == "apple_tv" or any(term in haystack for term in ("apple tv", "appletv"))) and not is_homepod
    is_cast = any(term in haystack for term in ("chromecast", "google cast", "google home", "nest audio", "nest hub", "cast"))
    has_display = device_class in {"tv", "receiver"} or any(
        term in haystack for term in ("nest hub", "display", "television", "google tv", "chromecast ultra")
    )
    is_audio_only = is_homepod or (is_airplay and not has_display) or (device_class == "speaker" and not has_display) or (
        any(term in haystack for term in ("sonos", "speaker", "soundbar")) and not has_display and not is_apple_tv
    )
    supported_features = safe_int(attributes.get("supported_features"), 0)
    supports_seek = bool(supported_features & 2) or attributes.get("media_position") is not None
    kind = "homepod" if is_homepod else "apple_tv" if is_apple_tv else "airplay" if is_airplay else "cast" if is_cast else "media_player"
    return {
        "entity_id": entity_id,
        "name": attributes.get("friendly_name") or device.get("name") or entity_id,
        "state": state or "unknown",
        "volume": attributes.get("volume_level"),
        "kind": kind,
        "integration": safe_text(registry.get("platform") or attributes.get("integration"), 80),
        "manufacturer": safe_text(device.get("manufacturer") or attributes.get("manufacturer"), 100),
        "model": safe_text(device.get("model") or attributes.get("model"), 100),
        "can_play_video": is_apple_tv or has_display or (is_cast and not is_audio_only and "chromecast" in haystack),
        "is_airplay": is_homepod or is_airplay,
        "is_cast": is_cast,
        "supports_seek": supports_seek,
    }


def ha_registry_snapshot():
    if not SUPERVISOR_TOKEN:
        return [], []
    connection = None
    try:
        connection = websocket.create_connection(
            "ws://supervisor/core/websocket",
            timeout=5,
            http_proxy_host=None,
        )
        hello = json.loads(connection.recv())
        if hello.get("type") != "auth_required":
            raise RuntimeError("Home Assistant WebSocket không yêu cầu auth")
        connection.send(json.dumps({"type": "auth", "access_token": SUPERVISOR_TOKEN}))
        authenticated = json.loads(connection.recv())
        if authenticated.get("type") != "auth_ok":
            raise RuntimeError("Home Assistant WebSocket auth thất bại")
        results = {}
        commands = (
            (10, "config/entity_registry/list", "entities"),
            (11, "config/device_registry/list", "devices"),
        )
        for command_id, command_type, key in commands:
            connection.send(json.dumps({"id": command_id, "type": command_type}))
            response = json.loads(connection.recv())
            if response.get("type") == "result" and response.get("success") and isinstance(response.get("result"), list):
                results[key] = response["result"]
            else:
                results[key] = []
        return results.get("entities", []), results.get("devices", [])
    except Exception as error:
        logger.info("Unable to read Home Assistant registries: %s", error)
        return [], []
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass


def load_media_player_profiles(rows):
    with state_lock:
        cached_profiles = {
            entity_id: dict(profile)
            for entity_id, profile in (entity_profile_cache.get("items") or {}).items()
        }
        cache_valid = bool(cached_profiles) and entity_profile_cache.get("expires_at", 0) > time.time()
    if cache_valid:
        refreshed = {}
        for row in rows if isinstance(rows, list) else []:
            entity_id = row.get("entity_id") if isinstance(row, dict) else None
            if not valid_entity(entity_id):
                continue
            attributes = row.get("attributes") if isinstance(row.get("attributes"), dict) else {}
            profile = cached_profiles.get(entity_id) or media_player_profile(
                entity_id,
                attributes,
                state=row.get("state"),
            )
            profile.update(
                {
                    "name": attributes.get("friendly_name") or profile.get("name") or entity_id,
                    "state": row.get("state") or "unknown",
                    "volume": attributes.get("volume_level"),
                    "supports_seek": bool(safe_int(attributes.get("supported_features"), 0) & 2)
                    or attributes.get("media_position") is not None,
                }
            )
            refreshed[entity_id] = profile
        with state_lock:
            entity_profile_cache["items"] = refreshed
        return refreshed
    raw_entities, raw_devices = ha_registry_snapshot()
    entity_registry = {
        str(item.get("entity_id")): item
        for item in raw_entities
        if isinstance(item, dict) and item.get("entity_id")
    }
    device_registry = {
        str(item.get("id")): item
        for item in raw_devices
        if isinstance(item, dict) and item.get("id")
    }
    profiles = {}
    for row in rows if isinstance(rows, list) else []:
        entity_id = row.get("entity_id") if isinstance(row, dict) else None
        if not valid_entity(entity_id):
            continue
        attributes = row.get("attributes") if isinstance(row.get("attributes"), dict) else {}
        registry = entity_registry.get(entity_id) or {}
        device = device_registry.get(str(registry.get("device_id") or "")) or {}
        profiles[entity_id] = media_player_profile(
            entity_id,
            attributes,
            registry,
            device,
            row.get("state"),
        )
    with state_lock:
        entity_profile_cache["items"] = profiles
        entity_profile_cache["expires_at"] = time.time() + ENTITY_PROFILE_TTL
    return profiles


def entity_profile(entity_id, refresh=False):
    with state_lock:
        if entity_profile_cache.get("expires_at", 0) > time.time():
            cached = entity_profile_cache.get("items", {}).get(entity_id)
            if cached:
                return dict(cached)
    if not refresh:
        return {}
    try:
        rows = ha_get("/states", timeout=5)
        profiles = load_media_player_profiles(rows)
        return dict(profiles.get(entity_id) or {})
    except Exception:
        return {}


def valid_youtube_url(value):
    try:
        parsed = urlparse(str(value or "").strip())
        host = (parsed.hostname or "").lower().rstrip(".")
    except Exception:
        return False
    return parsed.scheme == "https" and host in YOUTUBE_HOSTS and not parsed.username and not parsed.password


def safe_https_url(value):
    try:
        parsed = urlparse(str(value or "").strip())
        if parsed.scheme == "https" and parsed.hostname:
            return parsed.geturl()[:1200]
    except Exception:
        pass
    return ""


def sanitize_video_details(info, source_url, track):
    info = info if isinstance(info, dict) else {}
    raw_categories = info.get("categories") if isinstance(info.get("categories"), (list, tuple)) else []
    raw_tags = info.get("tags") if isinstance(info.get("tags"), (list, tuple)) else []
    categories = [safe_text(item, 80) for item in raw_categories if safe_text(item, 80)][:12]
    tags = [safe_text(item, 80) for item in raw_tags if safe_text(item, 80)][:16]
    return {
        "id": safe_text(info.get("id") or track.get("id"), 32),
        "title": safe_text(info.get("title") or track.get("title") or "Không rõ tên", 300),
        "url": source_url,
        "thumbnail": safe_https_url(info.get("thumbnail") or track.get("thumbnail")),
        "duration": max(0, safe_int(info.get("duration") or track.get("duration"), 0)),
        "channel": safe_text(info.get("channel") or info.get("uploader") or track.get("channel"), 200),
        "channel_url": safe_https_url(
            info.get("channel_url") or info.get("uploader_url") or track.get("channel_url")
        ),
        "view_count": max(0, safe_int(info.get("view_count") or track.get("view_count"), 0)),
        "like_count": max(0, safe_int(info.get("like_count"), 0)),
        "comment_count": max(0, safe_int(info.get("comment_count"), 0)),
        "upload_date": safe_text(info.get("upload_date") or track.get("upload_date"), 16),
        "description": safe_text(info.get("description"), 12000),
        "live_status": safe_text(info.get("live_status"), 40),
        "is_live": bool(info.get("is_live")),
        "categories": categories,
        "tags": tags,
    }


def valid_stream_url(value):
    try:
        parsed = urlparse(str(value or "").strip())
        host = (parsed.hostname or "").lower().rstrip(".")
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port not in (None, 443):
            return False
        if not any(host == suffix[1:] or host.endswith(suffix) for suffix in STREAM_SUFFIXES):
            return False
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        return bool(addresses) and all(ipaddress.ip_address(item[4][0]).is_global for item in addresses)
    except Exception:
        return False


def ingress_request():
    return request.remote_addr in INGRESS_IPS


def integration_api_request():
    authorization = str(request.headers.get("Authorization") or "").strip()
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.casefold() != "bearer" or not valid_integration_api_token(token):
        return False
    return hmac.compare_digest(token, integration_api_token())


LICENSE_PUBLIC_ENDPOINTS = {"index", "addon_icon", "static", "health", "license_api"}


def license_gate_response():
    if not license_manager or request.endpoint in LICENSE_PUBLIC_ENDPOINTS:
        return None
    if license_manager.permits_use():
        return None
    return (
        jsonify(
            {
                "success": False,
                "code": "license_required",
                "error": "YouTube Pro đang khóa. Hãy nhập License Key hợp lệ để tiếp tục.",
                "license": license_manager.integration_status(),
            }
        ),
        402,
    )


def require_valid_license_for_operation():
    if license_manager and not license_manager.permits_use():
        raise RuntimeError("YouTube Pro đang khóa. Hãy nhập License Key hợp lệ để tiếp tục.")


@app.before_request
def protect_routes():
    if request.endpoint == "health":
        return None
    if request.endpoint == "media_stream":
        return license_gate_response()
    if request.path.startswith("/api/integration/"):
        if not integration_api_request():
            return (
                jsonify({"success": False, "error": "Integration API token không hợp lệ"}),
                401,
                {"WWW-Authenticate": 'Bearer realm="YouTube Pro Integration"'},
            )
        return license_gate_response()
    if not ingress_request():
        abort(403)
    return license_gate_response()


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if request.endpoint == "media_stream":
        response.headers.setdefault("Access-Control-Allow-Origin", "*")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        response.headers.setdefault("Access-Control-Allow-Headers", "Range")
        response.headers.setdefault(
            "Access-Control-Expose-Headers",
            "Accept-Ranges, Content-Length, Content-Range, Content-Type",
        )
        response.headers.setdefault("Timing-Allow-Origin", "*")
    if request.endpoint in {"index", "license_api", "integration_token_api"}:
        response.headers["Cache-Control"] = "no-store, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response


def ha_headers():
    return {"Authorization": f"Bearer {SUPERVISOR_TOKEN}", "Content-Type": "application/json"}


def ha_get(path, timeout=8):
    response = requests.get(f"{HA_URL}{path}", headers=ha_headers(), timeout=timeout)
    response.raise_for_status()
    return response.json()


def supervisor_get(path, timeout=5):
    response = requests.get(f"{SUPERVISOR_URL}{path}", headers=ha_headers(), timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and payload.get("result") == "ok":
        data = payload.get("data")
        return data if isinstance(data, dict) else {}
    return payload if isinstance(payload, dict) else {}


def ha_service(service, payload, timeout=12):
    response = requests.post(
        f"{HA_URL}/services/media_player/{service}",
        headers=ha_headers(),
        json=payload,
        timeout=timeout,
    )
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"Home Assistant HTTP {response.status_code}: {response.text[:200]}")
    return response


def ydl_options(extra=None, use_cookies=False):
    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 15,
        "retries": 1,
        "extractor_retries": 1,
        "cachedir": os.path.join("/tmp", "yt-dlp-cache"),
    }
    if use_cookies and os.path.isfile(COOKIE_FILE):
        options["cookiefile"] = COOKIE_FILE
    if extra:
        options.update(extra)
    return options


def stream_mime(info):
    ext = str(info.get("ext") or "").lower()
    acodec = str(info.get("acodec") or "").lower()
    if ext in {"webm", "opus"} or "opus" in acodec:
        return "audio/webm", "webm"
    if ext == "ogg":
        return "audio/ogg", "ogg"
    return "audio/mp4", "m4a"


def video_stream_mime(info):
    if str(info.get("ext") or "").lower() != "mp4":
        raise RuntimeError("Trình phát video cần progressive MP4 tương thích")
    return "video/mp4", "mp4"


def pick_audio_info(info):
    if info.get("url") and valid_stream_url(info.get("url")):
        return info
    candidates = []
    for item in info.get("formats") or []:
        if item.get("url") and item.get("vcodec") == "none" and item.get("acodec") not in (None, "none"):
            candidates.append(item)
    candidates.sort(
        key=lambda item: (
            item.get("ext") == "m4a",
            str(item.get("acodec") or "").startswith("mp4a"),
            int(item.get("abr") or item.get("tbr") or 0),
        ),
        reverse=True,
    )
    for item in candidates:
        if valid_stream_url(item.get("url")):
            merged = dict(info)
            merged.update(item)
            merged["http_headers"] = item.get("http_headers") or info.get("http_headers") or {}
            return merged
    raise RuntimeError("Không tìm thấy audio stream hợp lệ")

def pick_video_info(info):
    if (
        info.get("url")
        and str(info.get("ext") or "").lower() == "mp4"
        and str(info.get("vcodec") or "none") not in {"", "none"}
        and str(info.get("acodec") or "none") not in {"", "none"}
        and valid_stream_url(info.get("url"))
    ):
        return info
    candidates = []
    for item in info.get("formats") or []:
        if not item.get("url"):
            continue
        if str(item.get("ext") or "").lower() != "mp4":
            continue
        if str(item.get("vcodec") or "none") in {"", "none"}:
            continue
        if str(item.get("acodec") or "none") in {"", "none"}:
            continue
        candidates.append(item)
    candidates.sort(
        key=lambda item: (
            str(item.get("ext") or "").lower() == "mp4",
            str(item.get("vcodec") or "").lower().startswith(("avc", "h264")),
            str(item.get("acodec") or "").lower().startswith(("mp4a", "aac")),
            min(max(0, safe_int(item.get("height"), 0)), 720),
            safe_int(item.get("tbr"), 0),
        ),
        reverse=True,
    )
    for item in candidates:
        if valid_stream_url(item.get("url")):
            merged = dict(info)
            merged.update(item)
            merged["http_headers"] = item.get("http_headers") or info.get("http_headers") or {}
            return merged
    raise RuntimeError("Không tìm thấy video MP4 có audio hợp lệ")


def stream_exact_size(info):
    size = max(0, safe_int(info.get("filesize"), 0))
    if size:
        return size
    try:
        values = parse_qs(urlparse(info.get("url") or "").query).get("clen") or []
        return max(0, safe_int(values[0], 0)) if values else 0
    except Exception:
        return 0


def validate_stream_access(info):
    stream_url = info.get("url")
    if not valid_stream_url(stream_url):
        raise RuntimeError("Stream URL không hợp lệ")
    exact_size = stream_exact_size(info)
    headers = dict(info.get("http_headers") or {})
    for name in ("Host", "Content-Length", "Connection", "Accept-Encoding"):
        headers.pop(name, None)
    headers["Range"] = "bytes=0-"
    response = None
    try:
        response = relay_session.get(
            stream_url,
            headers=headers,
            stream=True,
            timeout=(5, 8),
            allow_redirects=True,
        )
        if response.status_code not in {200, 206}:
            raise RuntimeError(f"HTTP {response.status_code}")
        if not valid_stream_url(response.url):
            raise RuntimeError("redirect không hợp lệ")
        first_chunk = next(response.iter_content(chunk_size=4096), b"")
        if not first_chunk:
            raise RuntimeError("stream không trả dữ liệu")
        total_size = 0
        content_range = str(response.headers.get("Content-Range") or "")
        if "/" in content_range:
            total_size = safe_int(content_range.rsplit("/", 1)[-1], 0)
        return {
            "content_length": max(exact_size, total_size),
            "content_type": safe_text(response.headers.get("Content-Type"), 120),
        }
    except (requests.RequestException, RuntimeError) as error:
        raise RuntimeError(f"Stream bị YouTube từ chối khi kiểm tra Range: {error}") from error
    finally:
        if response is not None:
            response.close()


def copy_resolved(value):
    result = dict(value)
    result["headers"] = dict(value.get("headers") or {})
    result["track"] = dict(value.get("track") or {})
    result["details"] = dict(value.get("details") or {})
    result["details"]["categories"] = list(result["details"].get("categories") or [])
    result["details"]["tags"] = list(result["details"].get("tags") or [])
    return result


def normalize_extractor_preferences(value):
    if not isinstance(value, dict) or safe_int(value.get("generation"), 0) != EXTRACTOR_PREF_GENERATION:
        return {"generation": EXTRACTOR_PREF_GENERATION, "preferred": None, "strategies": {}}
    preferred = safe_text(value.get("preferred"), 80) or None
    strategies = {}
    raw_strategies = value.get("strategies") if isinstance(value.get("strategies"), dict) else {}
    for name, raw in list(raw_strategies.items())[:20]:
        name = safe_text(name, 80)
        if not name or not isinstance(raw, dict):
            continue
        strategies[name] = {
            "successes": max(0, safe_int(raw.get("successes"), 0)),
            "failures": max(0, safe_int(raw.get("failures"), 0)),
            "consecutive_failures": max(0, safe_int(raw.get("consecutive_failures"), 0)),
            "cooldown_until": max(0, safe_int(raw.get("cooldown_until"), 0)),
            "last_elapsed_ms": max(0, safe_int(raw.get("last_elapsed_ms"), 0)),
            "last_success_at": safe_text(raw.get("last_success_at"), 40),
            "last_failure_at": safe_text(raw.get("last_failure_at"), 40),
            "last_error": safe_text(raw.get("last_error"), 300),
        }
    if preferred not in strategies:
        preferred = None
    return {"generation": EXTRACTOR_PREF_GENERATION, "preferred": preferred, "strategies": strategies}


def persist_extractor_preferences():
    try:
        with extractor_save_lock:
            with state_lock:
                snapshot = {
                    "generation": EXTRACTOR_PREF_GENERATION,
                    "preferred": extractor_preferences.get("preferred"),
                    "strategies": {
                        name: dict(stats)
                        for name, stats in (extractor_preferences.get("strategies") or {}).items()
                    },
                }
            save_json(EXTRACTOR_PREF_FILE, snapshot)
    except OSError as error:
        logger.warning("Unable to save extractor preference: %s", error)


def extractor_preference_status():
    now = int(time.time())
    with state_lock:
        return {
            "generation": EXTRACTOR_PREF_GENERATION,
            "preferred": extractor_preferences.get("preferred"),
            "strategies": {
                name: {
                    "successes": stats.get("successes", 0),
                    "failures": stats.get("failures", 0),
                    "consecutive_failures": stats.get("consecutive_failures", 0),
                    "last_elapsed_ms": stats.get("last_elapsed_ms", 0),
                    "cooldown_seconds": max(0, safe_int(stats.get("cooldown_until"), 0) - now),
                }
                for name, stats in (extractor_preferences.get("strategies") or {}).items()
            },
        }

def normalize_cast_preferences(value):
    result = {"generation": CAST_PREF_GENERATION, "entities": {}}
    if not isinstance(value, dict) or safe_int(value.get("generation"), 0) != CAST_PREF_GENERATION:
        return result
    raw_entities = value.get("entities") if isinstance(value, dict) else {}
    if not isinstance(raw_entities, dict):
        return result
    for entity_id, raw in list(raw_entities.items())[:100]:
        if not valid_entity(entity_id) or not isinstance(raw, dict):
            continue
        transports = {}
        raw_transports = raw.get("transports") if isinstance(raw.get("transports"), dict) else {}
        for name in ("direct", "relay"):
            stats = raw_transports.get(name) if isinstance(raw_transports.get(name), dict) else {}
            transports[name] = {
                "successes": max(0, safe_int(stats.get("successes"), 0)),
                "failures": max(0, safe_int(stats.get("failures"), 0)),
                "consecutive_failures": max(0, safe_int(stats.get("consecutive_failures"), 0)),
                "cooldown_until": max(0, safe_int(stats.get("cooldown_until"), 0)),
                "last_elapsed_ms": max(0, safe_int(stats.get("last_elapsed_ms"), 0)),
                "last_success_at": safe_text(stats.get("last_success_at"), 40),
                "last_failure_at": safe_text(stats.get("last_failure_at"), 40),
                "last_error": safe_text(stats.get("last_error"), 300),
            }
        preferred_transport = raw.get("preferred_transport")
        if preferred_transport not in {"direct", "relay"}:
            preferred_transport = None
        preferred_media_type = safe_text(raw.get("preferred_media_type"), 80)
        result["entities"][entity_id] = {
            "preferred_transport": preferred_transport,
            "preferred_media_type": preferred_media_type,
            "updated_at": safe_text(raw.get("updated_at"), 40),
            "transports": transports,
        }
    return result

def persist_cast_preferences():
    try:
        with state_lock:
            snapshot = normalize_cast_preferences(cast_preferences)
        save_json(CAST_PREF_FILE, snapshot)
    except OSError as error:
        logger.warning("Unable to save cast preferences: %s", error)

def cast_preference_status(entity_id=None):
    now = int(time.time())
    with state_lock:
        entities = cast_preferences.get("entities") or {}
        selected = {entity_id: entities.get(entity_id)} if entity_id else entities
        result = {}
        for key, raw in selected.items():
            if not isinstance(raw, dict):
                continue
            item = {
                "preferred_transport": raw.get("preferred_transport"),
                "preferred_media_type": raw.get("preferred_media_type"),
                "updated_at": raw.get("updated_at"),
                "transports": {},
            }
            for name, stats in (raw.get("transports") or {}).items():
                item["transports"][name] = {
                    **dict(stats),
                    "cooldown_seconds": max(0, safe_int(stats.get("cooldown_until"), 0) - now),
                }
                item["transports"][name].pop("cooldown_until", None)
            result[key] = item
        return result.get(entity_id) if entity_id else result

def record_cast_result(entity_id, transport, media_type, success, elapsed_ms=0, error=None):
    if not valid_entity(entity_id) or transport not in {"direct", "relay"}:
        return
    with state_lock:
        entities = cast_preferences.setdefault("entities", {})
        profile = entities.setdefault(
            entity_id,
            {
                "preferred_transport": None,
                "preferred_media_type": "",
                "updated_at": "",
                "transports": {},
            },
        )
        stats = profile.setdefault("transports", {}).setdefault(
            transport,
            {
                "successes": 0,
                "failures": 0,
                "consecutive_failures": 0,
                "cooldown_until": 0,
                "last_elapsed_ms": 0,
                "last_success_at": "",
                "last_failure_at": "",
                "last_error": "",
            },
        )
        stats["last_elapsed_ms"] = max(0, safe_int(elapsed_ms, 0))
        profile["updated_at"] = now_iso()
        if success:
            stats["successes"] = safe_int(stats.get("successes"), 0) + 1
            stats["consecutive_failures"] = 0
            stats["cooldown_until"] = 0
            stats["last_success_at"] = profile["updated_at"]
            stats["last_error"] = ""
            profile["preferred_transport"] = transport
            profile["preferred_media_type"] = safe_text(media_type, 80)
        else:
            failures = safe_int(stats.get("consecutive_failures"), 0) + 1
            stats["failures"] = safe_int(stats.get("failures"), 0) + 1
            stats["consecutive_failures"] = failures
            stats["last_failure_at"] = profile["updated_at"]
            stats["last_error"] = safe_text(error, 300)
            if failures >= CAST_FAILURE_THRESHOLD:
                cooldown = CAST_DIRECT_COOLDOWN if transport == "direct" else CAST_RELAY_COOLDOWN
                stats["cooldown_until"] = int(time.time() + cooldown)
                if profile.get("preferred_transport") == transport:
                    profile["preferred_transport"] = "relay" if transport == "direct" else "direct"
    persist_cast_preferences()

def cast_attempt_plan(entity_id, entry):
    default_media_type = cast_content_type(entry)
    media_types = [default_media_type]
    if default_media_type.startswith("audio/"):
        media_types.append("music")
    now = time.time()
    with state_lock:
        profile = dict((cast_preferences.get("entities") or {}).get(entity_id) or {})
        transport_stats = {
            name: dict(value)
            for name, value in (profile.get("transports") or {}).items()
            if isinstance(value, dict)
        }
    preferred_media_type = str(profile.get("preferred_media_type") or "")
    if preferred_media_type in media_types:
        media_types.remove(preferred_media_type)
        media_types.insert(0, preferred_media_type)
    transports = ["direct", "relay"]
    device_profile = entity_profile(entity_id) or entity_profile(entity_id, refresh=True)
    if device_profile.get("is_airplay") or device_profile.get("kind") == "homepod":
        transports = ["relay", "direct"]
        if "music" in media_types:
            media_types.remove("music")
            media_types.insert(0, "music")
    elif device_profile.get("is_cast"):
        # Google Cast thường tải media bằng full GET không có Range, mà YouTube
        # throttle mạnh các kết nối full GET nên loa bị giật/buffering. Ưu tiên
        # relay để add-on tự ép Range; direct vẫn là phương án dự phòng.
        transports = ["relay", "direct"]
    preferred_transport = profile.get("preferred_transport")
    if preferred_transport in transports:
        transports.remove(preferred_transport)
        transports.insert(0, preferred_transport)
    transports.sort(
        key=lambda name: (
            safe_int(transport_stats.get(name, {}).get("cooldown_until"), 0) > now,
            name != preferred_transport,
        )
    )
    return [(transport, media_type) for transport in transports for media_type in media_types]


def audio_format_string(options=None):
    options = options if isinstance(options, dict) else addon_options()
    prefer_m4a = safe_bool(options.get("audio_prefer_m4a"), True)
    max_kbps = max(0, safe_int(options.get("audio_max_bitrate_kbps"), 0))
    limit = f"[abr<={max_kbps}]" if max_kbps else ""
    if prefer_m4a:
        ordered = [
            f"bestaudio[ext=m4a]{limit}",
            f"bestaudio[acodec^=mp4a]{limit}",
            f"bestaudio{limit}",
        ]
    else:
        ordered = [
            f"bestaudio{limit}",
            f"bestaudio[ext=m4a]{limit}",
        ]
    if max_kbps:
        # Nếu giới hạn bitrate không khớp định dạng nào thì vẫn cho bestaudio để
        # không làm hỏng khả năng phát.
        ordered.append("bestaudio")
    ordered += ["best[height<=360][ext=mp4]", "best[ext=mp4]", "best"]
    return "/".join(ordered)


def available_resolve_strategies():
    audio_format = audio_format_string()
    original_format = "best[height<=360][ext=mp4]/best[ext=mp4]/bestaudio[ext=m4a]/bestaudio/best"
    strategies = [
        {
            "name": "visionos-no-cookie",
            "format": audio_format,
            "extractor_args": {"youtube": {"player_client": ["visionos"], "skip": ["hls", "dash"]}},
            "use_cookies": False,
        },
        {
            "name": "android-mp4-no-cookie",
            "format": original_format,
            "extractor_args": {"youtube": {"player_client": ["android"], "skip": ["hls", "dash"]}},
            "use_cookies": False,
        },
        {
            "name": "android_vr-mp4-no-cookie",
            "format": original_format,
            "extractor_args": {"youtube": {"player_client": ["android_vr"], "skip": ["hls", "dash"]}},
            "use_cookies": False,
        },
    ]
    provider = pot_provider_status()
    if provider.get("enabled") and provider.get("available"):
        strategies.insert(
            0,
            {
                "name": "mweb-po-token",
                "format": audio_format,
                "extractor_args": {
                    "youtube": {"player_client": ["mweb"], "skip": ["hls", "dash"]},
                    "youtubepot-bgutilhttp": {"base_url": [provider["url"]]},
                },
                "use_cookies": False,
            },
        )
    cookie = cookie_status()
    if cookie.get("valid") and cookie.get("authenticated"):
        strategies.append({"name": "authenticated-cookie", "format": audio_format, "use_cookies": True})
    return strategies


def available_video_resolve_strategies():
    max_height = max(144, min(safe_int(addon_options().get("video_max_height"), 720), 2160))
    video_format = (
        f"best[ext=mp4][vcodec!=none][acodec!=none][height<={max_height}]/"
        "best[ext=mp4][vcodec!=none][acodec!=none]"
    )
    return [
        {
            **strategy,
            "name": strategy["name"],
            "format": video_format,
        }
        for strategy in available_resolve_strategies()
    ]


def ordered_resolve_strategies(strategies):
    now = time.time()
    with state_lock:
        preferred = extractor_preferences.get("preferred")
        stats = {
            name: dict(value)
            for name, value in (extractor_preferences.get("strategies") or {}).items()
        }
    active = []
    cooling = []
    for index, strategy in enumerate(strategies):
        strategy_stats = stats.get(strategy["name"], {})
        item = (index, strategy)
        if safe_int(strategy_stats.get("cooldown_until"), 0) > now:
            cooling.append(item)
        else:
            active.append(item)
    active.sort(key=lambda item: (item[1]["name"] != preferred, item[0]))
    cooling.sort(key=lambda item: safe_int(stats.get(item[1]["name"], {}).get("cooldown_until"), 0))
    return [strategy for _, strategy in active + cooling]


def record_strategy_result(name, success, elapsed_ms, error=None):
    timestamp = now_iso()
    with state_lock:
        strategies = extractor_preferences.setdefault("strategies", {})
        stats = strategies.setdefault(
            name,
            {
                "successes": 0,
                "failures": 0,
                "consecutive_failures": 0,
                "cooldown_until": 0,
                "last_elapsed_ms": 0,
                "last_success_at": "",
                "last_failure_at": "",
                "last_error": "",
            },
        )
        stats["last_elapsed_ms"] = max(0, safe_int(elapsed_ms, 0))
        if success:
            should_persist = (
                extractor_preferences.get("preferred") != name
                or stats.get("consecutive_failures", 0) > 0
                or stats.get("cooldown_until", 0) > 0
            )
            stats["successes"] = safe_int(stats.get("successes"), 0) + 1
            stats["consecutive_failures"] = 0
            stats["cooldown_until"] = 0
            stats["last_success_at"] = timestamp
            stats["last_error"] = ""
            extractor_preferences["preferred"] = name
            return should_persist
        previous_failures = safe_int(stats.get("consecutive_failures"), 0)
        stats["failures"] = safe_int(stats.get("failures"), 0) + 1
        stats["consecutive_failures"] = previous_failures + 1
        stats["last_failure_at"] = timestamp
        stats["last_error"] = safe_text(public_ydl_error(error), 300)
        if stats["consecutive_failures"] >= EXTRACTOR_FAILURE_THRESHOLD:
            stats["cooldown_until"] = int(time.time() + EXTRACTOR_COOLDOWN)
        return previous_failures < EXTRACTOR_FAILURE_THRESHOLD <= stats["consecutive_failures"]


def purge_resolve_cache():
    now = time.time()
    expired = [key for key, entry in resolve_cache.items() if entry.get("expires_at", 0) <= now]
    for key in expired:
        resolve_cache.pop(key, None)
    while len(resolve_cache) > RESOLVE_LIMIT:
        oldest = min(resolve_cache, key=lambda key: resolve_cache[key].get("created_at", 0))
        resolve_cache.pop(oldest, None)


def get_cached_resolved(source_url):
    with state_lock:
        entry = resolve_cache.get(source_url)
        if not entry or entry.get("expires_at", 0) <= time.time():
            resolve_cache.pop(source_url, None)
            return None
        resolved = copy_resolved(entry["resolved"])
        resolved["cache_hit"] = True
        resolved["resolve_ms"] = 0
        return resolved


def cache_resolved_result(source_url, resolved):
    with state_lock:
        resolve_cache[source_url] = {
            "resolved": copy_resolved(resolved),
            "created_at": time.time(),
            "expires_at": time.time() + RESOLVE_TTL,
        }
        purge_resolve_cache()


def mark_resolve_cache_hit(cached):
    global last_error
    with state_lock:
        last_extractor.update(
            {
                "strategy": cached.get("strategy") or "resolve-cache",
                "format_id": cached.get("format_id") or "",
                "used_cookies": bool(cached.get("used_cookies")),
                "cache_hit": True,
                "elapsed_ms": 0,
                "attempts": [],
                "resolved_at": now_iso(),
            }
        )
    last_error = None


def ensure_audio_stream_validated(resolved):
    if resolved.get("stream_validated", True):
        return resolved
    checked = copy_resolved(resolved)
    try:
        probe = validate_stream_access(
            {
                "url": checked.get("stream_url"),
                "http_headers": checked.get("headers") or {},
                "filesize": checked.get("content_length") or 0,
            }
        )
    except Exception:
        with state_lock:
            resolve_cache.pop(checked.get("source_url"), None)
        return resolve_track_uncached(checked.get("source_url"), fast=False)
    checked["content_length"] = probe.get("content_length") or checked.get("content_length") or 0
    checked["stream_validated"] = True
    cache_resolved_result(checked.get("source_url"), checked)
    return checked


def resolve_track_uncached(source_url, fast=False):
    global last_error
    total_started = time.monotonic()
    strategies = ordered_resolve_strategies(available_resolve_strategies())
    errors = []
    attempts = []
    preference_dirty = False
    for strategy in strategies:
        attempt_started = time.monotonic()
        extra = {
            "format": strategy["format"],
            "socket_timeout": 10,
            "retries": 0,
            "extractor_retries": 0,
        }
        if strategy.get("extractor_args"):
            extra["extractor_args"] = strategy["extractor_args"]
        try:
            with yt_dlp.YoutubeDL(ydl_options(extra, use_cookies=strategy["use_cookies"])) as ydl:
                info = ydl.extract_info(source_url, download=False)
            selected = pick_audio_info(info or {})
            if fast:
                probe = {
                    "content_length": stream_exact_size(selected),
                    "content_type": "",
                }
            else:
                probe = validate_stream_access(selected)
            content_type, extension = stream_mime(selected)
            metadata = info if isinstance(info, dict) else selected
            track = sanitize_track(
                {
                    "id": selected.get("id") or metadata.get("id"),
                    "title": selected.get("title") or metadata.get("title"),
                    "url": source_url,
                    "thumbnail": selected.get("thumbnail") or metadata.get("thumbnail"),
                    "duration": selected.get("duration") or metadata.get("duration") or 0,
                    "channel": metadata.get("channel") or metadata.get("uploader"),
                    "channel_url": metadata.get("channel_url") or metadata.get("uploader_url"),
                    "view_count": metadata.get("view_count") or 0,
                    "upload_date": metadata.get("upload_date") or "",
                }
            )
            if not track:
                raise RuntimeError("Metadata bài hát không hợp lệ")
            attempt_elapsed = int((time.monotonic() - attempt_started) * 1000)
            total_elapsed = int((time.monotonic() - total_started) * 1000)
            resolved = {
                "source_url": source_url,
                "stream_url": selected["url"],
                "headers": selected.get("http_headers") if isinstance(selected.get("http_headers"), dict) else {},
                "content_type": content_type,
                "extension": extension,
                "content_length": probe.get("content_length") or stream_exact_size(selected),
                "strategy": strategy["name"],
                "format_id": str(selected.get("format_id") or ""),
                "used_cookies": strategy["use_cookies"],
                "stream_validated": not fast,
                "cache_hit": False,
                "resolve_ms": total_elapsed,
                "track": track,
                "details": sanitize_video_details(metadata, source_url, track),
            }
            cache_resolved_result(source_url, resolved)
            attempts.append({"strategy": strategy["name"], "elapsed_ms": attempt_elapsed, "success": True})
            preference_dirty = record_strategy_result(strategy["name"], True, attempt_elapsed) or preference_dirty
            with state_lock:
                last_extractor.update(
                    {
                        "strategy": strategy["name"],
                        "format_id": str(selected.get("format_id") or ""),
                        "used_cookies": strategy["use_cookies"],
                        "cache_hit": False,
                        "elapsed_ms": total_elapsed,
                        "attempts": attempts,
                        "resolved_at": now_iso(),
                    }
                )
            last_error = None
            if preference_dirty:
                persist_extractor_preferences()
            return resolved
        except Exception as error:
            attempt_elapsed = int((time.monotonic() - attempt_started) * 1000)
            errors.append((strategy["name"], error))
            attempts.append(
                {
                    "strategy": strategy["name"],
                    "elapsed_ms": attempt_elapsed,
                    "success": False,
                    "error": safe_text(public_ydl_error(error), 240),
                }
            )
            preference_dirty = record_strategy_result(strategy["name"], False, attempt_elapsed, error) or preference_dirty
            logger.warning("yt-dlp strategy %s failed: %s", strategy["name"], error)

    attempted = ", ".join(name for name, _ in errors)
    bot_blocked = any("confirm you" in str(error).lower().replace("’", "'") and "not a bot" in str(error).lower() for _, error in errors)
    if bot_blocked:
        last_error = "Đã thử các client không cookie nhưng YouTube vẫn chặn phiên/IP này. Hãy thử lại sau, đổi IP hoặc dùng cookie tùy chọn."
    else:
        last_error = public_ydl_error(errors[-1][1]) if errors else "Không thể resolve stream YouTube"
    total_elapsed = int((time.monotonic() - total_started) * 1000)
    with state_lock:
        last_extractor.update(
            {
                "strategy": None,
                "format_id": None,
                "used_cookies": False,
                "cache_hit": False,
                "elapsed_ms": total_elapsed,
                "attempts": attempts,
                "resolved_at": now_iso(),
            }
        )
    if preference_dirty:
        persist_extractor_preferences()
    logger.error("All yt-dlp strategies failed (%s): %s", attempted, last_error)
    raise RuntimeError(last_error)


def resolve_track(source_url, force=False, fast=False):
    require_valid_license_for_operation()
    if not valid_youtube_url(source_url):
        raise ValueError("URL YouTube không hợp lệ")
    if force:
        return resolve_track_uncached(source_url, fast=fast)

    cached = get_cached_resolved(source_url)
    if cached:
        if not fast:
            cached = ensure_audio_stream_validated(cached)
        mark_resolve_cache_hit(cached)
        return cached

    owner = False
    with state_lock:
        entry = resolve_cache.get(source_url)
        if entry and entry.get("expires_at", 0) > time.time():
            cached = copy_resolved(entry["resolved"])
            cached["cache_hit"] = True
            cached["resolve_ms"] = 0
        else:
            cached = None
            job = resolve_inflight.get(source_url)
            if not job:
                job = {"event": threading.Event(), "resolved": None, "error": None}
                resolve_inflight[source_url] = job
                owner = True
    if cached:
        if not fast:
            cached = ensure_audio_stream_validated(cached)
        mark_resolve_cache_hit(cached)
        return cached
    if not owner:
        if not job["event"].wait(RESOLVE_WAIT_TIMEOUT):
            raise RuntimeError("Quá thời gian chờ chuẩn bị bài hát")
        if job.get("error"):
            raise RuntimeError(job["error"])
        if job.get("resolved"):
            resolved = copy_resolved(job["resolved"])
            return resolved if fast else ensure_audio_stream_validated(resolved)
        cached = get_cached_resolved(source_url)
        if cached:
            if not fast:
                cached = ensure_audio_stream_validated(cached)
            mark_resolve_cache_hit(cached)
            return cached
        raise RuntimeError("Không nhận được stream sau khi chờ")

    try:
        resolved = resolve_track_uncached(source_url, fast=fast)
        job["resolved"] = copy_resolved(resolved)
        return resolved
    except Exception as error:
        job["error"] = str(error)
        raise
    finally:
        with state_lock:
            if resolve_inflight.get(source_url) is job:
                resolve_inflight.pop(source_url, None)
            job["event"].set()


def purge_video_resolve_cache():
    now = time.time()
    expired = [key for key, entry in video_resolve_cache.items() if entry.get("expires_at", 0) <= now]
    for key in expired:
        video_resolve_cache.pop(key, None)
    while len(video_resolve_cache) > VIDEO_RESOLVE_LIMIT:
        oldest = min(video_resolve_cache, key=lambda key: video_resolve_cache[key].get("created_at", 0))
        video_resolve_cache.pop(oldest, None)


def get_cached_video(source_url):
    with state_lock:
        entry = video_resolve_cache.get(source_url)
        if not entry or entry.get("expires_at", 0) <= time.time():
            video_resolve_cache.pop(source_url, None)
            return None
        resolved = copy_resolved(entry["resolved"])
        resolved["cache_hit"] = True
        resolved["resolve_ms"] = 0
        return resolved


def cache_video_result(source_url, resolved):
    with state_lock:
        video_resolve_cache[source_url] = {
            "resolved": copy_resolved(resolved),
            "created_at": time.time(),
            "expires_at": time.time() + VIDEO_RESOLVE_TTL,
        }
        purge_video_resolve_cache()


def resolve_video_uncached(source_url):
    global last_error
    total_started = time.monotonic()
    strategies = ordered_resolve_strategies(available_video_resolve_strategies())
    errors = []
    attempts = []
    preference_dirty = False
    for strategy in strategies:
        attempt_started = time.monotonic()
        extra = {
            "format": strategy["format"],
            "socket_timeout": 10,
            "retries": 0,
            "extractor_retries": 0,
        }
        if strategy.get("extractor_args"):
            extra["extractor_args"] = strategy["extractor_args"]
        try:
            with yt_dlp.YoutubeDL(ydl_options(extra, use_cookies=strategy["use_cookies"])) as ydl:
                info = ydl.extract_info(source_url, download=False)
            selected = pick_video_info(info or {})
            probe = validate_stream_access(selected)
            content_type, extension = video_stream_mime(selected)
            if not content_type.startswith("video/"):
                raise RuntimeError("Format đã chọn không chứa hình ảnh")
            metadata = info if isinstance(info, dict) else selected
            track = sanitize_track(
                {
                    "id": selected.get("id") or metadata.get("id"),
                    "title": selected.get("title") or metadata.get("title"),
                    "url": source_url,
                    "media_kind": "video",
                    "thumbnail": selected.get("thumbnail") or metadata.get("thumbnail"),
                    "duration": selected.get("duration") or metadata.get("duration") or 0,
                    "channel": metadata.get("channel") or metadata.get("uploader"),
                    "channel_url": metadata.get("channel_url") or metadata.get("uploader_url"),
                    "view_count": metadata.get("view_count") or 0,
                    "like_count": metadata.get("like_count") or 0,
                    "comment_count": metadata.get("comment_count") or 0,
                    "upload_date": metadata.get("upload_date") or "",
                    "description": metadata.get("description") or "",
                    "is_live": metadata.get("is_live"),
                }
            )
            if not track:
                raise RuntimeError("Metadata video không hợp lệ")
            attempt_elapsed = int((time.monotonic() - attempt_started) * 1000)
            total_elapsed = int((time.monotonic() - total_started) * 1000)
            resolved = {
                "source_url": source_url,
                "stream_url": selected["url"],
                "headers": selected.get("http_headers") if isinstance(selected.get("http_headers"), dict) else {},
                "content_type": content_type,
                "extension": extension,
                "content_length": probe.get("content_length") or stream_exact_size(selected),
                "strategy": strategy["name"],
                "format_id": str(selected.get("format_id") or ""),
                "used_cookies": strategy["use_cookies"],
                "cache_hit": False,
                "resolve_ms": total_elapsed,
                "media_kind": "video",
                "track": track,
                "details": sanitize_video_details(metadata, source_url, track),
            }
            cache_video_result(source_url, resolved)
            attempts.append({"strategy": strategy["name"], "elapsed_ms": attempt_elapsed, "success": True})
            preference_dirty = record_strategy_result(strategy["name"], True, attempt_elapsed) or preference_dirty
            with state_lock:
                last_extractor.update(
                    {
                        "strategy": strategy["name"],
                        "format_id": str(selected.get("format_id") or ""),
                        "used_cookies": strategy["use_cookies"],
                        "cache_hit": False,
                        "elapsed_ms": total_elapsed,
                        "attempts": attempts,
                        "resolved_at": now_iso(),
                    }
                )
            last_error = None
            if preference_dirty:
                persist_extractor_preferences()
            return resolved
        except Exception as error:
            attempt_elapsed = int((time.monotonic() - attempt_started) * 1000)
            errors.append((strategy["name"], error))
            attempts.append(
                {
                    "strategy": strategy["name"],
                    "elapsed_ms": attempt_elapsed,
                    "success": False,
                    "error": safe_text(public_ydl_error(error), 240),
                }
            )
            preference_dirty = record_strategy_result(strategy["name"], False, attempt_elapsed, error) or preference_dirty
            logger.warning("yt-dlp video strategy %s failed: %s", strategy["name"], error)
    if preference_dirty:
        persist_extractor_preferences()
    last_error = public_ydl_error(errors[-1][1]) if errors else "Không thể resolve video YouTube"
    logger.error("All yt-dlp video strategies failed: %s", last_error)
    raise RuntimeError(last_error)


def resolve_video(source_url, force=False):
    require_valid_license_for_operation()
    if not valid_youtube_url(source_url):
        raise ValueError("URL YouTube không hợp lệ")
    if force:
        return resolve_video_uncached(source_url)
    cached = get_cached_video(source_url)
    if cached:
        mark_resolve_cache_hit(cached)
        return cached
    owner = False
    with state_lock:
        job = video_resolve_inflight.get(source_url)
        if not job:
            job = {"event": threading.Event(), "resolved": None, "error": None}
            video_resolve_inflight[source_url] = job
            owner = True
    if not owner:
        if not job["event"].wait(RESOLVE_WAIT_TIMEOUT):
            raise RuntimeError("Quá thời gian chờ chuẩn bị video")
        if job.get("error"):
            raise RuntimeError(job["error"])
        if job.get("resolved"):
            return copy_resolved(job["resolved"])
        cached = get_cached_video(source_url)
        if cached:
            return cached
        raise RuntimeError("Không nhận được video sau khi chờ")
    try:
        resolved = resolve_video_uncached(source_url)
        job["resolved"] = copy_resolved(resolved)
        return resolved
    except Exception as error:
        job["error"] = str(error)
        raise
    finally:
        with state_lock:
            if video_resolve_inflight.get(source_url) is job:
                video_resolve_inflight.pop(source_url, None)
            job["event"].set()


def purge_stream_cache():
    now = time.time()
    expired = [token for token, entry in stream_cache.items() if entry.get("expires_at", 0) <= now]
    for token in expired:
        stream_cache.pop(token, None)
    while len(stream_cache) > STREAM_LIMIT:
        oldest = min(stream_cache, key=lambda token: stream_cache[token].get("created_at", 0))
        stream_cache.pop(oldest, None)


def cache_resolved(resolved, token=None):
    token = token or uuid.uuid4().hex
    entry = dict(resolved)
    entry.update({"created_at": time.time(), "expires_at": time.time() + STREAM_TTL})
    with state_lock:
        stream_cache[token] = entry
        purge_stream_cache()
    return token, entry


def get_stream_entry(token):
    with state_lock:
        entry = stream_cache.get(token)
        if not entry or entry.get("expires_at", 0) <= time.time():
            stream_cache.pop(token, None)
            return None
        return dict(entry)


def refresh_stream_entry(token, entry):
    resolver = resolve_video if cast_content_type(entry).startswith("video/") else resolve_track
    resolved = resolver(entry.get("source_url"), force=True)
    _, refreshed = cache_resolved(resolved, token=token)
    return refreshed


def media_path(token, entry):
    media_kind = "video" if cast_content_type(entry).startswith("video/") else "audio"
    extension = entry.get("extension") or ("mp4" if media_kind == "video" else "m4a")
    return f"/api/media/{token}/{media_kind}.{extension}"


def addon_options():
    value = load_json(OPTIONS_FILE, {})
    return value if isinstance(value, dict) else {}


def valid_base_url(value):
    try:
        parsed = urlparse(str(value or "").strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname)
    except Exception:
        return False

def pot_provider_url():
    options = addon_options()
    if not bool(options.get("pot_provider_enabled", False)) or not POT_PLUGIN_VERSION:
        return None
    value = str(options.get("pot_provider_url") or "http://127.0.0.1:4416").strip().rstrip("/")
    try:
        parsed = urlparse(value)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            return None
        return value
    except Exception:
        return None

def pot_provider_status(force=False):
    url = pot_provider_url()
    if not url:
        return {
            "enabled": bool(addon_options().get("pot_provider_enabled", False)),
            "available": False,
            "url": None,
            "plugin": POT_PLUGIN_VERSION,
            "version": None,
            "error": "Plugin chưa được cài" if not POT_PLUGIN_VERSION else None,
        }
    now = time.time()
    with state_lock:
        if (
            not force
            and pot_provider_cache.get("url") == url
            and pot_provider_cache.get("expires_at", 0) > now
        ):
            return {
                "enabled": True,
                "available": bool(pot_provider_cache.get("available")),
                "url": url,
                "plugin": POT_PLUGIN_VERSION,
                "version": pot_provider_cache.get("version"),
                "error": pot_provider_cache.get("error"),
            }
    available = False
    version = None
    error = None
    try:
        response = requests.get(f"{url}/ping", timeout=(1, 2), proxies={"http": None, "https": None})
        response.raise_for_status()
        payload = response.json()
        available = isinstance(payload, dict) and bool(payload.get("version"))
        version = safe_text(payload.get("version"), 40) if isinstance(payload, dict) else None
        if not available:
            error = "Phản hồi /ping không hợp lệ"
    except Exception as provider_error:
        error = safe_text(provider_error, 220)
    with state_lock:
        pot_provider_cache.update(
            {
                "url": url,
                "available": available,
                "version": version,
                "error": error,
                "expires_at": now + (60 if available else 20),
            }
        )
    return {
        "enabled": True,
        "available": available,
        "url": url,
        "plugin": POT_PLUGIN_VERSION,
        "version": version,
        "error": error,
    }


def supervisor_lan_host():
    try:
        network = supervisor_get("/network/info", timeout=4)
    except Exception as error:
        logger.info("Unable to read Supervisor LAN address: %s", error)
        return None
    candidates = []
    for interface in network.get("interfaces") or []:
        if not isinstance(interface, dict) or not interface.get("connected", True):
            continue
        name = str(interface.get("interface") or "").lower()
        if name == "lo" or name.startswith(("docker", "hassio", "veth", "br-")):
            continue
        ipv4 = interface.get("ipv4") if isinstance(interface.get("ipv4"), dict) else {}
        for raw_address in ipv4.get("address") or []:
            try:
                address = ipaddress.ip_interface(str(raw_address)).ip
            except ValueError:
                continue
            if address.is_loopback or address.is_link_local or address.is_multicast or address.is_unspecified:
                continue
            score = 0
            if interface.get("primary"):
                score += 4
            if interface.get("enabled", True):
                score += 2
            if address.is_private:
                score += 1
            candidates.append((score, str(address)))
    return max(candidates, default=(None, None))[1]


def media_base_url():
    with state_lock:
        if media_base_cache.get("value") and media_base_cache.get("expires_at", 0) > time.time():
            return media_base_cache["value"]
    configured = str(addon_options().get("media_base_url") or "").strip().rstrip("/")
    if valid_base_url(configured):
        value = configured
    else:
        value = None
    if not value:
        lan_host = supervisor_lan_host()
        if lan_host:
            host = f"[{lan_host}]" if ":" in lan_host else lan_host
            value = f"http://{host}:{PORT}"
    if not value:
        try:
            config = ha_get("/config", timeout=5)
            parsed = urlparse(str(config.get("internal_url") or ""))
            if parsed.hostname:
                host = f"[{parsed.hostname}]" if ":" in parsed.hostname else parsed.hostname
                value = f"http://{host}:{PORT}"
        except Exception as error:
            logger.warning("Unable to detect Home Assistant URL: %s", error)
    value = value or f"http://homeassistant.local:{PORT}"
    with state_lock:
        media_base_cache.update({"value": value, "expires_at": time.time() + 60})
    return value


def relay_url(token, entry):
    return f"{media_base_url()}{media_path(token, entry)}"


def cast_content_type(entry):
    value = str(entry.get("content_type") or "audio/mp4").split(";", 1)[0].strip().lower()
    return value if value.startswith(("audio/", "video/")) else "audio/mp4"


def cast_payload(entity_id, media_url, entry, media_type=None):
    track = entry.get("track") or {}
    extra = {
        "title": track.get("title"),
        "thumb": track.get("thumbnail"),
        "stream_type": "BUFFERED",
    }
    duration = max(0, safe_float(track.get("duration"), 0))
    if duration:
        extra["media_info"] = {"duration": duration}
    return {
        "entity_id": entity_id,
        "media_content_id": media_url,
        "media_content_type": media_type or cast_content_type(entry),
        "extra": extra,
    }


def cast_state_matches(entity_id, title, media_url):
    try:
        row = ha_get(f"/states/{entity_id}", timeout=3)
    except Exception:
        return None
    state = str(row.get("state") or "").lower()
    if state not in {"playing", "buffering", "paused"}:
        return False
    attributes = row.get("attributes") or {}
    current_title = str(
        attributes.get("media_title")
        or attributes.get("title")
        or ""
    ).strip()
    current_id = str(attributes.get("media_content_id") or "").strip()
    if current_id == media_url:
        return True
    if current_title and title and current_title.casefold() == str(title).casefold():
        return True
    if current_title or current_id:
        return False
    return True


def set_active_cast(entity_id, token, entry, transport, media_type, media_url):
    value = {
        "entity_id": entity_id,
        "token": token,
        "title": entry.get("track", {}).get("title"),
        "started_at": now_iso(),
        "transport": transport,
        "media_type": media_type,
        "media_url": media_url,
        "duration": max(0, safe_int(entry.get("track", {}).get("duration"), 0)),
        "position": 0,
        "position_updated_at": time.time(),
        "expected_state": "playing",
    }
    with state_lock:
        active_casts[entity_id] = dict(value)
        active_cast.update(value)

def active_cast_for(entity_id):
    with state_lock:
        return dict(active_casts.get(entity_id) or {})

def clear_active_cast(entity_id):
    empty = {
        "entity_id": None,
        "token": None,
        "title": None,
        "started_at": None,
        "transport": None,
        "media_type": None,
        "media_url": None,
        "duration": 0,
        "position": 0,
        "position_updated_at": 0,
        "expected_state": None,
    }
    with state_lock:
        active_casts.pop(entity_id, None)
        if active_cast.get("entity_id") == entity_id:
            active_cast.update(empty)

def update_active_cast_state(entity_id, updates):
    with state_lock:
        current = active_casts.get(entity_id)
        if current:
            current.update(updates)
        if active_cast.get("entity_id") == entity_id:
            active_cast.update(updates)

def start_cast_transport(entity_id, token, entry, transport, attempted=None):
    attempted = set(attempted or ())
    if transport in attempted:
        return None
    direct_url = str(entry.get("stream_url") or "").strip()
    media_url = direct_url if transport == "direct" else relay_url(token, entry)
    if transport == "direct" and not media_url:
        return None
    media_types = []
    for planned_transport, media_type in cast_attempt_plan(entity_id, entry):
        if planned_transport == transport and media_type not in media_types:
            media_types.append(media_type)
    errors = []
    started_at = time.monotonic()
    for media_type in media_types:
        try:
            ha_service("play_media", cast_payload(entity_id, media_url, entry, media_type))
            set_active_cast(entity_id, token, entry, transport, media_type, media_url)
            threading.Thread(
                target=monitor_cast_start,
                args=(entity_id, token, entry, transport, media_type, media_url, attempted | {transport}, started_at),
                daemon=True,
            ).start()
            return media_url
        except Exception as error:
            errors.append(error)
            logger.warning("Cast %s/%s transport failed: %s", transport, media_type, error)
    if errors:
        elapsed_ms = int((time.monotonic() - started_at) * 1000)
        record_cast_result(entity_id, transport, media_types[0] if media_types else "", False, elapsed_ms, errors[-1])
    return None

def cast_progress_snapshot(entity_id):
    try:
        row = ha_get(f"/states/{entity_id}", timeout=3)
    except Exception:
        return None
    attributes = row.get("attributes") or {}
    return {
        "state": str(row.get("state") or "").lower(),
        "position": safe_float(attributes.get("media_position"), -1),
    }


def monitor_cast_stall(entity_id, timeout=RELAY_STALL_WINDOW, samples=RELAY_STALL_SAMPLES):
    first_position = None
    advanced = False
    buffering = 0
    for _ in range(max(1, samples)):
        time.sleep(max(0.5, timeout / max(1, samples)))
        snapshot = cast_progress_snapshot(entity_id)
        if snapshot is None:
            return False
        position = snapshot["position"]
        if position >= 0:
            if first_position is None:
                first_position = position
            elif position > first_position + 0.5:
                advanced = True
        if snapshot["state"] == "buffering":
            buffering += 1
    return not advanced and buffering >= max(1, samples - 1)


def monitor_cast_start(entity_id, token, entry, transport, media_type, media_url, attempted, started_at):
    title = (entry.get("track") or {}).get("title")
    for delay in (0.8, 1.0, 1.2):
        time.sleep(delay)
        active = active_cast_for(entity_id)
        if (
            active.get("entity_id") != entity_id
            or active.get("token") != token
            or active.get("media_url") != media_url
        ):
            return
        started = cast_state_matches(entity_id, title, media_url)
        if started is True:
            if transport == "direct":
                profile = entity_profile(entity_id) or {}
                if profile.get("is_cast") and monitor_cast_stall(entity_id):
                    active = active_cast_for(entity_id)
                    if (
                        active.get("entity_id") != entity_id
                        or active.get("token") != token
                        or active.get("media_url") != media_url
                    ):
                        return
                    record_cast_result(
                        entity_id,
                        transport,
                        media_type,
                        False,
                        int((time.monotonic() - started_at) * 1000),
                        "Loa bị buffering kéo dài",
                    )
                    fallback_url = start_cast_transport(entity_id, token, entry, "relay", attempted | {transport})
                    if fallback_url:
                        logger.warning("Cast direct bị buffering kéo dài; đã chuyển sang relay")
                    return
            record_cast_result(
                entity_id,
                transport,
                media_type,
                True,
                int((time.monotonic() - started_at) * 1000),
            )
            return
        if started is None:
            return
    record_cast_result(
        entity_id,
        transport,
        media_type,
        False,
        int((time.monotonic() - started_at) * 1000),
        "Loa không chuyển sang trạng thái phát",
    )
    fallback = "relay" if transport == "direct" else "direct"
    fallback_url = start_cast_transport(entity_id, token, entry, fallback, attempted)
    if fallback_url:
        logger.warning("Cast %s did not start; switched to %s", transport, fallback)


def cast_entry(entity_id, token, entry):
    if not valid_entity(entity_id):
        raise ValueError("Thiết bị phát không hợp lệ")
    if cast_content_type(entry).startswith("video/"):
        profile = entity_profile(entity_id, refresh=True)
        if profile and not profile.get("can_play_video", False):
            audio_resolved = resolve_track(entry.get("source_url"))
            _, entry = cache_resolved(audio_resolved, token=token)
            logger.info("Video target %s chỉ hỗ trợ audio; đã tự chuyển fallback audio", entity_id)
    attempted = set()
    for transport, _ in cast_attempt_plan(entity_id, entry):
        if transport in attempted:
            continue
        attempted.add(transport)
        selected_url = start_cast_transport(entity_id, token, entry, transport)
        if selected_url:
            return selected_url
    raise RuntimeError("Không thể gửi media tới thiết bị phát")


def playback_lock(entity_id):
    with state_lock:
        return playback_locks.setdefault(entity_id, threading.RLock())

def normalize_repeat_mode(value):
    return value if value in {"off", "all", "one"} else "off"

def normalize_radio_state(value):
    if not isinstance(value, dict) or not value.get("enabled"):
        return None
    seed = sanitize_track(value.get("seed"))
    if not seed:
        return None
    return {
        "enabled": True,
        "seed": seed,
        "query": safe_text(value.get("query"), 160),
        "media_kind": normalize_media_kind(value.get("media_kind") or seed.get("media_kind")),
        "profile_id": normalize_listener_profile_id(value.get("profile_id")) or "default",
        "generated": max(0, safe_int(value.get("generated"), 0)),
        "updated_at": safe_text(value.get("updated_at"), 40),
    }

def normalize_playback_session(value):
    if not isinstance(value, dict):
        return None
    entity_id = value.get("entity_id")
    if not valid_entity(entity_id):
        return None
    tracks = [
        track
        for track in (sanitize_track(item) for item in safe_list(value.get("tracks"), PLAYBACK_MAX_TRACKS))
        if track
    ]
    if not tracks:
        return None
    index = max(0, min(safe_int(value.get("index"), 0), len(tracks) - 1))
    session_state = value.get("state")
    if session_state not in {"idle", "resolving", "starting", "playing", "paused", "stopped", "completed", "error"}:
        session_state = "stopped"
    return {
        "session_id": safe_text(value.get("session_id") or uuid.uuid4().hex, 80),
        "entity_id": entity_id,
        "tracks": tracks,
        "index": index,
        "repeat": normalize_repeat_mode(value.get("repeat")),
        "shuffle": bool(value.get("shuffle")),
        "source": safe_text(value.get("source"), 40),
        "source_name": safe_text(value.get("source_name"), 160),
        "state": session_state,
        "current_token": safe_text(value.get("current_token"), 80),
        "play_id": safe_text(value.get("play_id"), 80),
        "started_at": safe_text(value.get("started_at"), 40),
        "track_started_at": max(0, safe_float(value.get("track_started_at"), 0)),
        "updated_at": safe_text(value.get("updated_at"), 40),
        "last_state": safe_text(value.get("last_state"), 40),
        "last_position": max(0, safe_float(value.get("last_position"), 0)),
        "last_duration": max(0, safe_float(value.get("last_duration"), 0)),
        "last_error": safe_text(value.get("last_error"), 500),
        "stop_requested": bool(value.get("stop_requested")),
        "radio": normalize_radio_state(value.get("radio")),
    }

def persist_playback_sessions():
    try:
        with state_lock:
            snapshot = {
                entity_id: dict(session)
                for entity_id, session in playback_sessions.items()
                if isinstance(session, dict)
            }
        save_json(PLAYBACK_FILE, snapshot)
    except OSError as error:
        logger.warning("Unable to save playback sessions: %s", error)

def playback_session_public(session, include_tracks=False):
    if not isinstance(session, dict):
        return None
    tracks = session.get("tracks") or []
    index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
    result = {
        "session_id": session.get("session_id"),
        "entity_id": session.get("entity_id"),
        "state": session.get("state"),
        "index": index,
        "track_count": len(tracks),
        "upcoming_count": max(0, len(tracks) - index - 1),
        "current_track": dict(tracks[index]) if tracks else None,
        "repeat": session.get("repeat", "off"),
        "shuffle": bool(session.get("shuffle")),
        "source": session.get("source"),
        "source_name": session.get("source_name"),
        "started_at": session.get("started_at"),
        "updated_at": session.get("updated_at"),
        "last_position": session.get("last_position", 0),
        "last_duration": session.get("last_duration", 0),
        "last_error": session.get("last_error"),
    }
    radio = normalize_radio_state(session.get("radio"))
    if radio:
        result["radio"] = {
            "enabled": True,
            "seed": dict(radio["seed"]),
            "query": radio.get("query", ""),
            "media_kind": radio.get("media_kind", "audio"),
            "profile_id": radio.get("profile_id", "default"),
            "generated": radio.get("generated", 0),
            "updated_at": radio.get("updated_at", ""),
        }
    if include_tracks:
        result["tracks"] = [dict(track) for track in tracks]
    return result

def playback_session_for(entity_id):
    with state_lock:
        session = playback_sessions.get(entity_id)
        return dict(session) if isinstance(session, dict) else None

def publish_event(event_type, data):
    message = json.dumps(
        {"type": event_type, "data": data, "at": now_iso()},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    stale = []
    with state_lock:
        subscribers = list(event_subscribers)
    for subscriber in subscribers:
        try:
            subscriber.put_nowait(message)
        except queue_module.Full:
            stale.append(subscriber)
    if stale:
        with state_lock:
            for subscriber in stale:
                event_subscribers.discard(subscriber)

def playback_update_session(entity_id, updates, publish=True, persist=True):
    with state_lock:
        session = playback_sessions.get(entity_id)
        if not session:
            return None
        session.update(updates)
        session["updated_at"] = now_iso()
        public = playback_session_public(session)
    if persist:
        persist_playback_sessions()
    if publish:
        publish_event("playback", public)
    if session.get("radio") and session.get("state") in {"resolving", "starting", "playing", "paused"}:
        maybe_schedule_radio_refill(entity_id)
    return public

def playback_next_index(session, step=1, automatic=False):
    tracks = session.get("tracks") or []
    if not tracks:
        return None
    index = max(0, min(safe_int(session.get("index"), 0), len(tracks) - 1))
    if automatic and session.get("repeat") == "one":
        return index
    target = index + step
    if 0 <= target < len(tracks):
        return target
    if session.get("repeat") == "all":
        return 0 if step > 0 else len(tracks) - 1
    if step < 0:
        return 0
    return None

def normalize_queue_position(value):
    return "next" if str(value or "").strip().casefold() == "next" else "end"

def queue_session_active(session):
    return bool(
        isinstance(session, dict)
        and session.get("tracks")
        and session.get("state") in {"idle", "resolving", "starting", "playing", "paused"}
    )

def session_queue_view(session):
    if not queue_session_active(session):
        return None
    tracks = list(session.get("tracks") or [])
    if not tracks:
        return None
    index = max(0, min(safe_int(session.get("index"), 0), len(tracks) - 1))
    return {
        "scope": "session",
        "entity_id": session.get("entity_id"),
        "current_track": dict(tracks[index]),
        "tracks": [dict(track) for track in tracks[index + 1:]],
        "total": max(0, len(tracks) - index - 1),
        "session": playback_session_public(session),
    }

def queue_view_payload(entity_id=None):
    if entity_id and valid_entity(entity_id):
        session = playback_session_for(entity_id)
        if queue_session_active(session):
            return session_queue_view(session)
    with state_lock:
        tracks = [dict(track) for track in queue]
    return {
        "scope": "global",
        "entity_id": None,
        "current_track": None,
        "tracks": tracks,
        "total": len(tracks),
        "session": None,
    }

def trim_session_tracks(tracks, index, preferred_index=None):
    tracks = list(tracks)
    index = max(0, min(safe_int(index, 0), max(0, len(tracks) - 1)))
    while len(tracks) > PLAYBACK_MAX_TRACKS:
        if index > 0:
            tracks.pop(0)
            index -= 1
            if preferred_index is not None:
                preferred_index -= 1
            continue
        if preferred_index is not None and preferred_index == len(tracks) - 1 and len(tracks) > 1:
            tracks.pop(-2)
        else:
            tracks.pop()
    return tracks, index

def queue_enqueue_track(track, entity_id=None, position="end"):
    clean_track = sanitize_track(track)
    if not clean_track:
        raise ValueError("Bài hát không hợp lệ")
    position = normalize_queue_position(position)
    if entity_id and valid_entity(entity_id):
        with playback_lock(entity_id):
            with state_lock:
                session = playback_sessions.get(entity_id)
                if queue_session_active(session):
                    tracks = list(session.get("tracks") or [])
                    index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
                    insert_at = index + 1 if position == "next" else len(tracks)
                    tracks.insert(insert_at, clean_track)
                    tracks, index = trim_session_tracks(tracks, index, insert_at)
                    session.update({"tracks": tracks, "index": index, "stop_requested": False})
                    public = playback_session_public(session)
                else:
                    session = None
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {
                    "success": True,
                    "scope": "session",
                    "track": clean_track,
                    "session": public,
                    "queue": session_queue_view(session),
                }
    global queue
    with state_lock:
        if position == "next":
            queue.insert(0, clean_track)
            queue = queue[:200]
        else:
            queue.append(clean_track)
            queue = queue[-200:]
        save_json(QUEUE_FILE, queue)
        snapshot = [dict(item) for item in queue]
    return {
        "success": True,
        "scope": "global",
        "track": clean_track,
        "queue": {
            "scope": "global",
            "entity_id": None,
            "current_track": None,
            "tracks": snapshot,
            "total": len(snapshot),
            "session": None,
        },
    }

def queue_remove_item(index, entity_id=None):
    index = safe_int(index, -1)
    if index < 0:
        raise ValueError("Vị trí hàng chờ không hợp lệ")
    if entity_id and valid_entity(entity_id):
        with playback_lock(entity_id):
            with state_lock:
                session = playback_sessions.get(entity_id)
                if queue_session_active(session):
                    tracks = list(session.get("tracks") or [])
                    current_index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
                    actual_index = current_index + 1 + index
                    if actual_index >= len(tracks):
                        raise ValueError("Không tìm thấy bài trong hàng chờ")
                    tracks.pop(actual_index)
                    session["tracks"] = tracks
                    session["index"] = min(current_index, max(0, len(tracks) - 1))
                    public = playback_session_public(session)
                else:
                    session = None
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {"success": True, "scope": "session", "session": public, "queue": session_queue_view(session)}
    global queue
    with state_lock:
        if index >= len(queue):
            raise ValueError("Không tìm thấy bài trong hàng chờ")
        queue.pop(index)
        save_json(QUEUE_FILE, queue)
    return {"success": True, "scope": "global", "queue": queue_view_payload()}

def queue_reorder_items(from_index, to_index, entity_id=None):
    from_index = safe_int(from_index, -1)
    to_index = safe_int(to_index, -1)
    if from_index < 0 or to_index < 0:
        raise ValueError("Vị trí hàng chờ không hợp lệ")
    if entity_id and valid_entity(entity_id):
        with playback_lock(entity_id):
            with state_lock:
                session = playback_sessions.get(entity_id)
                if queue_session_active(session):
                    tracks = list(session.get("tracks") or [])
                    current_index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
                    upcoming = tracks[current_index + 1:]
                    if from_index >= len(upcoming) or to_index >= len(upcoming):
                        raise ValueError("Không tìm thấy bài trong hàng chờ")
                    moved = upcoming.pop(from_index)
                    upcoming.insert(to_index, moved)
                    session["tracks"] = tracks[:current_index + 1] + upcoming
                    session["index"] = current_index
                    public = playback_session_public(session)
                else:
                    session = None
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {"success": True, "scope": "session", "session": public, "queue": session_queue_view(session)}
    global queue
    with state_lock:
        if from_index >= len(queue) or to_index >= len(queue):
            raise ValueError("Không tìm thấy bài trong hàng chờ")
        moved = queue.pop(from_index)
        queue.insert(to_index, moved)
        save_json(QUEUE_FILE, queue)
    return {"success": True, "scope": "global", "queue": queue_view_payload()}

def queue_shuffle(entity_id=None):
    if entity_id and valid_entity(entity_id):
        with playback_lock(entity_id):
            with state_lock:
                session = playback_sessions.get(entity_id)
                if queue_session_active(session):
                    tracks = list(session.get("tracks") or [])
                    current_index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
                    upcoming = tracks[current_index + 1:]
                    random.shuffle(upcoming)
                    session.update({
                        "tracks": tracks[:current_index + 1] + upcoming,
                        "index": current_index,
                        "shuffle": True,
                    })
                    public = playback_session_public(session)
                else:
                    session = None
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {"success": True, "scope": "session", "session": public, "queue": session_queue_view(session)}
    global queue
    with state_lock:
        random.shuffle(queue)
        save_json(QUEUE_FILE, queue)
    return {"success": True, "scope": "global", "queue": queue_view_payload()}

def queue_clear(entity_id=None):
    if entity_id and valid_entity(entity_id):
        with playback_lock(entity_id):
            with state_lock:
                session = playback_sessions.get(entity_id)
                if queue_session_active(session):
                    tracks = list(session.get("tracks") or [])
                    current_index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
                    session.update({
                        "tracks": tracks[:current_index + 1],
                        "index": current_index,
                        "radio": None,
                    })
                    public = playback_session_public(session)
                else:
                    session = None
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {"success": True, "scope": "session", "session": public, "queue": session_queue_view(session)}
    global queue
    with state_lock:
        queue = []
        save_json(QUEUE_FILE, queue)
    return {"success": True, "scope": "global", "queue": queue_view_payload()}

def queue_tracks_for_save(entity_id=None):
    if entity_id and valid_entity(entity_id):
        session = playback_session_for(entity_id)
        if queue_session_active(session):
            tracks = session.get("tracks") or []
            index = max(0, min(safe_int(session.get("index"), 0), max(0, len(tracks) - 1)))
            return [dict(track) for track in tracks[index:]]
    with state_lock:
        return [dict(track) for track in queue]

def save_queue_as_playlist(name, entity_id=None):
    playlist_name = normalize_name(name)
    if not playlist_name:
        raise ValueError("Tên playlist không hợp lệ")
    tracks = queue_tracks_for_save(entity_id)
    unique = []
    seen = set()
    for track in tracks:
        url = track.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(track)
    if not unique:
        raise ValueError("Hàng chờ đang trống")
    with state_lock:
        existing = list(playlists.get(playlist_name) or [])
        existing_urls = {item.get("url") for item in existing}
        added = [track for track in unique if track.get("url") not in existing_urls]
        playlists[playlist_name] = (existing + added)[-1000:]
        save_json(PLAYLIST_FILE, playlists)
        total = len(playlists[playlist_name])
    return {"success": True, "name": playlist_name, "added": len(added), "track_count": total}

def playback_prefetch_next(entity_id, session_id, play_id):
    try:
        session = playback_session_for(entity_id)
        if not session or session.get("session_id") != session_id or session.get("play_id") != play_id:
            return
        next_index = playback_next_index(session, 1, automatic=True)
        if next_index is None or next_index == session.get("index"):
            return
        next_track = session["tracks"][next_index]
        profile = entity_profile(entity_id)
        resolver = resolve_video if next_track.get("media_kind") == "video" and profile.get("can_play_video", True) else resolve_track
        resolver(next_track["url"])
    except Exception as error:
        logger.info("Playback prefetch failed for %s: %s", entity_id, public_ydl_error(error))

def record_history_track(track):
    global history
    clean = sanitize_track(track)
    if not clean:
        return
    clean["played_at"] = now_iso()
    with state_lock:
        history = [item for item in history if item.get("url") != clean["url"]]
        history.append(clean)
        history = history[-50:]
        save_json(HISTORY_FILE, history)
    try:
        record_listener_event(clean, "play")
    except ValueError:
        pass

def playback_play_current(entity_id):
    with playback_lock(entity_id):
        session = playback_session_for(entity_id)
        if not session:
            raise ValueError("Không tìm thấy phiên phát")
        tracks = session.get("tracks") or []
        index = max(0, min(safe_int(session.get("index"), 0), len(tracks) - 1))
        track = tracks[index]
        session_id = session.get("session_id")
        play_id = uuid.uuid4().hex
        playback_update_session(
            entity_id,
            {"state": "resolving", "play_id": play_id, "stop_requested": False, "last_error": ""},
        )
        try:
            profile = entity_profile(entity_id, refresh=True)
            resolver = resolve_video if track.get("media_kind") == "video" and profile.get("can_play_video", True) else resolve_track
            resolved = resolver(track["url"])
            current = playback_session_for(entity_id)
            if not current or current.get("session_id") != session_id or current.get("play_id") != play_id:
                raise RuntimeError("Phiên phát đã được thay thế")
            token, entry = cache_resolved(resolved)
            cast_entry(entity_id, token, entry)
            effective_entry = get_stream_entry(token) or entry
            resolved_track = sanitize_track(effective_entry.get("track")) or track
            with state_lock:
                stored = playback_sessions.get(entity_id)
                if stored and stored.get("session_id") == session_id and stored.get("play_id") == play_id:
                    stored["tracks"][index] = resolved_track
            public = playback_update_session(
                entity_id,
                {
                    "state": "starting",
                    "current_token": token,
                    "started_at": current.get("started_at") or now_iso(),
                    "track_started_at": time.time(),
                    "last_state": "starting",
                    "last_position": 0,
                    "last_duration": max(0, safe_float(effective_entry.get("track", {}).get("duration"), 0)),
                    "last_error": "",
                    "resume_count": 0,
                    "play_failures": 0,
                },
            )
            record_history_track(resolved_track)
            maybe_schedule_radio_refill(entity_id)
            threading.Thread(
                target=playback_prefetch_next,
                args=(entity_id, session_id, play_id),
                daemon=True,
            ).start()
            return public
        except Exception as error:
            current = playback_session_for(entity_id)
            if current and current.get("session_id") == session_id and current.get("play_id") == play_id:
                failures = safe_int(current.get("play_failures"), 0) + 1
                playback_update_session(
                    entity_id,
                    {"state": "error", "last_error": public_ydl_error(error), "play_failures": failures},
                )
                if (
                    auto_skip_enabled()
                    and failures <= AUTO_SKIP_MAX_FAILURES
                    and len(tracks) > 1
                    and entity_id not in playback_advance_pending
                ):
                    threading.Thread(
                        target=auto_skip_failed_track,
                        args=(entity_id, session_id, play_id),
                        daemon=True,
                    ).start()
            raise


def auto_skip_failed_track(entity_id, session_id, play_id):
    time.sleep(2)
    session = playback_session_for(entity_id)
    if not session:
        return
    if session.get("session_id") != session_id:
        return
    if session.get("stop_requested") or session.get("state") in {"stopped", "completed"}:
        return
    logger.warning("Tự động bỏ qua bài lỗi trên %s (lần %s)", entity_id, session.get("play_failures"))
    try:
        advance_playback_session(
            entity_id,
            1,
            automatic=True,
            expected_session_id=session_id,
            expected_play_id=session.get("play_id"),
        )
    except Exception as error:
        logger.error("Auto-skip thất bại cho %s: %s", entity_id, error)

def start_playback_session(entity_id, tracks, index=0, repeat="off", shuffle=False, source="", source_name=""):
    if not valid_entity(entity_id):
        raise ValueError("Thiết bị phát không hợp lệ")
    clean_tracks = [
        track
        for track in (sanitize_track(item) for item in safe_list(tracks, PLAYBACK_MAX_TRACKS))
        if track
    ]
    if not clean_tracks:
        raise ValueError("Danh sách phát trống")
    selected_index = max(0, min(safe_int(index, 0), len(clean_tracks) - 1))
    if shuffle:
        selected = clean_tracks[selected_index]
        remaining = [track for position, track in enumerate(clean_tracks) if position != selected_index]
        random.shuffle(remaining)
        clean_tracks = [selected, *remaining]
        selected_index = 0
    session = normalize_playback_session(
        {
            "session_id": uuid.uuid4().hex,
            "entity_id": entity_id,
            "tracks": clean_tracks,
            "index": selected_index,
            "repeat": repeat,
            "shuffle": shuffle,
            "source": source,
            "source_name": source_name,
            "state": "idle",
            "started_at": now_iso(),
        }
    )
    with playback_lock(entity_id):
        clear_playback_interruption(entity_id)
        with state_lock:
            playback_sessions[entity_id] = session
        persist_playback_sessions()
        publish_event("playback", playback_session_public(session))
        return playback_play_current(entity_id)

def adopt_playback_session(entity_id, tracks, index, repeat, shuffle, token, entry, source="", source_name=""):
    if not valid_entity(entity_id):
        raise ValueError("Thiết bị phát không hợp lệ")
    clean_tracks = [
        track
        for track in (sanitize_track(item) for item in safe_list(tracks, PLAYBACK_MAX_TRACKS))
        if track
    ]
    current_track = sanitize_track((entry or {}).get("track"))
    if not clean_tracks and current_track:
        clean_tracks = [current_track]
    if not clean_tracks:
        raise ValueError("Danh sách phát trống")
    selected_index = max(0, min(safe_int(index, 0), len(clean_tracks) - 1))
    if current_track:
        matching = next(
            (position for position, track in enumerate(clean_tracks) if track.get("url") == current_track.get("url")),
            None,
        )
        if matching is not None:
            selected_index = matching
    if shuffle:
        selected = clean_tracks[selected_index]
        remaining = [track for position, track in enumerate(clean_tracks) if position != selected_index]
        random.shuffle(remaining)
        clean_tracks = [selected, *remaining]
        selected_index = 0
    session = normalize_playback_session(
        {
            "session_id": uuid.uuid4().hex,
            "entity_id": entity_id,
            "tracks": clean_tracks,
            "index": selected_index,
            "repeat": repeat,
            "shuffle": shuffle,
            "source": source,
            "source_name": source_name,
            "state": "starting",
            "current_token": token,
            "play_id": uuid.uuid4().hex,
            "started_at": now_iso(),
            "track_started_at": time.time(),
            "last_state": "starting",
            "last_duration": max(0, safe_float((entry or {}).get("track", {}).get("duration"), 0)),
        }
    )
    with playback_lock(entity_id):
        clear_playback_interruption(entity_id)
        with state_lock:
            playback_sessions[entity_id] = session
        persist_playback_sessions()
        public = playback_session_public(session)
        publish_event("playback", public)
        record_history_track(current_track or clean_tracks[selected_index])
        return public

def advance_playback_session(
    entity_id,
    step=1,
    automatic=False,
    expected_session_id=None,
    expected_play_id=None,
):
    with playback_lock(entity_id):
        clear_playback_interruption(entity_id)
        session = playback_session_for(entity_id)
        if not session:
            raise ValueError("Không tìm thấy phiên phát")
        if expected_session_id and session.get("session_id") != expected_session_id:
            return playback_session_public(session)
        if expected_play_id and session.get("play_id") != expected_play_id:
            return playback_session_public(session)
        target = playback_next_index(session, step, automatic)
        if target is None:
            clear_active_cast(entity_id)
            return playback_update_session(
                entity_id,
                {"state": "completed", "last_state": "idle", "stop_requested": False},
            )
        if not automatic:
            tracks = session.get("tracks") or []
            current_index = max(0, min(safe_int(session.get("index"), 0), len(tracks) - 1))
            if tracks and target != current_index:
                try:
                    record_listener_event(tracks[current_index], "skip")
                except ValueError:
                    pass
        playback_update_session(
            entity_id,
            {"index": target, "state": "idle", "last_position": 0, "last_error": "", "stop_requested": False},
        )
        return playback_play_current(entity_id)

def request_playback_advance(entity_id):
    session = playback_session_for(entity_id)
    if not session:
        return
    expected_session_id = session.get("session_id")
    expected_play_id = session.get("play_id")
    with state_lock:
        if entity_id in playback_advance_pending:
            return
        playback_advance_pending.add(entity_id)

    def run():
        try:
            advance_playback_session(
                entity_id,
                1,
                automatic=True,
                expected_session_id=expected_session_id,
                expected_play_id=expected_play_id,
            )
        except Exception as error:
            logger.error("Auto-next failed for %s: %s", entity_id, error)
        finally:
            with state_lock:
                playback_advance_pending.discard(entity_id)

    threading.Thread(target=run, daemon=True).start()

def stop_playback_session(entity_id, stop_player=True, remove=False):
    with playback_lock(entity_id):
        clear_playback_interruption(entity_id)
        session = playback_session_for(entity_id)
        previous_state = session.get("state") if session else None
        public = None
        if session:
            public = playback_update_session(
                entity_id,
                {"state": "stopped", "stop_requested": True, "last_error": ""},
            )
        try:
            if stop_player and valid_entity(entity_id):
                ha_service("media_stop", {"entity_id": entity_id})
        except Exception as error:
            if session:
                playback_update_session(
                    entity_id,
                    {
                        "state": previous_state or "error",
                        "stop_requested": False,
                        "last_error": safe_text(error, 500),
                    },
                )
            raise
        clear_active_cast(entity_id)
        if remove:
            with state_lock:
                playback_sessions.pop(entity_id, None)
            persist_playback_sessions()
            publish_event("playback", {"entity_id": entity_id, "state": "removed"})
            return None
        return public

def update_playback_mode(entity_id, repeat=None, shuffle=None):
    with playback_lock(entity_id):
        session = playback_session_for(entity_id)
        if not session:
            raise ValueError("Không tìm thấy phiên phát")
        updates = {}
        if repeat is not None:
            updates["repeat"] = normalize_repeat_mode(repeat)
        if shuffle is not None and bool(shuffle) != bool(session.get("shuffle")):
            tracks = list(session.get("tracks") or [])
            index = safe_int(session.get("index"), 0)
            current = tracks[index]
            remaining = [track for position, track in enumerate(tracks) if position != index]
            if shuffle:
                random.shuffle(remaining)
            updates.update({"tracks": [current, *remaining], "index": 0, "shuffle": bool(shuffle)})
        return playback_update_session(entity_id, updates)

def interruption_resume_enabled():
    return safe_bool(addon_options().get("resume_after_interruption"), True)


def auto_skip_enabled():
    return safe_bool(addon_options().get("auto_skip_failed"), True)


def mark_playback_interrupted(entity_id, position=0, duration=0, volume=None):
    if not valid_entity(entity_id):
        return
    with state_lock:
        if entity_id in playback_interruptions:
            return
        info = {
            "position": max(0, safe_float(position, 0)),
            "duration": max(0, safe_float(duration, 0)),
            "at": time.time(),
        }
        if volume is not None:
            info["volume"] = max(0.0, min(1.0, safe_float(volume, 0)))
        playback_interruptions[entity_id] = info
    # Đóng băng vị trí ước lượng để automation khác không làm trôi vị trí.
    update_active_cast_state(entity_id, {"expected_state": None})


def clear_playback_interruption(entity_id):
    with state_lock:
        playback_interruptions.pop(entity_id, None)


def playback_handle_state(entity_id, row):
    if not valid_entity(entity_id) or not isinstance(row, dict):
        return
    attributes = row.get("attributes") or {}
    player_state = str(row.get("state") or "unknown").lower()
    has_position = attributes.get("media_position") is not None
    position = max(0, safe_float(attributes.get("media_position"), 0))
    duration = max(0, safe_float(attributes.get("media_duration"), 0))
    current_media_id = str(attributes.get("media_content_id") or "").strip()
    active = active_cast_for(entity_id)
    our_media_url = str(active.get("media_url") or "").strip() if active else ""
    media_mismatch = bool(our_media_url and current_media_id and current_media_id != our_media_url)
    if active:
        duration = duration or max(0, safe_float(active.get("duration"), 0))
        if not has_position and player_state in {"playing", "buffering", "paused", "idle"}:
            position = active_cast_position_locked(active)
        update_active_cast_state(
            entity_id,
            {
                "position": position,
                "position_updated_at": time.time(),
                "duration": duration,
                "expected_state": player_state if player_state in {"playing", "paused", "buffering"} else None,
            },
        )
    session = playback_session_for(entity_id)
    if not session:
        publish_event("player_state", {"entity_id": entity_id, "state": player_state})
        return
    previous_state = session.get("last_state")
    effective_duration = duration or max(0, safe_float(session.get("last_duration"), 0))
    effective_position = (
        position
        if has_position or active
        else max(0, safe_float(session.get("last_position"), 0))
    )
    session_state = session.get("state")
    stop_requested = bool(session.get("stop_requested"))
    if media_mismatch and player_state in {"playing", "buffering", "paused"} and not stop_requested:
        # TTS/automation khác đang chiếm loa: giữ phiên để phát tiếp sau khi xong.
        mark_playback_interrupted(entity_id, effective_position, effective_duration, attributes.get("volume_level"))
        publish_event(
            "player_state",
            {
                "entity_id": entity_id,
                "state": "interrupted",
                "position": effective_position,
                "duration": effective_duration,
            },
        )
        return
    interrupted = entity_id in playback_interruptions
    updates = {
        "last_state": player_state,
        "last_position": effective_position,
        "last_duration": effective_duration,
    }
    if player_state in {"playing", "buffering"}:
        updates["state"] = "playing" if player_state == "playing" else "starting"
        updates["stop_requested"] = False
    elif player_state == "paused":
        updates["state"] = "paused"
    playback_update_session(entity_id, updates, persist=False)
    publish_event(
        "player_state",
        {
            "entity_id": entity_id,
            "state": player_state,
            "position": effective_position,
            "duration": effective_duration,
        },
    )
    if player_state not in {"idle", "off"} or stop_requested:
        return
    track_started_at = max(0, safe_float(session.get("track_started_at"), 0))
    if track_started_at and time.time() - track_started_at < 5 and not interrupted:
        return
    near_end = effective_duration > 0 and effective_position >= max(1, effective_duration - PLAYBACK_END_GRACE)
    if previous_state in {"playing", "buffering"} and near_end and session_state not in {"stopped", "completed"}:
        clear_playback_interruption(entity_id)
        request_playback_advance(entity_id)
    elif previous_state in {"playing", "buffering", "paused"}:
        if interrupted:
            # Automation khác vừa kết thúc; worker sẽ phát tiếp khi loa rảnh.
            return
        if interruption_resume_enabled() and session_state not in {"stopped", "completed"}:
            mark_playback_interrupted(entity_id, effective_position, effective_duration, attributes.get("volume_level"))
            return
        playback_update_session(entity_id, {"state": "stopped", "stop_requested": True})

def resume_interrupted_playback(entity_id):
    with state_lock:
        info = playback_interruptions.get(entity_id)
    if not info:
        return
    clear_playback_interruption(entity_id)
    if not interruption_resume_enabled():
        return
    with playback_lock(entity_id):
        session = playback_session_for(entity_id)
        if not session:
            return
        if session.get("stop_requested") or session.get("state") in {"stopped", "completed"}:
            return
        if entity_id in playback_advance_pending:
            return
        attempts = safe_int(session.get("resume_count"), 0) + 1
        if attempts > INTERRUPTION_RESUME_MAX:
            playback_update_session(
                entity_id,
                {
                    "state": "stopped",
                    "stop_requested": True,
                    "last_error": "Đã thử phát tiếp quá nhiều lần",
                },
            )
            return
        position = max(0.0, safe_float(info.get("position"), 0))
        token = str(session.get("current_token") or "").strip()
        entry = get_stream_entry(token) if token else None
        if not entry:
            playback_update_session(entity_id, {"resume_count": attempts})
            try:
                playback_play_current(entity_id)
            except Exception as error:
                logger.warning("Resume re-resolve failed for %s: %s", entity_id, error)
            return
        playback_update_session(
            entity_id,
            {
                "resume_count": attempts,
                "state": "starting",
                "stop_requested": False,
                "last_state": "starting",
                "track_started_at": time.time(),
                "last_error": "",
            },
        )
        try:
            cast_entry(entity_id, token, entry)
        except Exception as error:
            logger.warning("Resume cast failed for %s: %s", entity_id, error)
            try:
                playback_play_current(entity_id)
            except Exception as inner:
                logger.error("Resume fallback failed for %s: %s", entity_id, inner)
            return
        playback_update_session(
            entity_id,
            {"state": "playing", "last_state": "playing", "last_position": position},
        )
        if position > 1:
            try:
                ha_service("media_seek", {"entity_id": entity_id, "seek_position": position})
            except Exception as error:
                logger.info("Không seek lại được cho %s: %s", entity_id, error)
        saved_volume = info.get("volume")
        if saved_volume is not None:
            try:
                ha_service("volume_set", {"entity_id": entity_id, "volume_level": saved_volume})
            except Exception as error:
                logger.info("Không khôi phục được âm lượng cho %s: %s", entity_id, error)


def interruption_worker():
    while True:
        try:
            with state_lock:
                entities = list(playback_interruptions)
            for entity_id in entities:
                info = playback_interruptions.get(entity_id)
                if not info:
                    continue
                age = time.time() - safe_float(info.get("at"), time.time())
                if age > INTERRUPTION_MAX_HOLD:
                    clear_playback_interruption(entity_id)
                    continue
                if age < INTERRUPTION_RESUME_DELAY:
                    continue
                try:
                    row = ha_get(f"/states/{entity_id}", timeout=4)
                except Exception:
                    continue
                state = str(row.get("state") or "").lower()
                attrs = row.get("attributes") or {}
                media_id = str(attrs.get("media_content_id") or "").strip()
                active = active_cast_for(entity_id)
                our_url = str(active.get("media_url") or "").strip()
                if state in {"playing", "buffering", "paused"}:
                    if media_id and our_url and media_id != our_url:
                        continue
                    clear_playback_interruption(entity_id)
                    continue
                if state == "idle":
                    resume_interrupted_playback(entity_id)
                    continue
                if state in {"off", "unavailable"}:
                    clear_playback_interruption(entity_id)
                    playback_update_session(entity_id, {"state": "stopped", "stop_requested": True})
        except Exception as error:
            logger.error("Interruption worker failed: %s", error)
        time.sleep(2)


def playback_watchdog_worker():
    last_positions = {}
    while True:
        try:
            with state_lock:
                entities = list(playback_sessions)
            for entity_id in entities:
                session = playback_session_for(entity_id)
                if not session:
                    last_positions.pop(entity_id, None)
                    continue
                if session.get("state") not in {"playing", "starting"}:
                    last_positions.pop(entity_id, None)
                    continue
                if entity_id in playback_interruptions or session.get("stop_requested"):
                    continue
                snapshot = cast_progress_snapshot(entity_id)
                if not snapshot or snapshot.get("state") != "playing" or snapshot.get("position", -1) < 0:
                    last_positions.pop(entity_id, None)
                    continue
                position = snapshot["position"]
                now = time.time()
                previous = last_positions.get(entity_id)
                if not previous or abs(position - previous["position"]) >= 0.5:
                    last_positions[entity_id] = {"position": position, "at": now}
                    continue
                if now - previous["at"] >= STALL_WATCHDOG_FROZEN:
                    logger.warning("Playback đứng ở %s (vị trí %.1fs); thử phát tiếp", entity_id, position)
                    last_positions.pop(entity_id, None)
                    mark_playback_interrupted(entity_id, position, session.get("last_duration", 0))
                    threading.Thread(
                        target=resume_interrupted_playback,
                        args=(entity_id,),
                        daemon=True,
                    ).start()
        except Exception as error:
            logger.error("Playback watchdog failed: %s", error)
        time.sleep(STALL_WATCHDOG_INTERVAL)

def ha_websocket_worker():
    if not SUPERVISOR_TOKEN:
        return
    while True:
        connection = None
        try:
            connection = websocket.create_connection(
                "ws://supervisor/core/websocket",
                timeout=30,
                http_proxy_host=None,
            )
            hello = json.loads(connection.recv())
            if hello.get("type") != "auth_required":
                raise RuntimeError("Home Assistant WebSocket không yêu cầu auth")
            connection.send(json.dumps({"type": "auth", "access_token": SUPERVISOR_TOKEN}))
            authenticated = json.loads(connection.recv())
            if authenticated.get("type") != "auth_ok":
                raise RuntimeError("Home Assistant WebSocket auth thất bại")
            connection.send(json.dumps({"id": 1, "type": "subscribe_events", "event_type": "state_changed"}))
            subscribed = json.loads(connection.recv())
            if subscribed.get("type") != "result" or not subscribed.get("success"):
                raise RuntimeError("Không subscribe được state_changed")
            with state_lock:
                ha_ws_status.update(
                    {"connected": True, "last_connected_at": now_iso(), "last_error": None}
                )
            publish_event("ha_websocket", dict(ha_ws_status))
            while True:
                try:
                    message = json.loads(connection.recv())
                except websocket.WebSocketTimeoutException:
                    connection.ping()
                    continue
                if message.get("type") != "event":
                    continue
                event = message.get("event") or {}
                event_data = event.get("data") or {}
                entity_id = event_data.get("entity_id")
                if not valid_entity(entity_id):
                    continue
                with state_lock:
                    interested = entity_id in playback_sessions or entity_id in active_casts
                    ha_ws_status["last_event_at"] = now_iso()
                if interested:
                    playback_handle_state(entity_id, event_data.get("new_state") or {})
        except Exception as error:
            with state_lock:
                ha_ws_status.update(
                    {"connected": False, "last_error": safe_text(error, 300)}
                )
            publish_event("ha_websocket", dict(ha_ws_status))
            logger.warning("Home Assistant WebSocket reconnecting: %s", error)
            time.sleep(5)
        finally:
            if connection is not None:
                try:
                    connection.close()
                except Exception:
                    pass

def playback_poll_worker():
    while True:
        try:
            with state_lock:
                entities = list(playback_sessions)
                connected = bool(ha_ws_status.get("connected"))
            if not connected:
                for entity_id in entities:
                    try:
                        playback_handle_state(entity_id, ha_get(f"/states/{entity_id}", timeout=4))
                    except Exception as error:
                        logger.info("Playback poll failed for %s: %s", entity_id, error)
            time.sleep(8 if connected else 2)
        except Exception as error:
            logger.error("Playback poll worker failed: %s", error)
            time.sleep(5)

def media_head_response(entry):
    content_type = cast_content_type(entry)
    total = max(0, safe_int(entry.get("content_length"), 0))
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": content_type,
        "Cache-Control": "no-store",
        "Content-Disposition": "inline",
    }
    if not total:
        return None
    range_header = str(request.headers.get("Range") or "").strip()
    if not range_header or not range_header.lower().startswith("bytes=") or "," in range_header:
        headers["Content-Length"] = str(total)
        return Response(status=200, headers=headers)
    raw_range = range_header[6:].strip()
    start_text, _, end_text = raw_range.partition("-")
    try:
        if start_text:
            start = int(start_text)
            end = int(end_text) if end_text else total - 1
        else:
            suffix = int(end_text)
            start = max(0, total - suffix)
            end = total - 1
    except (TypeError, ValueError):
        start = total
        end = total - 1
    if start < 0 or start >= total or end < start:
        headers["Content-Range"] = f"bytes */{total}"
        return Response(status=416, headers=headers)
    end = min(end, total - 1)
    headers["Content-Length"] = str(end - start + 1)
    headers["Content-Range"] = f"bytes {start}-{end}/{total}"
    return Response(status=206, headers=headers)


def purge_search_cache():
    now = time.time()
    expired = [key for key, entry in search_cache.items() if entry.get("expires_at", 0) <= now]
    for key in expired:
        search_cache.pop(key, None)
    while len(search_cache) > SEARCH_CACHE_LIMIT:
        oldest = min(
            search_cache,
            key=lambda key: search_cache[key].get("accessed_at", search_cache[key].get("created_at", 0)),
        )
        search_cache.pop(oldest, None)

def search_youtube(query, offset=0, limit=20, media_kind="audio"):
    require_valid_license_for_operation()
    media_kind = normalize_media_kind(media_kind)
    default_query = f"video thịnh hành Việt Nam {datetime.now().year}" if media_kind == "video" else f"nhạc hay {datetime.now().year}"
    query = str(query or "").strip()[:160] or default_query
    max_results = VIDEO_SEARCH_MAX_RESULTS if media_kind == "video" else SEARCH_MAX_RESULTS
    offset = max(0, min(safe_int(offset, 0), max_results))
    if offset >= max_results:
        return []
    limit = max(1, min(safe_int(limit, 20), 20, max_results - offset))
    needed = offset + limit
    batch_end = min(
        max_results,
        max(SEARCH_INITIAL_BATCH, math.ceil(needed / SEARCH_INITIAL_BATCH) * SEARCH_INITIAL_BATCH),
    )
    cache_key = f"{media_kind}:{query.casefold()}"
    with state_lock:
        purge_search_cache()
        cached = search_cache.get(cache_key)
        if cached and cached.get("expires_at", 0) > time.time() and len(cached.get("items", [])) >= needed:
            cached["accessed_at"] = time.time()
            return cached["items"][offset:needed]
    options = ydl_options({"extract_flat": "in_playlist", "skip_download": True, "playlistend": batch_end})
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(f"ytsearch{batch_end}:{query}", download=False)
    items = []
    for item in (info or {}).get("entries") or []:
        video_id = str(item.get("id") or "").strip()
        if not video_id:
            continue
        track = sanitize_track(
            {
                "id": video_id,
                "title": item.get("title"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": item.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                "duration": item.get("duration") or 0,
                "channel": item.get("channel") or item.get("uploader"),
                "channel_url": item.get("channel_url") or item.get("uploader_url"),
                "view_count": item.get("view_count") or 0,
                "upload_date": item.get("upload_date") or "",
                "description": item.get("description") or "",
                "media_kind": media_kind,
            }
        )
        if track:
            items.append(track)
    with state_lock:
        timestamp = time.time()
        search_cache[cache_key] = {
            "items": items,
            "created_at": timestamp,
            "accessed_at": timestamp,
            "expires_at": timestamp + SEARCH_TTL,
        }
        purge_search_cache()
    return items[offset:needed]


def search_video_youtube(query, offset=0, limit=20):
    return search_youtube(query, offset, limit, media_kind="video")

def radio_track_key(track):
    clean = sanitize_track(track)
    if not clean:
        return ""
    video_id = clean.get("id")
    if video_id:
        return f"id:{video_id}"
    parsed = urlparse(clean.get("url", ""))
    if parsed.hostname == "youtu.be":
        video_id = parsed.path.strip("/").split("/", 1)[0]
    else:
        query = parse_qs(parsed.query)
        video_id = (query.get("v") or [""])[0]
    return f"id:{video_id}" if video_id else f"url:{clean.get('url')}"

def radio_query_text(value):
    text = safe_text(value, 160)
    text = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", text)
    text = re.sub(
        r"\b(official|lyrics?|lyric|audio|video|mv|hd|4k|full|visualizer|topic|music)\b",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"[^\wÀ-ỹ\s-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()[:120]

def radio_query_for_seed(seed, media_kind="audio"):
    seed = sanitize_track(seed) or {}
    channel = radio_query_text(seed.get("channel"))
    title = radio_query_text(seed.get("title"))
    parts = [part for part in (channel, title) if part]
    if not parts:
        parts = ["nhạc hay mới nhất" if media_kind == "audio" else "video hay mới nhất"]
    suffix = " music" if media_kind == "audio" else " videos"
    query = " ".join(parts)
    if suffix.casefold() not in query.casefold():
        query = f"{query}{suffix}"
    return query[:160]

def radio_excluded_urls(entity_id=None, seed=None, profile_id=None):
    excluded = set()
    seed_key = radio_track_key(seed)
    if seed_key:
        excluded.add(seed_key)
    if entity_id and valid_entity(entity_id):
        session = playback_session_for(entity_id)
        if queue_session_active(session):
            excluded.update(radio_track_key(track) for track in session.get("tracks") or [])
    with state_lock:
        excluded.update(radio_track_key(track) for track in history[-20:])
        selected_id = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        profile = listener_profiles.get(selected_id) or listener_profiles.get("default")
        if profile:
            excluded.update(
                radio_track_key({"url": value})
                for value in profile.get("blocked_tracks", [])
                if valid_youtube_url(value)
            )
    return {value for value in excluded if value}


def listener_profile_has_signals(profile):
    if not isinstance(profile, dict):
        return False
    if profile.get("blocked_tracks") or profile.get("blocked_channels"):
        return True
    stats = profile.get("tracks") if isinstance(profile.get("tracks"), dict) else {}
    return any(
        isinstance(item, dict)
        and any(safe_int(item.get(field), 0) > 0 for field in ("plays", "likes", "dislikes", "skips"))
        for item in stats.values()
    )


def listener_track_is_blocked(track, profile):
    clean = sanitize_track(track)
    if not clean or not isinstance(profile, dict):
        return False
    blocked_tracks = set(profile.get("blocked_tracks") or [])
    blocked_channels = set(profile.get("blocked_channels") or [])
    return clean.get("url") in blocked_tracks or listener_channel_key(clean) in blocked_channels


def listener_track_score(track, profile, recent_urls=None):
    clean = sanitize_track(track) or {}
    stats = profile.get("tracks") if isinstance(profile, dict) and isinstance(profile.get("tracks"), dict) else {}
    stat = stats.get(clean.get("url"), {}) if clean else {}
    score = (
        safe_int(stat.get("likes"), 0) * 100
        + safe_int(stat.get("plays"), 0) * 4
        - safe_int(stat.get("dislikes"), 0) * 75
        - safe_int(stat.get("skips"), 0) * 10
    )
    channel = listener_channel_key(clean)
    if channel:
        for item in stats.values():
            if not isinstance(item, dict) or listener_channel_key(item) != channel:
                continue
            score += safe_int(item.get("likes"), 0) * 18
            score += safe_int(item.get("plays"), 0) * 1.5
            score -= safe_int(item.get("dislikes"), 0) * 12
    last_played = str(stat.get("last_played") or "")
    if last_played:
        try:
            stamp = datetime.fromisoformat(last_played)
            age_hours = max(0, (datetime.now() - stamp).total_seconds() / 3600)
            score += max(0, 18 - age_hours / 8)
        except (TypeError, ValueError, OverflowError):
            pass
    if recent_urls and clean.get("url") in recent_urls:
        score -= 36
    score += min(20, math.log1p(max(0, safe_int(clean.get("view_count"), 0)))) / 10
    return score


def rank_listener_tracks(candidates, profile, limit, exclude_keys=None):
    limit = max(1, min(safe_int(limit, PERSONAL_MIX_DEFAULT_LIMIT), PERSONAL_MIX_MAX_LIMIT))
    excluded = set(exclude_keys or [])
    normalized_excluded = set(excluded)
    for value in excluded:
        if valid_youtube_url(value):
            normalized_excluded.add(radio_track_key({"url": value}))
    recent_urls = {item.get("url") for item in history[-16:] if isinstance(item, dict)}
    unique = []
    seen_keys = set()
    for position, raw_track in enumerate(candidates or []):
        clean = sanitize_track(raw_track)
        key = radio_track_key(clean)
        if not clean or not key or key in seen_keys or key in normalized_excluded:
            continue
        if listener_track_is_blocked(clean, profile):
            continue
        seen_keys.add(key)
        unique.append(
            (
                position,
                listener_track_score(clean, profile, recent_urls),
                clean,
            )
        )
    if listener_profile_has_signals(profile):
        unique.sort(key=lambda item: (-item[1], item[0]))
    return [item[2] for item in unique[:limit]]


def personal_mix_search_queries(profile, media_kind="audio"):
    stats = profile.get("tracks") if isinstance(profile, dict) and isinstance(profile.get("tracks"), dict) else {}
    ranked = sorted(
        (item for item in stats.values() if isinstance(item, dict)),
        key=lambda item: (
            safe_int(item.get("likes"), 0) * 100
            + safe_int(item.get("plays"), 0) * 4
            - safe_int(item.get("dislikes"), 0) * 75,
            safe_int(item.get("plays"), 0),
        ),
        reverse=True,
    )
    queries = []
    for stat in ranked[:4]:
        title = radio_query_text(stat.get("title"))
        channel = radio_query_text(stat.get("channel"))
        parts = [part for part in (channel, title) if part]
        if not parts:
            continue
        suffix = " music" if media_kind == "audio" else " videos"
        query = " ".join(parts)
        if suffix.casefold() not in query.casefold():
            query = f"{query}{suffix}"
        if query.casefold() not in {item.casefold() for item in queries}:
            queries.append(query[:160])
    if not queries:
        with state_lock:
            recent = list(history[-6:])
        for track in reversed(recent):
            query = radio_query_for_seed(track, media_kind)
            if query.casefold() not in {item.casefold() for item in queries}:
                queries.append(query)
            if len(queries) >= 3:
                break
    if not queries:
        queries.append("nhạc hay mới nhất" if media_kind == "audio" else "video hay mới nhất")
    return queries[:4]


def generate_personal_mix(profile_id=None, media_kind="audio", limit=PERSONAL_MIX_DEFAULT_LIMIT):
    media_kind = normalize_media_kind(media_kind)
    limit = max(5, min(safe_int(limit, PERSONAL_MIX_DEFAULT_LIMIT), PERSONAL_MIX_MAX_LIMIT))
    with state_lock:
        selected_id = normalize_listener_profile_id(profile_id) if profile_id else active_listener_profile_id
        if selected_id not in listener_profiles:
            selected_id = "default"
        cached = personal_mix_cache.get((selected_id, media_kind, limit))
        if cached and cached.get("expires_at", 0) > time.time():
            return json.loads(json.dumps(cached["payload"], ensure_ascii=False))
        profile = json.loads(json.dumps(listener_profiles[selected_id], ensure_ascii=False))
    queries = personal_mix_search_queries(profile, media_kind)
    candidates = []
    last_error = None
    for query in queries:
        try:
            rows = search_youtube(
                query,
                0,
                min(30, max(limit + 8, 20)),
                media_kind=media_kind,
            )
            candidates.extend(rows or [])
        except Exception as error:
            last_error = error
            if not candidates and query == queries[-1]:
                raise
    recent_keys = {
        radio_track_key(item)
        for item in history[-12:]
        if isinstance(item, dict) and radio_track_key(item)
    }
    ranked = rank_listener_tracks(candidates, profile, limit, recent_keys)
    if len(ranked) < limit:
        ranked = rank_listener_tracks(candidates, profile, limit)
    if not ranked and last_error:
        raise last_error
    payload = {
        "success": True,
        "profile_id": selected_id,
        "profile": listener_profile_public(profile),
        "query": queries[0],
        "queries": queries,
        "tracks": ranked,
        "has_more": False,
    }
    with state_lock:
        personal_mix_cache[(selected_id, media_kind, limit)] = {
            "expires_at": time.time() + PERSONAL_MIX_CACHE_TTL,
            "payload": json.loads(json.dumps(payload, ensure_ascii=False)),
        }
    return payload


def generate_radio_tracks(
    seed,
    entity_id=None,
    media_kind="audio",
    limit=RADIO_DEFAULT_LIMIT,
    exclude_urls=None,
    profile_id=None,
):
    clean_seed = sanitize_track(seed)
    if not clean_seed:
        raise ValueError("Bài hát gốc không hợp lệ")
    media_kind = normalize_media_kind(media_kind or clean_seed.get("media_kind"))
    limit = max(5, min(safe_int(limit, RADIO_DEFAULT_LIMIT), RADIO_MAX_LIMIT))
    query = radio_query_for_seed(clean_seed, media_kind)
    excluded = radio_excluded_urls(entity_id, clean_seed, profile_id)
    for value in safe_list(exclude_urls, PLAYBACK_MAX_TRACKS):
        key = radio_track_key({"url": value}) if valid_youtube_url(value) else ""
        if key:
            excluded.add(key)
    candidates = []
    candidate_keys = set()
    queries = [query]
    channel = radio_query_text(clean_seed.get("channel"))
    if channel:
        fallback = f"{channel} {('nhạc' if media_kind == 'audio' else 'video')}"
        if fallback.casefold() != query.casefold():
            queries.append(fallback[:160])
    scan_limit = min(
        SEARCH_MAX_RESULTS if media_kind == "audio" else VIDEO_SEARCH_MAX_RESULTS,
        max(80, len(excluded) + limit + 20),
    )
    candidate_target = min(scan_limit, max(limit + 8, 20))
    for current_query in queries:
        for offset in range(0, scan_limit, 20):
            try:
                rows = search_youtube(
                    current_query,
                    offset,
                    min(20, limit + 8),
                    media_kind=media_kind,
                )
            except Exception:
                if candidates:
                    break
                raise
            if not rows:
                break
            for row in rows:
                clean = sanitize_track(row)
                key = radio_track_key(clean)
                if not clean or not key or key in excluded or key in candidate_keys:
                    continue
                candidate_keys.add(key)
                candidates.append(clean)
                if len(candidates) >= candidate_target:
                    break
            if len(candidates) >= candidate_target:
                break
        if len(candidates) >= candidate_target:
            break
    profile = listener_profile_snapshot(profile_id)
    ranked = rank_listener_tracks(candidates, profile, limit, excluded)
    return ranked, query

def set_session_radio(seed, query, media_kind, generated, profile_id=None):
    return {
        "enabled": True,
        "seed": sanitize_track(seed),
        "query": safe_text(query, 160),
        "media_kind": normalize_media_kind(media_kind),
        "profile_id": normalize_listener_profile_id(profile_id) or active_listener_profile_id,
        "generated": max(0, safe_int(generated, 0)),
        "updated_at": now_iso(),
    }

def maybe_schedule_radio_refill(entity_id):
    if not valid_entity(entity_id):
        return
    session = playback_session_for(entity_id)
    radio = normalize_radio_state(session.get("radio")) if session else None
    if not radio or not queue_session_active(session):
        return
    upcoming = max(0, len(session.get("tracks") or []) - safe_int(session.get("index"), 0) - 1)
    if upcoming > RADIO_REFILL_THRESHOLD:
        return
    with state_lock:
        if entity_id in radio_refill_pending:
            return
        radio_refill_pending.add(entity_id)

    def refill():
        try:
            current = playback_session_for(entity_id)
            if not queue_session_active(current):
                return
            metadata = normalize_radio_state(current.get("radio"))
            if not metadata:
                return
            tracks, query = generate_radio_tracks(
                metadata["seed"],
                entity_id,
                metadata.get("media_kind"),
                RADIO_REFILL_LIMIT,
                profile_id=metadata.get("profile_id"),
            )
            if not tracks:
                return
            with playback_lock(entity_id):
                with state_lock:
                    stored = playback_sessions.get(entity_id)
                    if (
                        not queue_session_active(stored)
                        or stored.get("session_id") != current.get("session_id")
                    ):
                        return
                    stored_tracks = list(stored.get("tracks") or [])
                    existing_keys = {radio_track_key(item) for item in stored_tracks}
                    additions = [
                        track
                        for track in tracks
                        if radio_track_key(track) not in existing_keys
                    ]
                    if not additions:
                        return
                    current_index = max(
                        0,
                        min(
                            safe_int(stored.get("index"), 0),
                            max(0, len(stored_tracks) - 1),
                        ),
                    )
                    stored_tracks, current_index = trim_session_tracks(
                        stored_tracks + additions,
                        current_index,
                    )
                    stored["tracks"] = stored_tracks
                    stored["index"] = current_index
                    old_radio = normalize_radio_state(stored.get("radio")) or metadata
                    old_generated = safe_int(old_radio.get("generated"), 0)
                    stored["radio"] = set_session_radio(
                        old_radio["seed"],
                        query,
                        old_radio.get("media_kind"),
                        old_generated + len(additions),
                        old_radio.get("profile_id"),
                    )
                    public = playback_session_public(stored)
                persist_playback_sessions()
                publish_event("playback", public)
                logger.info("Radio refilled %s with %s tracks", entity_id, len(additions))
        except Exception as error:
            logger.info("Radio refill failed for %s: %s", entity_id, public_ydl_error(error))
        finally:
            with state_lock:
                radio_refill_pending.discard(entity_id)

    threading.Thread(target=refill, daemon=True).start()

def create_radio(
    seed,
    entity_id=None,
    media_kind="audio",
    limit=RADIO_DEFAULT_LIMIT,
    mode="replace",
    start_if_missing=False,
    exclude_urls=None,
    profile_id=None,
):
    clean_seed = sanitize_track(seed)
    if not clean_seed:
        raise ValueError("Bài hát gốc không hợp lệ")
    media_kind = normalize_media_kind(media_kind or clean_seed.get("media_kind"))
    clean_seed["media_kind"] = media_kind
    mode = "append" if str(mode or "").strip().casefold() == "append" else "replace"
    excluded_values = [
        value
        for value in safe_list(exclude_urls, PLAYBACK_MAX_TRACKS)
        if valid_youtube_url(value)
    ]
    tracks, query = generate_radio_tracks(
        clean_seed,
        entity_id,
        media_kind,
        limit,
        excluded_values,
        profile_id,
    )
    session = playback_session_for(entity_id) if valid_entity(entity_id) else None
    if queue_session_active(session):
        with playback_lock(entity_id):
            with state_lock:
                stored = playback_sessions.get(entity_id)
                if not queue_session_active(stored):
                    session = None
                else:
                    current_tracks = list(stored.get("tracks") or [])
                    current_index = max(0, min(safe_int(stored.get("index"), 0), max(0, len(current_tracks) - 1)))
                    existing_keys = {radio_track_key(item) for item in current_tracks}
                    additions = [item for item in tracks if radio_track_key(item) not in existing_keys]
                    if mode == "replace":
                        next_tracks = current_tracks[:current_index + 1] + additions
                    else:
                        next_tracks = current_tracks + additions
                    next_tracks, current_index = trim_session_tracks(
                        next_tracks,
                        current_index,
                    )
                    stored["tracks"] = next_tracks
                    stored["index"] = current_index
                    previous_radio = normalize_radio_state(stored.get("radio"))
                    generated = len(additions)
                    if mode == "append" and previous_radio:
                        generated += safe_int(previous_radio.get("generated"), 0)
                    stored["radio"] = set_session_radio(
                        clean_seed,
                        query,
                        media_kind,
                        generated,
                        profile_id,
                    )
                    public = playback_session_public(stored)
            if session:
                persist_playback_sessions()
                publish_event("playback", public)
                return {
                    "success": True,
                    "query": query,
                    "seed": clean_seed,
                    "tracks": additions,
                    "media_kind": media_kind,
                    "mode": mode,
                    "profile_id": normalize_listener_profile_id(profile_id) or active_listener_profile_id,
                    "session": public,
                    "queue": session_queue_view(stored),
                }
    if start_if_missing and valid_entity(entity_id):
        start_tracks = [clean_seed, *tracks]
        started = start_playback_session(
            entity_id,
            start_tracks,
            0,
            "off",
            False,
            "radio",
            query,
        )
        with playback_lock(entity_id):
            with state_lock:
                stored = playback_sessions.get(entity_id)
                if stored:
                    stored["radio"] = set_session_radio(
                        clean_seed,
                        query,
                        media_kind,
                        len(tracks),
                        profile_id,
                    )
                    started = playback_session_public(stored)
            persist_playback_sessions()
            publish_event("playback", started)
        return {
            "success": True,
            "query": query,
            "seed": clean_seed,
            "tracks": tracks,
            "media_kind": media_kind,
            "mode": mode,
            "profile_id": normalize_listener_profile_id(profile_id) or active_listener_profile_id,
            "session": started,
            "queue": session_queue_view(playback_session_for(entity_id)),
        }
    return {
        "success": True,
        "query": query,
        "seed": clean_seed,
        "tracks": tracks,
        "media_kind": media_kind,
        "mode": mode,
        "profile_id": normalize_listener_profile_id(profile_id) or active_listener_profile_id,
        "session": None,
        "queue": None,
    }


def create_personal_mix(
    entity_id=None,
    profile_id=None,
    media_kind="audio",
    limit=PERSONAL_MIX_DEFAULT_LIMIT,
    start_if_requested=False,
    shuffle=True,
):
    payload = generate_personal_mix(profile_id, media_kind, limit)
    tracks = list(payload.get("tracks") or [])
    if start_if_requested:
        if not valid_entity(entity_id):
            raise ValueError("Thiết bị phát không hợp lệ")
        if not tracks:
            raise ValueError("Personal Mix chưa có bài phù hợp")
        profile = payload.get("profile") or {}
        session = start_playback_session(
            entity_id,
            tracks,
            0,
            "all",
            bool(shuffle),
            "personal_mix",
            profile.get("name") or "Personal Mix",
        )
        payload["session"] = session
        payload["queue"] = session_queue_view(playback_session_for(entity_id))
    else:
        payload["session"] = None
        payload["queue"] = None
    return payload


def normalize_timer(value):
    if not isinstance(value, dict):
        return None
    run_time = normalize_time(value.get("time") or value.get("at"))
    timer_type = value.get("type") or "play"
    entity_id = value.get("entity_id")
    days = sorted({day for day in (value.get("days") or []) if isinstance(day, int) and 0 <= day <= 6})
    if not run_time or timer_type not in {"play", "stop"} or not valid_entity(entity_id):
        return None
    try:
        duration = max(0, min(int(value.get("duration") or 0), 720))
    except (TypeError, ValueError):
        duration = 0
    return {
        "id": str(value.get("id") or uuid.uuid4())[:80],
        "time": run_time,
        "type": timer_type,
        "entity_id": entity_id,
        "playlist_name": normalize_name(value.get("playlist_name")) or "",
        "days": days,
        "is_random": bool(value.get("is_random", True)),
        "enabled": bool(value.get("enabled", True)),
        "duration": duration,
        "last_trigger_date": value.get("last_trigger_date"),
        "last_triggered_at": safe_text(value.get("last_triggered_at"), 40),
        "last_attempt_at": safe_text(value.get("last_attempt_at"), 40),
        "last_error": safe_text(value.get("last_error"), 300),
    }


def migrate_timers():
    global timers
    normalized = [timer for timer in (normalize_timer(item) for item in timers) if timer]
    existing_ids = {timer["id"] for timer in normalized}
    for item in load_json(LEGACY_SCHEDULE_FILE, []):
        timer = normalize_timer(item)
        if timer and timer["id"] not in existing_ids:
            normalized.append(timer)
            existing_ids.add(timer["id"])
    timers = normalized[-100:]
    save_json(TIMER_FILE, timers)


def stop_entity(entity_id):
    if valid_entity(entity_id):
        if playback_session_for(entity_id):
            stop_playback_session(entity_id, stop_player=True)
        else:
            ha_service("media_stop", {"entity_id": entity_id})
            clear_active_cast(entity_id)


def active_cast_position_locked(value=None, now=None):
    current_cast = value if isinstance(value, dict) else active_cast
    current = max(0, safe_float(current_cast.get("position"), 0))
    updated = max(0, safe_float(current_cast.get("position_updated_at"), 0))
    if current_cast.get("expected_state") == "playing" and updated:
        current += max(0, (now or time.time()) - updated)
    duration = max(0, safe_float(current_cast.get("duration"), 0))
    return min(current, duration) if duration else current


def set_sleep(minutes, entity_id):
    global sleep_timer
    with state_lock:
        sleep_timer = {
            "enabled": True,
            "minutes": minutes,
            "entity_id": entity_id,
            "end_at": (datetime.now() + timedelta(minutes=minutes)).isoformat(timespec="seconds"),
            "created_at": now_iso(),
        }
        save_json(SLEEP_FILE, sleep_timer)
    return dict(sleep_timer)


def sleep_worker():
    global sleep_timer
    while True:
        try:
            with state_lock:
                current = dict(sleep_timer) if isinstance(sleep_timer, dict) else {}
            if current.get("enabled") and current.get("end_at"):
                end_time = datetime.fromisoformat(current["end_at"]).timestamp()
                now = time.time()
                remaining = end_time - now
                entity_id = current.get("entity_id")
                fade_enabled = safe_bool(addon_options().get("sleep_fade"), True)
                if (
                    fade_enabled
                    and remaining > 0
                    and remaining <= SLEEP_FADE_SECONDS
                    and entity_id
                    and entity_id != "browser"
                ):
                    with state_lock:
                        base_volume = sleep_timer.get("fade_base_volume")
                        last_fade = sleep_timer.get("fade_volume")
                    if base_volume is None:
                        try:
                            row = ha_get(f"/states/{entity_id}", timeout=4)
                            base_volume = safe_float((row.get("attributes") or {}).get("volume_level"), -1)
                        except Exception:
                            base_volume = -1
                        if base_volume is None or base_volume < 0:
                            base_volume = 0
                        with state_lock:
                            if isinstance(sleep_timer, dict) and sleep_timer.get("enabled"):
                                sleep_timer["fade_base_volume"] = base_volume
                    target = max(0.0, min(1.0, base_volume * max(0.0, remaining / SLEEP_FADE_SECONDS)))
                    if last_fade is None or abs(target - last_fade) >= 0.02:
                        try:
                            ha_service("volume_set", {"entity_id": entity_id, "volume_level": round(target, 3)})
                        except Exception as error:
                            logger.info("Sleep fade volume thất bại cho %s: %s", entity_id, error)
                        with state_lock:
                            if isinstance(sleep_timer, dict) and sleep_timer.get("enabled"):
                                sleep_timer["fade_volume"] = target
                if now >= end_time:
                    if entity_id != "browser":
                        stop_entity(entity_id)
                    base_volume = current.get("fade_base_volume")
                    if base_volume is not None and entity_id and entity_id != "browser":
                        try:
                            ha_service("volume_set", {"entity_id": entity_id, "volume_level": base_volume})
                        except Exception as error:
                            logger.info("Khôi phục âm lượng sau sleep thất bại cho %s: %s", entity_id, error)
                    with state_lock:
                        sleep_timer = {
                            "enabled": False,
                            "entity_id": entity_id,
                            "minutes": current.get("minutes", 0),
                            "last_triggered_at": now_iso(),
                        }
                        save_json(SLEEP_FILE, sleep_timer)
            time.sleep(2)
        except Exception as error:
            logger.error("Sleep worker failed: %s", error)
            time.sleep(5)


def run_timer_cycle(now=None):
    if license_manager and not license_manager.permits_use():
        return []
    global timers
    current_time = now or datetime.now()
    minute = current_time.strftime("%H:%M")
    today = current_time.strftime("%Y-%m-%d")
    due = []
    with state_lock:
        for timer in timers:
            if not timer.get("enabled", True):
                continue
            days = timer.get("days") or []
            if timer.get("time") != minute or (days and current_time.weekday() not in days):
                continue
            if timer.get("last_trigger_date") == today:
                continue
            last_attempt_at = timer.get("last_attempt_at")
            if last_attempt_at:
                try:
                    elapsed = (current_time - datetime.fromisoformat(last_attempt_at)).total_seconds()
                    if elapsed < TIMER_RETRY_SECONDS:
                        continue
                except (TypeError, ValueError):
                    pass
            timer["last_attempt_at"] = current_time.isoformat(timespec="seconds")
            due.append(dict(timer))
        if due:
            save_json(TIMER_FILE, timers)
    results = []
    for timer in due:
        error_text = ""
        try:
            if timer["type"] == "stop":
                stop_entity(timer["entity_id"])
            else:
                with state_lock:
                    playlist = list(playlists.get(timer.get("playlist_name")) or [])
                if not playlist:
                    raise RuntimeError("Playlist trống hoặc không tồn tại")
                start_playback_session(
                    timer["entity_id"],
                    playlist,
                    0,
                    "all",
                    bool(timer.get("is_random", True)),
                    "timer",
                    timer.get("playlist_name"),
                )
                if timer.get("duration"):
                    set_sleep(timer["duration"], timer["entity_id"])
        except Exception as error:
            error_text = safe_text(error, 300)
            logger.error("Timer %s failed: %s", timer.get("id"), error)
        with state_lock:
            stored = next((item for item in timers if item.get("id") == timer.get("id")), None)
            if stored:
                if error_text:
                    stored["last_error"] = error_text
                else:
                    stored.update(
                        {
                            "last_trigger_date": today,
                            "last_triggered_at": now_iso(),
                            "last_error": "",
                        }
                    )
                save_json(TIMER_FILE, timers)
        results.append({"id": timer.get("id"), "success": not error_text, "error": error_text})
    return results

def timer_worker():
    while True:
        try:
            run_timer_cycle()
            time.sleep(10)
        except Exception as error:
            logger.error("Timer worker failed: %s", error)
            time.sleep(10)


def integration_status_payload():
    ha_ok = False
    try:
        ha_get("/config", timeout=3)
        ha_ok = True
    except Exception:
        pass
    with state_lock:
        sessions = {
            entity_id: playback_session_public(session)
            for entity_id, session in playback_sessions.items()
        }
        transports = {
            entity_id: value.get("transport")
            for entity_id, value in active_casts.items()
            if value.get("transport")
        }
        extractor = dict(last_extractor)
        websocket_status = dict(ha_ws_status)
        playlist_summary = [
            {"name": name, "track_count": len(items)}
            for name, items in sorted(playlists.items())
        ]
        queue_count = len(queue)
        timer_count = len(timers)
    active_states = {"resolving", "starting", "playing", "paused"}
    active_session_count = sum(
        1 for session in sessions.values() if session and session.get("state") in active_states
    )
    return {
        "success": True,
        "api_version": INTEGRATION_API_VERSION,
        "version": APP_VERSION,
        "health": "ok" if ha_ok else "degraded",
        "ha_ok": ha_ok,
        "websocket_connected": bool(websocket_status.get("connected")),
        "websocket_last_error": websocket_status.get("last_error"),
        "extractor": extractor.get("strategy") or "idle",
        "format_id": extractor.get("format_id"),
        "resolve_ms": extractor.get("elapsed_ms"),
        "last_resolved_at": extractor.get("resolved_at"),
        "last_error": last_error,
        "active_session_count": active_session_count,
        "sessions": sessions,
        "transports": transports,
        "playlists": playlist_summary,
        "queue_count": queue_count,
        "timer_count": timer_count,
        "listener_profile": listener_preferences_public().get("active_profile"),
        "license": license_manager.integration_status() if license_manager else None,
    }


def integration_track_page(items, reverse=False):
    tracks = list(items or [])
    if reverse:
        tracks.reverse()
    offset = max(0, safe_int(request.args.get("offset"), 0))
    limit = max(1, min(safe_int(request.args.get("limit"), 100), MEDIA_BROWSER_MAX_TRACKS))
    page = tracks[offset:offset + limit]
    return {
        "success": True,
        "tracks": [dict(track) for track in page],
        "offset": offset,
        "total": len(tracks),
        "has_more": offset + len(page) < len(tracks),
    }


def listener_preferences_action(data):
    if not isinstance(data, dict):
        raise ValueError("Dữ liệu hồ sơ nghe không hợp lệ")
    action = safe_text(data.get("action"), 24).casefold()
    profile_id = data.get("profile_id")
    if not action and profile_id:
        action = "switch"
    if action in {"switch", "select", "activate"}:
        return set_active_listener_profile(profile_id)
    if action in {"create", "new"}:
        return create_listener_profile(data.get("name"))
    if action in {"delete", "remove"}:
        return delete_listener_profile(profile_id)
    if action in {"rename", "update"}:
        normalized_id = normalize_listener_profile_id(profile_id)
        name = safe_text(data.get("name"), 60)
        if not normalized_id or not name:
            raise ValueError("Hồ sơ nghe không hợp lệ")
        with state_lock:
            profile = listener_profiles.get(normalized_id)
            if not profile:
                raise ValueError("Không tìm thấy hồ sơ nghe")
            if any(
                item.get("id") != normalized_id
                and item.get("name", "").casefold() == name.casefold()
                for item in listener_profiles.values()
            ):
                raise ValueError("Tên hồ sơ đã tồn tại")
            profile["name"] = name
            profile["updated_at"] = now_iso()
        persist_listener_profiles()
        invalidate_personal_mix_cache(normalized_id)
        return listener_preferences_public()
    raise ValueError("Thao tác hồ sơ nghe không hợp lệ")


def listener_feedback_action(data):
    if not isinstance(data, dict):
        raise ValueError("Dữ liệu phản hồi nghe không hợp lệ")
    action = safe_text(data.get("action"), 24).casefold()
    if action in {"undo", "revert"}:
        return {
            "success": True,
            "profile": undo_listener_feedback(data.get("profile_id")),
            "preferences": listener_preferences_public(),
        }
    track = data.get("track") if isinstance(data.get("track"), dict) else data
    if action in {"block", "block_video", "block_song"}:
        action = "block_track"
    if action in {"channel", "block_artist"}:
        action = "block_channel"
    profile = record_listener_event(track, action, data.get("profile_id"))
    if profile is None:
        raise ValueError("Bài hát không hợp lệ")
    return {
        "success": True,
        "profile": profile,
        "action": action,
        "feedback": listener_feedback_state(track, data.get("profile_id")),
        "preferences": listener_preferences_public(),
    }


def personal_mix_request(data):
    if not isinstance(data, dict):
        raise ValueError("Dữ liệu Personal Mix không hợp lệ")
    profile_id = normalize_listener_profile_id(data.get("profile_id"))
    if safe_bool(data.get("refresh")):
        invalidate_personal_mix_cache(profile_id)
    return create_personal_mix(
        data.get("entity_id"),
        profile_id,
        data.get("media_kind"),
        data.get("limit"),
        safe_bool(data.get("start_if_missing") or data.get("start")),
        safe_bool(data.get("shuffle"), True),
    )


def request_json_object():
    value = request.get_json(silent=True)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("JSON body phải là object")
    return value


@app.route("/")
def index():
    license_bootstrap = {}
    if license_manager:
        cached_license = license_manager.current_status()
        if cached_license.get("valid") and license_manager.permits_use():
            license_bootstrap = cached_license
    return render_template(
        "index.html",
        version=APP_VERSION,
        license_bootstrap=license_bootstrap,
    )


@app.route("/icon.png")
def addon_icon():
    return send_from_directory(os.path.dirname(__file__), "icon.png", max_age=86400)


@app.route("/api/health")
def health():
    licensed = bool(license_manager and license_manager.permits_use())
    return jsonify({"ok": True, "version": APP_VERSION, "licensed": licensed})


@app.route("/api/license", methods=["GET", "POST", "DELETE"])
def license_api():
    if not license_manager:
        return jsonify({"success": False, "error": "License manager chưa sẵn sàng"}), 503
    if request.method == "GET":
        force = request.args.get("refresh") in {"1", "true", "yes"}
        return jsonify({"success": True, "license": license_manager.status(force=force)})
    if request.method == "DELETE":
        return jsonify({"success": True, "license": license_manager.deactivate()})
    data = request.get_json(silent=True) or {}
    try:
        status = license_manager.activate(data.get("license_key"))
    except (ValueError, RuntimeError, requests.RequestException) as error:
        return jsonify({"success": False, "error": safe_text(error, 240)}), 400
    if not status.get("valid"):
        return jsonify(
            {
                "success": False,
                "error": f"License không hợp lệ: {status.get('code') or status.get('state')}",
                "license": status,
            }
        ), 400
    return jsonify({"success": True, "license": status})


@app.route("/api/integration-token", methods=["GET", "POST"])
def integration_token_api():
    if request.method == "POST" and request.headers.get("X-YouTube-Pro-Action") != "rotate-token":
        return jsonify({"success": False, "error": "Yêu cầu rotate token không hợp lệ"}), 400
    token = rotate_integration_api_token() if request.method == "POST" else integration_api_token()
    return jsonify(
        {
            "success": True,
            "token": token,
            "updated_at": integration_token_status().get("updated_at"),
            "rotated": request.method == "POST",
        }
    )


@app.route("/api/integration/health")
def integration_health_api():
    return jsonify(
        {
            "success": True,
            "api_version": INTEGRATION_API_VERSION,
            "version": APP_VERSION,
            "license": license_manager.integration_status() if license_manager else None,
        }
    )


@app.route("/api/integration/status")
def integration_status_api():
    return jsonify(integration_status_payload())


@app.route("/api/integration/preferences", methods=["GET", "POST"])
def integration_preferences_api():
    if request.method == "GET":
        return jsonify(listener_preferences_public())
    try:
        return jsonify(listener_preferences_action(request_json_object()))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/integration/preferences/feedback", methods=["POST"])
def integration_preferences_feedback_api():
    try:
        return jsonify(listener_feedback_action(request_json_object()))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/integration/personal-mix", methods=["GET", "POST"])
def integration_personal_mix_api():
    try:
        data = (
            request.args.to_dict()
            if request.method == "GET"
            else request_json_object()
        )
        return jsonify(personal_mix_request(data))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        logger.error("Integration Personal Mix failed: %s", error)
        return jsonify({"success": False, "error": public_ydl_error(error)}), 502


@app.route("/api/integration/playlists")
def integration_playlists_api():
    with state_lock:
        result = [
            {"name": name, "track_count": len(items)}
            for name, items in sorted(playlists.items())
        ]
    return jsonify({"success": True, "playlists": result})


@app.route("/api/integration/library")
def integration_library_api():
    with state_lock:
        playlist_summary = [
            {
                "name": name,
                "track_count": len(items),
                "thumbnail": next((item.get("thumbnail") for item in items if item.get("thumbnail")), ""),
            }
            for name, items in sorted(playlists.items())
        ]
        payload = {
            "success": True,
            "playlists": playlist_summary,
            "queue_count": len(queue),
            "history_count": len(history),
            "search_history": list(search_history),
            "discovery": [dict(item) for item in MEDIA_BROWSER_DISCOVERY],
            "video_discovery": [dict(item) for item in VIDEO_DISCOVERY],
            "listener_profile": listener_profile_public(
                listener_profiles.get(active_listener_profile_id)
                or listener_profiles.get("default")
            ),
        }
    return jsonify(payload)


@app.route("/api/integration/playlists/<name>")
def integration_playlist_items_api(name):
    playlist_name = normalize_name(name)
    if not playlist_name:
        return jsonify({"success": False, "error": "Playlist không hợp lệ"}), 400
    with state_lock:
        if playlist_name not in playlists:
            return jsonify({"success": False, "error": "Không tìm thấy playlist"}), 404
        payload = integration_track_page(playlists[playlist_name])
    payload["name"] = playlist_name
    return jsonify(payload)


@app.route("/api/integration/queue")
def integration_queue_api():
    entity_id = request.args.get("entity_id")
    if entity_id and valid_entity(entity_id) and playback_session_for(entity_id):
        view = queue_view_payload(entity_id)
        payload = integration_track_page(view.get("tracks"))
        payload.update(
            {
                "scope": view.get("scope"),
                "entity_id": view.get("entity_id"),
                "current_track": view.get("current_track"),
                "session": view.get("session"),
            }
        )
    else:
        with state_lock:
            payload = integration_track_page(queue)
    payload["name"] = "Hàng chờ"
    return jsonify(payload)


@app.route("/api/integration/history")
def integration_history_api():
    with state_lock:
        payload = integration_track_page(history, reverse=True)
    payload["name"] = "Nghe gần đây"
    return jsonify(payload)


@app.route("/api/integration/search", methods=["POST"])
def integration_search_api():
    global last_error
    data = request.get_json(silent=True) or {}
    query = safe_text(data.get("query"), 160)
    if not query:
        return jsonify({"success": False, "error": "Từ khóa tìm kiếm không hợp lệ"}), 400
    try:
        offset = max(0, safe_int(data.get("offset"), 0))
        limit = max(1, min(safe_int(data.get("limit"), 20), 20))
        media_kind = normalize_media_kind(data.get("media_kind") or data.get("mode"))
        results = search_youtube(query, offset, limit, media_kind=media_kind)
        record_search_query(query)
        last_error = None
        max_results = VIDEO_SEARCH_MAX_RESULTS if media_kind == "video" else SEARCH_MAX_RESULTS
        return jsonify(
            {
                "success": True,
                "query": query,
                "results": results,
                "offset": offset,
                "media_kind": media_kind,
                "has_more": len(results) >= limit and offset + len(results) < max_results,
            }
        )
    except Exception as error:
        last_error = public_ydl_error(error)
        logger.error("Integration yt-dlp search failed: %s", error)
        return jsonify({"success": False, "error": last_error}), 502


@app.route("/api/integration/resolve", methods=["POST"])
def integration_resolve_api():
    data = request.get_json(silent=True) or {}
    try:
        requested_kind = normalize_media_kind(
            data.get("media_kind") or data.get("mode")
        )
        media_kind = requested_kind
        entity_id = data.get("entity_id")
        if requested_kind == "video" and valid_entity(entity_id):
            profile = entity_profile(entity_id, refresh=True)
            if profile and not profile.get("can_play_video", False):
                media_kind = "audio"
        resolver = resolve_video if media_kind == "video" else resolve_track
        resolved = resolver(data.get("url"))
        token, entry = cache_resolved(resolved)
        return jsonify(
            {
                "success": True,
                "media_url": relay_url(token, entry),
                "content_type": cast_content_type(entry),
                "media_kind": requested_kind,
                "effective_media_kind": media_kind,
                "track": entry.get("track") or {},
                "expires_in": STREAM_TTL,
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/integration/control", methods=["POST"])
def integration_control_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    action = data.get("action")
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị không hợp lệ"}), 400
    if action not in {"play", "pause", "stop", "next", "previous", "mode"}:
        return jsonify({"success": False, "error": "Lệnh playback không hợp lệ"}), 400
    try:
        session = playback_session_for(entity_id)
        if action == "next":
            session = advance_playback_session(entity_id, 1) if session else None
            if session is None:
                ha_service("media_next_track", {"entity_id": entity_id})
        elif action == "previous":
            session = advance_playback_session(entity_id, -1) if session else None
            if session is None:
                ha_service("media_previous_track", {"entity_id": entity_id})
        elif action == "stop":
            session = stop_playback_session(entity_id, stop_player=True) if session else None
            if session is None:
                ha_service("media_stop", {"entity_id": entity_id})
        elif action == "pause":
            ha_service("media_pause", {"entity_id": entity_id})
        elif action == "mode":
            if not session:
                return jsonify({"success": False, "error": "Chưa có phiên phát cho thiết bị"}), 409
            session = update_playback_mode(entity_id, data.get("repeat"), data.get("shuffle"))
        elif session and session.get("state") in {"stopped", "completed", "error"}:
            if session.get("state") == "completed":
                playback_update_session(entity_id, {"index": 0, "state": "idle", "stop_requested": False})
            session = playback_play_current(entity_id)
        else:
            ha_service("media_play", {"entity_id": entity_id})
        return jsonify(
            {
                "success": True,
                "session": playback_session_public(session) if session else None,
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/integration/play", methods=["POST"])
def integration_play_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    track_data = data.get("track") if isinstance(data.get("track"), dict) else {}
    requested_kind = normalize_media_kind(
        track_data.get("media_kind")
        or data.get("media_kind")
        or data.get("mode")
        or "audio"
    )
    track_data = {
        **track_data,
        "url": track_data.get("url") or data.get("url"),
        "title": track_data.get("title") or data.get("title") or "YouTube",
        "media_kind": requested_kind,
    }
    track = sanitize_track(track_data)
    if not valid_entity(entity_id) or not track:
        return jsonify({"success": False, "error": "Thiết bị hoặc URL YouTube không hợp lệ"}), 400
    try:
        session = start_playback_session(
            entity_id,
            [track],
            0,
            data.get("repeat"),
            bool(data.get("shuffle")),
            "integration",
            safe_text(data.get("source_name") or "Home Assistant", 160),
        )
        return jsonify({"success": True, "session": session})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/integration/play-playlist", methods=["POST"])
def integration_play_playlist_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    playlist_name = normalize_name(data.get("playlist_name"))
    if not valid_entity(entity_id) or not playlist_name:
        return jsonify({"success": False, "error": "Thiết bị hoặc playlist không hợp lệ"}), 400
    with state_lock:
        tracks = list(playlists.get(playlist_name) or [])
    if not tracks:
        return jsonify({"success": False, "error": "Playlist trống hoặc không tồn tại"}), 404
    try:
        session = start_playback_session(
            entity_id,
            tracks,
            data.get("index"),
            data.get("repeat") or "all",
            bool(data.get("shuffle")),
            "playlist",
            playlist_name,
        )
        return jsonify({"success": True, "session": session})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/integration/enqueue", methods=["POST"])
def integration_enqueue_api():
    data = request.get_json(silent=True) or {}
    track_data = data.get("track") if isinstance(data.get("track"), dict) else {}
    requested_kind = normalize_media_kind(
        track_data.get("media_kind")
        or data.get("media_kind")
        or data.get("mode")
        or "audio"
    )
    track_data = {
        **track_data,
        "url": track_data.get("url") or data.get("url"),
        "title": track_data.get("title") or data.get("title") or "YouTube",
        "media_kind": requested_kind,
    }
    track = sanitize_track(track_data)
    if not track:
        return jsonify({"success": False, "error": "URL YouTube không hợp lệ"}), 400
    try:
        result = queue_enqueue_track(
            track,
            data.get("entity_id"),
            data.get("position"),
        )
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    result["queue_count"] = (
        result.get("queue", {}).get("total", 0)
        if isinstance(result.get("queue"), dict)
        else 0
    )
    return jsonify(result)

@app.route("/api/integration/queue/items", methods=["PATCH", "DELETE", "POST"])
def integration_queue_items_api():
    data = request.get_json(silent=True) or {}
    try:
        if request.method == "PATCH":
            result = queue_reorder_items(
                data.get("from_index"),
                data.get("to_index"),
                data.get("entity_id"),
            )
        elif request.method == "DELETE":
            if data.get("clear"):
                result = queue_clear(data.get("entity_id"))
            else:
                result = queue_remove_item(data.get("index"), data.get("entity_id"))
        else:
            result = queue_enqueue_track(
                data.get("track") if isinstance(data.get("track"), dict) else data,
                data.get("entity_id"),
                data.get("position"),
            )
        return jsonify(result)
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

@app.route("/api/integration/queue/shuffle", methods=["POST"])
def integration_queue_shuffle_api():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(queue_shuffle(data.get("entity_id")))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

@app.route("/api/integration/radio", methods=["POST"])
def integration_radio_api():
    data = request.get_json(silent=True) or {}
    seed = data.get("seed") if isinstance(data.get("seed"), dict) else data.get("track")
    if not isinstance(seed, dict):
        seed = {"url": data.get("url"), "title": data.get("title"), "media_kind": data.get("media_kind")}
    try:
        return jsonify(
            create_radio(
                seed,
                data.get("entity_id"),
                data.get("media_kind"),
                data.get("limit"),
                data.get("mode"),
                bool(data.get("start_if_missing")),
                data.get("exclude_urls"),
                data.get("profile_id"),
            )
        )
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        logger.error("Integration radio generation failed: %s", error)
        return jsonify({"success": False, "error": public_ydl_error(error)}), 502


@app.route("/api/integration/timers", methods=["POST"])
def integration_timer_api():
    global timers
    data = request.get_json(silent=True) or {}
    timer = normalize_timer(data)
    if not timer:
        return jsonify({"success": False, "error": "Lịch phát không hợp lệ"}), 400
    if timer["type"] == "play":
        with state_lock:
            playlist_exists = bool(playlists.get(timer["playlist_name"]))
        if not playlist_exists:
            return jsonify({"success": False, "error": "Playlist trống hoặc không tồn tại"}), 400
    with state_lock:
        old = next((item for item in timers if item.get("id") == timer["id"]), None)
        if old:
            timer["last_trigger_date"] = old.get("last_trigger_date")
            timer["last_triggered_at"] = old.get("last_triggered_at", "")
        timers = [item for item in timers if item.get("id") != timer["id"]]
        timers.append(timer)
        timers = timers[-100:]
        save_json(TIMER_FILE, timers)
    return jsonify({"success": True, "timer": timer})


@app.route("/api/status")
def status():
    ha_ok = False
    try:
        ha_get("/config", timeout=4)
        ha_ok = True
    except Exception:
        pass
    with state_lock:
        cast_status = dict(active_cast)
        cast_statuses = {entity_id: dict(value) for entity_id, value in active_casts.items()}
        sessions = {
            entity_id: playback_session_public(session)
            for entity_id, session in playback_sessions.items()
        }
        websocket_status = dict(ha_ws_status)
    cast_status.pop("media_url", None)
    for value in cast_statuses.values():
        value.pop("media_url", None)
    return jsonify(
        {
            "ok": True,
            "version": APP_VERSION,
            "ha_ok": ha_ok,
            "deno": bool(shutil.which("deno")),
            "ejs": EJS_VERSION,
            "yt_dlp": YTDLP_VERSION,
            "media_base_url": media_base_url(),
            "cookie": cookie_status(),
            "last_extractor": dict(last_extractor),
            "extractor_preference": extractor_preference_status(),
            "pot_token_provider": pot_provider_status(),
            "cast_preference": cast_preference_status(cast_status.get("entity_id")),
            "last_error": last_error,
            "active_cast": cast_status,
            "active_casts": cast_statuses,
            "playback_sessions": sessions,
            "ha_websocket": websocket_status,
            "integration_api": {
                "api_version": INTEGRATION_API_VERSION,
                **integration_token_status(),
            },
            "listener_profile": listener_preferences_public().get("active_profile"),
            "license": license_manager.current_status() if license_manager else None,
        }
    )

@app.route("/api/events")
def events_api():
    subscriber = queue_module.Queue(maxsize=20)
    with state_lock:
        event_subscribers.add(subscriber)
        initial_sessions = {
            entity_id: playback_session_public(session)
            for entity_id, session in playback_sessions.items()
        }

    def generate():
        try:
            initial = json.dumps(
                {"type": "snapshot", "data": {"playback_sessions": initial_sessions}, "at": now_iso()},
                ensure_ascii=False,
                separators=(",", ":"),
            )
            yield f"data: {initial}\n\n"
            while True:
                try:
                    message = subscriber.get(timeout=15)
                    yield f"data: {message}\n\n"
                except queue_module.Empty:
                    yield ": keepalive\n\n"
        finally:
            with state_lock:
                event_subscribers.discard(subscriber)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@app.route("/api/cast-preferences", methods=["GET", "DELETE"])
def cast_preferences_api():
    global cast_preferences
    if request.method == "GET":
        return jsonify({"success": True, "profiles": cast_preference_status()})
    entity_id = str((request.get_json(silent=True) or {}).get("entity_id") or "").strip()
    with state_lock:
        if entity_id:
            cast_preferences.setdefault("entities", {}).pop(entity_id, None)
        else:
            cast_preferences = {"generation": CAST_PREF_GENERATION, "entities": {}}
    persist_cast_preferences()
    return jsonify({"success": True, "profiles": cast_preference_status()})


@app.route("/api/preferences", methods=["GET", "POST"])
def preferences_api():
    if request.method == "GET":
        return jsonify(listener_preferences_public())
    try:
        return jsonify(listener_preferences_action(request_json_object()))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/preferences/feedback", methods=["POST"])
def preferences_feedback_api():
    try:
        return jsonify(listener_feedback_action(request_json_object()))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/preferences/undo", methods=["POST"])
def preferences_undo_api():
    try:
        data = request_json_object()
        return jsonify(
            {
                "success": True,
                "profile": undo_listener_feedback(data.get("profile_id")),
                "preferences": listener_preferences_public(),
            }
        )
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/personal-mix", methods=["GET", "POST"])
def personal_mix_api():
    try:
        data = (
            request.args.to_dict()
            if request.method == "GET"
            else request_json_object()
        )
        return jsonify(personal_mix_request(data))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        logger.error("Personal Mix failed: %s", error)
        return jsonify({"success": False, "error": public_ydl_error(error)}), 502


@app.route("/api/cookies", methods=["GET", "POST", "DELETE"])
def cookies_api():
    global last_error
    if request.method == "GET":
        return jsonify({"success": True, "cookie": cookie_status()})
    if request.method == "DELETE":
        try:
            os.remove(COOKIE_FILE)
        except FileNotFoundError:
            pass
        except OSError as error:
            return jsonify({"success": False, "error": str(error)}), 500
        clear_youtube_session()
        last_error = None
        return jsonify({"success": True, "cookie": cookie_status()})

    upload = request.files.get("file")
    if not upload or not upload.filename:
        return jsonify({"success": False, "error": "Hãy chọn file cookies.txt"}), 400
    raw = upload.stream.read(COOKIE_MAX_BYTES + 1)
    if len(raw) > COOKIE_MAX_BYTES:
        return jsonify({"success": False, "error": "cookies.txt không được vượt quá 512 KB"}), 413
    try:
        parsed = parse_cookie_text(raw)
        if not parsed["authenticated"]:
            raise ValueError("Không tìm thấy cookie đăng nhập YouTube đang hoạt động")
        os.makedirs(DATA_DIR, exist_ok=True)
        temp_path = f"{COOKIE_FILE}.tmp"
        descriptor = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(parsed["content"])
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, COOKIE_FILE)
            os.chmod(COOKIE_FILE, 0o600)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        clear_youtube_session()
        last_error = None
        return jsonify({"success": True, "cookie": cookie_status()})
    except (OSError, ValueError) as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/entities")
def entities():
    try:
        rows = ha_get("/states")
        profiles = load_media_player_profiles(rows)
        result = []
        for row in rows if isinstance(rows, list) else []:
            entity_id = row.get("entity_id")
            if not valid_entity(entity_id):
                continue
            attributes = row.get("attributes") or {}
            profile = profiles.get(entity_id) or media_player_profile(
                entity_id,
                attributes,
                state=row.get("state"),
            )
            result.append(
                {
                    "entity_id": entity_id,
                    "name": profile.get("name") or attributes.get("friendly_name") or entity_id,
                    "state": row.get("state"),
                    "volume": attributes.get("volume_level"),
                    "kind": profile.get("kind", "media_player"),
                    "integration": profile.get("integration", ""),
                    "manufacturer": profile.get("manufacturer", ""),
                    "model": profile.get("model", ""),
                    "can_play_video": bool(profile.get("can_play_video")),
                    "is_airplay": bool(profile.get("is_airplay")),
                    "is_cast": bool(profile.get("is_cast")),
                    "supports_seek": bool(profile.get("supports_seek")),
                }
            )
        return jsonify(result)
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/search", methods=["POST"])
def search_api():
    global last_error
    data = request.get_json(silent=True) or {}
    try:
        offset = max(0, safe_int(data.get("offset"), 0))
        query = safe_text(data.get("query"), 160)
        media_kind = normalize_media_kind(data.get("media_kind") or data.get("mode"))
        results = search_youtube(query, offset, media_kind=media_kind)
        if query:
            record_search_query(query)
        last_error = None
        return jsonify(
            {
                "success": True,
                "results": results,
                "has_more": len(results) >= 20 and offset + len(results) < (
                    VIDEO_SEARCH_MAX_RESULTS if media_kind == "video" else SEARCH_MAX_RESULTS
                ),
                "media_kind": media_kind,
            }
        )
    except Exception as error:
        last_error = public_ydl_error(error)
        logger.error("yt-dlp search failed: %s", error)
        return jsonify({"success": False, "error": last_error}), 502


@app.route("/api/video/search", methods=["POST"])
def video_search_api():
    global last_error
    data = request.get_json(silent=True) or {}
    try:
        offset = max(0, safe_int(data.get("offset"), 0))
        query = safe_text(data.get("query"), 160)
        results = search_video_youtube(query, offset)
        if query:
            record_search_query(query)
        last_error = None
        return jsonify(
            {
                "success": True,
                "results": results,
                "has_more": len(results) >= 20 and offset + len(results) < VIDEO_SEARCH_MAX_RESULTS,
                "discovery": [dict(item) for item in VIDEO_DISCOVERY],
            }
        )
    except Exception as error:
        last_error = public_ydl_error(error)
        logger.error("yt-dlp video search failed: %s", error)
        return jsonify({"success": False, "error": last_error}), 502


@app.route("/api/resolve", methods=["POST"])
def resolve_api():
    data = request.get_json(silent=True) or {}
    try:
        resolver = resolve_video if normalize_media_kind(data.get("media_kind") or data.get("mode")) == "video" else resolve_track
        fast_audio = (
            resolver is resolve_track
            and data.get("fast") is True
            and safe_text(data.get("playback_target"), 24) == "browser"
        )
        resolved = resolver(data.get("url"), fast=fast_audio) if fast_audio else resolver(data.get("url"))
        token, entry = cache_resolved(resolved)
        return jsonify(
            {
                "success": True,
                "token": token,
                "media_url": relay_url(token, entry),
                "media_path": media_path(token, entry),
                "content_type": entry["content_type"],
                "track": entry["track"],
                "details": entry.get("details") or {},
                "strategy": entry.get("strategy"),
                "format_id": entry.get("format_id"),
                "resolve_ms": entry.get("resolve_ms", 0),
                "cache_hit": bool(entry.get("cache_hit")),
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/video/resolve", methods=["POST"])
def video_resolve_api():
    data = request.get_json(silent=True) or {}
    try:
        resolved = resolve_video(data.get("url"))
        token, entry = cache_resolved(resolved)
        return jsonify(
            {
                "success": True,
                "token": token,
                "media_path": media_path(token, entry),
                "media_url": relay_url(token, entry),
                "content_type": entry["content_type"],
                "track": entry["track"],
                "details": entry.get("details") or {},
                "strategy": entry.get("strategy"),
                "format_id": entry.get("format_id"),
                "resolve_ms": entry.get("resolve_ms", 0),
                "cache_hit": bool(entry.get("cache_hit")),
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/details", methods=["POST"])
def details_api():
    data = request.get_json(silent=True) or {}
    try:
        resolver = resolve_video if normalize_media_kind(data.get("media_kind") or data.get("mode")) == "video" else resolve_track
        resolved = resolver(data.get("url"))
        return jsonify(
            {
                "success": True,
                "track": resolved.get("track") or {},
                "details": resolved.get("details") or {},
                "strategy": resolved.get("strategy"),
                "format_id": resolved.get("format_id"),
                "resolve_ms": resolved.get("resolve_ms", 0),
                "cache_hit": bool(resolved.get("cache_hit")),
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


def parse_range_bounds(value, total=0):
    text = str(value or "").strip().lower()
    if not text.startswith("bytes=") or "," in text:
        return 0, None
    start_text, _, end_text = text[6:].strip().partition("-")
    if not start_text:
        try:
            suffix = int(end_text)
        except ValueError:
            return 0, None
        return (max(0, total - suffix) if total > 0 else 0), None
    try:
        start = max(0, int(start_text))
    except ValueError:
        start = 0
    try:
        end = int(end_text) if end_text else None
    except ValueError:
        end = None
    if end is not None and end < start:
        end = None
    return start, end


@app.route("/api/media/<token>/<path:filename>", methods=["GET", "HEAD", "OPTIONS"])
def media_stream(token, filename):
    entry = get_stream_entry(token)
    if not entry:
        return jsonify({"success": False, "error": "Stream đã hết hạn"}), 404

    if request.method == "OPTIONS":
        return Response(status=204)
    if request.method == "HEAD":
        head_response = media_head_response(entry)
        if head_response is not None:
            return head_response

    client_range = str(request.headers.get("Range") or "").strip()
    base_start, base_end = parse_range_bounds(client_range, safe_int(entry.get("content_length"), 0))

    def open_upstream(byte_start, byte_end, initial=False):
        nonlocal entry

        def request_headers(target):
            headers = dict(target.get("headers") or {})
            for name in ("Host", "Content-Length", "Connection", "Accept-Encoding"):
                headers.pop(name, None)
            if request.headers.get("Icy-MetaData"):
                headers["Icy-MetaData"] = request.headers["Icy-MetaData"]
            if request.method == "GET":
                if initial and client_range:
                    headers["Range"] = client_range
                else:
                    value = f"bytes={max(0, byte_start)}-"
                    if byte_end is not None:
                        value += str(byte_end)
                    headers["Range"] = value
            elif client_range:
                headers["Range"] = client_range
            return headers

        current = entry
        upstream = relay_session.request(
            request.method,
            current["stream_url"],
            headers=request_headers(current),
            stream=request.method == "GET",
            timeout=(10, 45),
            allow_redirects=True,
        )
        if upstream.status_code in {401, 403, 410}:
            upstream.close()
            entry = refresh_stream_entry(token, current)
            current = entry
            upstream = relay_session.request(
                request.method,
                current["stream_url"],
                headers=request_headers(current),
                stream=request.method == "GET",
                timeout=(10, 45),
                allow_redirects=True,
            )
        return upstream

    try:
        upstream = open_upstream(base_start, base_end, initial=True)
        if not valid_stream_url(upstream.url):
            upstream.close()
            return jsonify({"success": False, "error": "Redirect stream không hợp lệ"}), 502
        response_headers = {}
        for name in ("Accept-Ranges", "Content-Range", "Content-Length", "ETag", "Last-Modified"):
            if upstream.headers.get(name):
                response_headers[name] = upstream.headers[name]
        response_headers.setdefault("Accept-Ranges", "bytes")
        response_headers["Content-Type"] = upstream.headers.get("Content-Type") or cast_content_type(entry)
        response_headers["Cache-Control"] = "no-store"
        response_headers["Content-Disposition"] = "inline"
        response_headers["X-Accel-Buffering"] = "no"

        response_status = upstream.status_code
        if request.method == "GET" and not client_range and response_status == 206:
            # Client không yêu cầu Range: giữ ngữ nghĩa 200 cho trình phát, dù
            # kết nối upstream phía trên có dùng Range để tránh throttle.
            response_status = 200
            response_headers.pop("Content-Range", None)

        if request.method == "HEAD":
            upstream.close()
            return Response(status=response_status, headers=response_headers)

        def generate():
            nonlocal upstream
            marked_valid = entry.get("stream_validated", True)
            chunk_size = 32 * 1024 if cast_content_type(entry).startswith("audio/") else 256 * 1024
            sent = 0
            attempts = 0
            try:
                while True:
                    try:
                        for chunk in upstream.iter_content(chunk_size=chunk_size):
                            if license_manager and not license_manager.permits_use():
                                return
                            if not chunk:
                                continue
                            if not marked_valid:
                                entry["stream_validated"] = True
                                with state_lock:
                                    cached_entry = stream_cache.get(token)
                                    if cached_entry:
                                        cached_entry["stream_validated"] = True
                                cache_resolved_result(entry.get("source_url"), entry)
                                marked_valid = True
                            sent += len(chunk)
                            yield chunk
                        return
                    except (requests.RequestException, OSError) as error:
                        attempts += 1
                        with contextlib.suppress(Exception):
                            upstream.close()
                        if attempts > RELAY_RESUME_ATTEMPTS:
                            logger.warning("Media relay dừng sau %s byte: %s", sent, error)
                            return
                        logger.warning(
                            "Media relay đứt sau %s byte (%s); nối lại lần %s",
                            sent,
                            error,
                            attempts,
                        )
                        try:
                            upstream = open_upstream(base_start + sent, base_end)
                        except Exception as resume_error:
                            logger.error("Media relay không nối lại được: %s", resume_error)
                            return
            finally:
                with contextlib.suppress(Exception):
                    upstream.close()

        return Response(stream_with_context(generate()), status=response_status, headers=response_headers)
    except Exception as error:
        logger.error("Media relay failed: %s", error)
        return jsonify({"success": False, "error": "Không thể tải media stream"}), 502


@app.route("/api/cast", methods=["POST"])
def cast_api():
    data = request.get_json(silent=True) or {}
    token = str(data.get("token") or "")
    entity_id = data.get("entity_id")
    entry = get_stream_entry(token)
    if not entry:
        return jsonify({"success": False, "error": "Stream đã hết hạn"}), 404
    try:
        url = cast_entry(entity_id, token, entry)
        cast_info = active_cast_for(entity_id)
        session = None
        if isinstance(data.get("tracks"), list):
            session = adopt_playback_session(
                entity_id,
                data.get("tracks"),
                data.get("index"),
                data.get("repeat"),
                data.get("shuffle"),
                token,
                entry,
                data.get("source"),
                data.get("source_name"),
            )
        return jsonify(
            {
                "success": True,
                "media_url": url,
                "transport": cast_info.get("transport"),
                "content_type": cast_info.get("media_type") or cast_content_type(entry),
                "duration": cast_info.get("duration", 0),
                "session": session,
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/video/cast", methods=["POST"])
def video_cast_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị phát không hợp lệ"}), 400
    track = sanitize_track(data.get("track") or {"url": data.get("url"), "media_kind": "video"})
    if not track:
        return jsonify({"success": False, "error": "Video không hợp lệ"}), 400
    track["media_kind"] = "video"
    try:
        profile = entity_profile(entity_id) or entity_profile(entity_id, refresh=True)
        if playback_session_for(entity_id):
            stop_playback_session(entity_id, stop_player=False, remove=True)
        audio_fallback = bool(profile) and not profile.get("can_play_video", False)
        resolved = resolve_track(track["url"]) if audio_fallback else resolve_video(track["url"])
        token, entry = cache_resolved(resolved)
        media_url = cast_entry(entity_id, token, entry)
        effective_entry = get_stream_entry(token) or entry
        effective_track = {**track, **dict(effective_entry.get("track") or {})}
        effective_track["media_kind"] = "video"
        session = adopt_playback_session(
            entity_id,
            [effective_track],
            0,
            "off",
            False,
            token,
            effective_entry,
            "video",
            effective_track.get("title") or "YouTube Video",
        )
        return jsonify(
            {
                "success": True,
                "mode": "audio_fallback" if cast_content_type(effective_entry).startswith("audio/") else "video",
                "token": token,
                "media_path": media_path(token, effective_entry),
                "media_url": media_url,
                "content_type": cast_content_type(effective_entry),
                "track": effective_track,
                "device": profile,
                "session": session,
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502

@app.route("/api/playback/start", methods=["POST"])
def playback_start_api():
    data = request.get_json(silent=True) or {}
    try:
        session = start_playback_session(
            data.get("entity_id"),
            data.get("tracks"),
            data.get("index"),
            data.get("repeat"),
            data.get("shuffle"),
            data.get("source"),
            data.get("source_name"),
        )
        return jsonify({"success": True, "session": session})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502

@app.route("/api/playback/<entity_id>", methods=["GET", "DELETE"])
def playback_session_api(entity_id):
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị không hợp lệ"}), 400
    if request.method == "DELETE":
        try:
            stop_playback_session(entity_id, stop_player=True, remove=True)
            return jsonify({"success": True})
        except Exception as error:
            return jsonify({"success": False, "error": str(error)}), 502
    session = playback_session_for(entity_id)
    return jsonify({"success": True, "session": playback_session_public(session, include_tracks=True)})

@app.route("/api/playback/control", methods=["POST"])
def playback_control_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị không hợp lệ"}), 400
    try:
        action = data.get("action")
        if action == "next":
            session = advance_playback_session(entity_id, 1)
        elif action == "previous":
            session = advance_playback_session(entity_id, -1)
        elif action == "play":
            session = playback_play_current(entity_id)
        elif action == "stop":
            session = stop_playback_session(entity_id, stop_player=True)
        elif action == "mode":
            session = update_playback_mode(entity_id, data.get("repeat"), data.get("shuffle"))
        else:
            return jsonify({"success": False, "error": "Lệnh playback không hợp lệ"}), 400
        return jsonify({"success": True, "session": session})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/control", methods=["POST"])
def control_api():
    data = request.get_json(silent=True) or {}
    entity_id = data.get("entity_id")
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị không hợp lệ"}), 400
    action = data.get("action")
    services = {
        "play": "media_play",
        "pause": "media_pause",
        "stop": "media_stop",
        "next": "media_next_track",
        "previous": "media_previous_track",
    }
    try:
        session = playback_session_for(entity_id)
        if session and action in {"next", "previous"}:
            updated = advance_playback_session(entity_id, 1 if action == "next" else -1)
            return jsonify({"success": True, "session": updated})
        if session and action == "stop":
            updated = stop_playback_session(entity_id, stop_player=True)
            return jsonify({"success": True, "session": updated})
        if session and action == "play" and session.get("state") in {"stopped", "completed", "error"}:
            if session.get("state") == "completed":
                playback_update_session(entity_id, {"index": 0, "state": "idle", "stop_requested": False})
            updated = playback_play_current(entity_id)
            return jsonify({"success": True, "session": updated})
        if action == "volume":
            volume = safe_float(data.get("volume"), -1)
            if not 0 <= volume <= 1:
                raise ValueError("Âm lượng phải từ 0 đến 1")
            ha_service("volume_set", {"entity_id": entity_id, "volume_level": volume})
        elif action == "seek":
            position = safe_float(data.get("seek_position"), -1)
            if position < 0:
                raise ValueError("Vị trí tua không hợp lệ")
            ha_service("media_seek", {"entity_id": entity_id, "seek_position": position})
            current = active_cast_for(entity_id)
            if current:
                update_active_cast_state(
                    entity_id,
                    {
                        "position": position,
                        "position_updated_at": time.time(),
                        "expected_state": current.get("expected_state") or "playing",
                    },
                )
        elif action in services:
            ha_service(services[action], {"entity_id": entity_id})
            current = active_cast_for(entity_id)
            if current:
                if action == "stop":
                    clear_active_cast(entity_id)
                else:
                    updates = {
                        "position_updated_at": time.time(),
                        "expected_state": "playing" if action in {"play", "next", "previous"} else action,
                    }
                    if action == "pause":
                        updates["position"] = active_cast_position_locked(current)
                    update_active_cast_state(entity_id, updates)
        else:
            return jsonify({"success": False, "error": "Lệnh không hợp lệ"}), 400
        return jsonify({"success": True})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


@app.route("/api/state")
def state_api():
    entity_id = request.args.get("entity_id")
    if not valid_entity(entity_id):
        return jsonify({"success": False, "error": "Thiết bị không hợp lệ"}), 400
    try:
        row = ha_get(f"/states/{entity_id}")
        attributes = row.get("attributes") or {}
        player_state = str(row.get("state") or "unknown").lower()
        has_position = attributes.get("media_position") is not None
        position = max(0, safe_float(attributes.get("media_position"), 0))
        updated_at = attributes.get("media_position_updated_at")
        if updated_at and player_state == "playing":
            try:
                stamp = datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=timezone.utc)
                position += max(0, (datetime.now(timezone.utc) - stamp).total_seconds())
            except (TypeError, ValueError, OverflowError):
                pass
        duration = max(0, safe_float(attributes.get("media_duration"), 0))
        current_title = str(attributes.get("media_title") or attributes.get("title") or "").strip()
        active = active_cast_for(entity_id)
        estimated_position = active_cast_position_locked(active) if active else 0
        active_title = str(active.get("title") or "").strip()
        same_media = not current_title or not active_title or current_title.casefold() == active_title.casefold()
        if active and same_media:
            duration = duration or max(0, safe_float(active.get("duration"), 0))
            if not has_position and player_state in {"playing", "buffering", "paused"}:
                position = estimated_position
        if duration:
            position = min(position, duration)
        return jsonify(
            {
                "success": True,
                "state": player_state,
                "position": position,
                "duration": duration,
                "volume": attributes.get("volume_level"),
                "title": current_title,
                "media_content_id": attributes.get("media_content_id") or "",
                "supports_seek": bool(safe_int(attributes.get("supported_features"), 0) & 2),
                "transport": active.get("transport"),
                "playback_session": playback_session_public(playback_session_for(entity_id)),
            }
        )
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502


def fetch_playlist_entries(url, limit=PLAYLIST_IMPORT_MAX):
    options = ydl_options(
        {
            "extract_flat": "in_playlist",
            "noplaylist": False,
            "playlistend": max(1, min(safe_int(limit, PLAYLIST_IMPORT_MAX), PLAYLIST_IMPORT_MAX)),
            "skip_download": True,
        }
    )
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    if not isinstance(info, dict):
        raise RuntimeError("Không đọc được playlist")
    raw_entries = info.get("entries")
    if raw_entries is None:
        raw_entries = [info]
    tracks = []
    seen = set()
    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue
        video_id = safe_text(entry.get("id"), 32)
        web = str(entry.get("webpage_url") or entry.get("url") or "").strip()
        if not web or web == video_id:
            web = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""
        thumbnails = entry.get("thumbnails") if isinstance(entry.get("thumbnails"), list) else []
        thumbnail = entry.get("thumbnail") or (thumbnails[-1].get("url") if thumbnails else None)
        track = sanitize_track(
            {
                "id": video_id,
                "title": entry.get("title"),
                "url": web,
                "thumbnail": thumbnail,
                "duration": entry.get("duration") or 0,
                "channel": entry.get("channel") or entry.get("uploader"),
                "channel_url": entry.get("channel_url") or entry.get("uploader_url"),
                "view_count": entry.get("view_count") or 0,
                "upload_date": entry.get("upload_date") or "",
            }
        )
        if not track or track["url"] in seen:
            continue
        seen.add(track["url"])
        tracks.append(track)
        if len(tracks) >= PLAYLIST_IMPORT_MAX:
            break
    if not tracks:
        raise RuntimeError("Playlist không có bài hợp lệ")
    return tracks, safe_text(info.get("title"), 160)


@app.route("/api/playlists", methods=["GET", "POST"])
def playlists_api():
    global playlists
    if request.method == "POST":
        name = normalize_name((request.get_json(silent=True) or {}).get("name"))
        if not name:
            return jsonify({"success": False, "error": "Tên playlist không hợp lệ"}), 400
        with state_lock:
            playlists.setdefault(name, [])
            save_json(PLAYLIST_FILE, playlists)
    return jsonify(playlists)


@app.route("/api/playlists/<name>", methods=["DELETE"])
def playlist_delete(name):
    global playlists
    with state_lock:
        playlists.pop(name, None)
        save_json(PLAYLIST_FILE, playlists)
    return jsonify({"success": True})


@app.route("/api/playlists/export", methods=["GET"])
def playlists_export_api():
    with state_lock:
        snapshot = {
            name: [dict(track) for track in items]
            for name, items in playlists.items()
            if isinstance(items, list)
        }
    return jsonify({"success": True, "version": 1, "exported_at": now_iso(), "playlists": snapshot})


@app.route("/api/playlists/import", methods=["POST"])
def playlists_import_api():
    global playlists
    data = request.get_json(silent=True) or {}
    raw = data.get("playlists") if isinstance(data.get("playlists"), dict) else data
    incoming = sanitize_playlists(raw if isinstance(raw, dict) else {})
    if not incoming:
        return jsonify({"success": False, "error": "Dữ liệu playlist không hợp lệ"}), 400
    mode = str(data.get("mode") or "merge").strip().lower()
    added = 0
    with state_lock:
        if mode == "replace":
            playlists = {}
        for name, items in incoming.items():
            target = playlists.setdefault(name, [])
            existing = {item["url"] for item in target}
            for track in items:
                if track["url"] in existing:
                    continue
                target.append(track)
                existing.add(track["url"])
                added += 1
            playlists[name] = target[-1000:]
        save_json(PLAYLIST_FILE, playlists)
    return jsonify({"success": True, "added": added, "playlists": len(playlists)})


@app.route("/api/playlists/import-url", methods=["POST"])
def playlists_import_url_api():
    global playlists
    data = request.get_json(silent=True) or {}
    url = str(data.get("url") or "").strip()
    if not valid_youtube_url(url):
        return jsonify({"success": False, "error": "URL không hợp lệ"}), 400
    name = normalize_name(data.get("name"))
    try:
        tracks, title = fetch_playlist_entries(url, data.get("limit") or PLAYLIST_IMPORT_MAX)
    except Exception as error:
        return jsonify({"success": False, "error": public_ydl_error(error)}), 502
    playlist_name = name or normalize_name(title) or "Playlist nhập"
    with state_lock:
        target = playlists.setdefault(playlist_name, [])
        existing = {item["url"] for item in target}
        for track in tracks:
            if track["url"] in existing:
                continue
            target.append(track)
            existing.add(track["url"])
        playlists[playlist_name] = target[-1000:]
        save_json(PLAYLIST_FILE, playlists)
    return jsonify({"success": True, "name": playlist_name, "count": len(tracks), "tracks": tracks[:50]})


@app.route("/api/stats", methods=["GET"])
def stats_api():
    with state_lock:
        profiles = {
            profile_id: {
                "tracks": {
                    url: dict(stat)
                    for url, stat in (profile.get("tracks") or {}).items()
                    if isinstance(stat, dict)
                }
            }
            for profile_id, profile in listener_profiles.items()
            if isinstance(profile, dict)
        }
        thumbnails = {}
        for item in history:
            if isinstance(item, dict) and item.get("url") and item.get("thumbnail"):
                thumbnails[item["url"]] = item["thumbnail"]
        for items in playlists.values():
            if not isinstance(items, list):
                continue
            for item in items:
                if isinstance(item, dict) and item.get("url") and item.get("thumbnail"):
                    thumbnails.setdefault(item["url"], item["thumbnail"])
    aggregate = {}
    for profile in profiles.values():
        for url, stat in profile["tracks"].items():
            item = aggregate.setdefault(
                url,
                {
                    "url": url,
                    "title": stat.get("title"),
                    "channel": stat.get("channel"),
                    "thumbnail": thumbnails.get(url),
                    "plays": 0,
                    "likes": 0,
                    "dislikes": 0,
                    "skips": 0,
                    "last_played": "",
                },
            )
            item["plays"] += max(0, safe_int(stat.get("plays"), 0))
            item["likes"] += max(0, safe_int(stat.get("likes"), 0))
            item["dislikes"] += max(0, safe_int(stat.get("dislikes"), 0))
            item["skips"] += max(0, safe_int(stat.get("skips"), 0))
            if str(stat.get("last_played") or "") > str(item.get("last_played") or ""):
                item["last_played"] = stat.get("last_played")
    top_tracks = sorted(
        aggregate.values(),
        key=lambda item: (item["plays"], item["likes"]),
        reverse=True,
    )[:20]
    channels = {}
    for item in aggregate.values():
        channel = str(item.get("channel") or "").strip()
        if not channel:
            continue
        entry = channels.setdefault(channel, {"channel": channel, "plays": 0})
        entry["plays"] += item["plays"]
    top_channels = sorted(channels.values(), key=lambda item: item["plays"], reverse=True)[:10]
    return jsonify(
        {
            "success": True,
            "total_plays": sum(item["plays"] for item in aggregate.values()),
            "track_count": len(aggregate),
            "top_tracks": top_tracks,
            "top_channels": top_channels,
        }
    )


def lyrics_payload(item):
    if not isinstance(item, dict):
        return None
    return {
        "success": True,
        "found": True,
        "plain": safe_text(item.get("plainLyrics"), 20000),
        "synced": safe_text(item.get("syncedLyrics"), 20000),
        "track": safe_text(item.get("trackName"), 200),
        "artist": safe_text(item.get("artistName"), 200),
        "duration": max(0, safe_int(item.get("duration"), 0)),
    }


@app.route("/api/lyrics", methods=["POST"])
def lyrics_api():
    data = request.get_json(silent=True) or {}
    title = safe_text(data.get("title"), 200)
    artist = safe_text(data.get("artist") or data.get("channel"), 200)
    duration = max(0, safe_float(data.get("duration"), 0))
    if not title:
        return jsonify({"success": False, "error": "Thiếu tên bài"}), 400
    key = f"{title.casefold()}|{artist.casefold()}|{int(duration)}"
    now = time.time()
    with state_lock:
        cached = lyrics_cache.get(key)
        if cached and cached.get("expires_at", 0) > now:
            return jsonify(cached["payload"])
    headers = {"User-Agent": f"YouTubeProAddon/{APP_VERSION}"}
    payload = {"success": True, "found": False}
    try:
        params = {"track_name": title}
        if artist:
            params["artist_name"] = artist
        if duration:
            params["duration"] = str(int(round(duration)))
        response = requests.get(
            "https://lrclib.net/api/get",
            params=params,
            headers=headers,
            timeout=(4, 8),
        )
        if response.status_code == 404 and artist:
            search = requests.get(
                "https://lrclib.net/api/search",
                params={"q": f"{artist} {title}".strip()},
                headers=headers,
                timeout=(4, 8),
            )
            if search.ok:
                results = search.json()
                if isinstance(results, list) and results:
                    best = max(
                        results,
                        key=lambda item: (
                            bool(item.get("syncedLyrics")),
                            int(item.get("duration") or 0) == int(round(duration)),
                        ),
                    )
                    candidate = lyrics_payload(best)
                    if candidate:
                        payload = candidate
        elif response.ok:
            candidate = lyrics_payload(response.json())
            if candidate:
                payload = candidate
    except requests.RequestException as error:
        return jsonify({"success": False, "error": safe_text(error, 200)}), 502
    with state_lock:
        lyrics_cache[key] = {"payload": payload, "expires_at": now + LYRICS_TTL}
        if len(lyrics_cache) > LYRICS_CACHE_LIMIT:
            oldest = sorted(lyrics_cache, key=lambda k: lyrics_cache[k].get("expires_at", 0))
            for stale in oldest[: len(lyrics_cache) - LYRICS_CACHE_LIMIT]:
                lyrics_cache.pop(stale, None)
    return jsonify(payload)


def enforce_license_runtime():
    if not license_manager or license_manager.permits_use():
        return
    with state_lock:
        session_entities = list(playback_sessions)
        cast_entities = [entity_id for entity_id in active_casts if entity_id not in playback_sessions]
        stream_cache.clear()
        resolve_cache.clear()
    for entity_id in session_entities:
        try:
            stop_playback_session(entity_id, stop_player=True, remove=True)
        except Exception as error:
            logger.warning("Unable to stop unlicensed playback for %s: %s", entity_id, error)
    for entity_id in cast_entities:
        try:
            ha_service("media_stop", {"entity_id": entity_id})
        except Exception as error:
            logger.warning("Unable to stop unlicensed cast for %s: %s", entity_id, error)
        clear_active_cast(entity_id)


def license_validation_worker():
    while True:
        try:
            if license_manager.configured():
                license_manager.validate(force=False)
            enforce_license_runtime()
        except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
            logger.warning("License worker failed: %s", error)
        time.sleep(60)


@app.route("/api/playlists/<name>/items", methods=["POST"])
def playlist_add(name):
    track = sanitize_track(request.get_json(silent=True) or {})
    if not track:
        return jsonify({"success": False, "error": "Bài hát không hợp lệ"}), 400
    with state_lock:
        if name not in playlists:
            return jsonify({"success": False, "error": "Không tìm thấy playlist"}), 404
        if not any(item["url"] == track["url"] for item in playlists[name]):
            playlists[name].append(track)
            playlists[name] = playlists[name][-1000:]
            save_json(PLAYLIST_FILE, playlists)
    return jsonify({"success": True})


@app.route("/api/playlists/<name>/items/<int:index>", methods=["DELETE"])
def playlist_item_delete(name, index):
    with state_lock:
        if name in playlists and 0 <= index < len(playlists[name]):
            playlists[name].pop(index)
            save_json(PLAYLIST_FILE, playlists)
    return jsonify({"success": True})


@app.route("/api/queue", methods=["GET", "POST", "DELETE"])
def queue_api():
    global queue
    if request.method == "GET":
        return jsonify(queue)
    if request.method == "DELETE":
        with state_lock:
            queue = []
            save_json(QUEUE_FILE, queue)
        return jsonify({"success": True})
    track = sanitize_track(request.get_json(silent=True) or {})
    if not track:
        return jsonify({"success": False, "error": "Bài hát không hợp lệ"}), 400
    with state_lock:
        queue.append(track)
        queue = queue[-200:]
        save_json(QUEUE_FILE, queue)
    return jsonify({"success": True, "queue": queue})


@app.route("/api/queue/view", methods=["GET", "DELETE"])
def queue_view_api():
    entity_id = request.args.get("entity_id")
    if request.method == "DELETE":
        data = request.get_json(silent=True) or {}
        entity_id = data.get("entity_id") or entity_id
        try:
            return jsonify(queue_clear(entity_id))
        except ValueError as error:
            return jsonify({"success": False, "error": str(error)}), 400
    return jsonify({"success": True, **queue_view_payload(entity_id)})

@app.route("/api/queue/items", methods=["POST", "PATCH"])
def queue_items_api():
    data = request.get_json(silent=True) or {}
    try:
        if request.method == "PATCH":
            result = queue_reorder_items(
                data.get("from_index"),
                data.get("to_index"),
                data.get("entity_id"),
            )
        else:
            result = queue_enqueue_track(
                data.get("track") if isinstance(data.get("track"), dict) else data,
                data.get("entity_id"),
                data.get("position"),
            )
        return jsonify(result)
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        logger.error("Queue operation failed: %s", error)
        return jsonify({"success": False, "error": "Không thể cập nhật hàng chờ"}), 500

@app.route("/api/queue/items/<int:index>", methods=["DELETE"])
def queue_item_delete_api(index):
    try:
        return jsonify(queue_remove_item(index, request.args.get("entity_id")))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

@app.route("/api/queue/shuffle", methods=["POST"])
def queue_shuffle_api():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(queue_shuffle(data.get("entity_id")))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

@app.route("/api/queue/save", methods=["POST"])
def queue_save_api():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(save_queue_as_playlist(data.get("name"), data.get("entity_id")))
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

@app.route("/api/radio", methods=["POST"])
def radio_api():
    data = request.get_json(silent=True) or {}
    seed = data.get("seed") if isinstance(data.get("seed"), dict) else data.get("track")
    if not isinstance(seed, dict):
        seed = {
            "url": data.get("url"),
            "title": data.get("title"),
            "media_kind": data.get("media_kind"),
        }
    try:
        result = create_radio(
            seed,
            data.get("entity_id"),
            data.get("media_kind"),
            data.get("limit"),
            data.get("mode"),
            bool(data.get("start_if_missing")),
            data.get("exclude_urls"),
            data.get("profile_id"),
        )
        return jsonify(result)
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        logger.error("Radio generation failed: %s", error)
        return jsonify({"success": False, "error": public_ydl_error(error)}), 502

@app.route("/api/queue/<int:index>", methods=["DELETE"])
def queue_delete(index):
    with state_lock:
        if 0 <= index < len(queue):
            queue.pop(index)
            save_json(QUEUE_FILE, queue)
    return jsonify({"success": True})


@app.route("/api/history", methods=["GET", "POST", "DELETE"])
def history_api():
    global history
    if request.method == "GET":
        return jsonify(history)
    if request.method == "DELETE":
        with state_lock:
            history = []
            save_json(HISTORY_FILE, history)
        return jsonify({"success": True})
    track = sanitize_track(request.get_json(silent=True) or {})
    if not track:
        return jsonify({"success": False, "error": "Bài hát không hợp lệ"}), 400
    track["played_at"] = now_iso()
    with state_lock:
        history = [item for item in history if item.get("url") != track["url"]]
        history.append(track)
        history = history[-50:]
        save_json(HISTORY_FILE, history)
    try:
        record_listener_event(track, "play")
    except ValueError:
        pass
    return jsonify({"success": True})


@app.route("/api/sleep", methods=["GET", "POST", "DELETE"])
def sleep_api():
    global sleep_timer
    if request.method == "GET":
        current = dict(sleep_timer) if isinstance(sleep_timer, dict) else {"enabled": False}
        if current.get("enabled") and current.get("end_at"):
            current["remaining"] = max(0, int(datetime.fromisoformat(current["end_at"]).timestamp() - time.time()))
        return jsonify(current)
    if request.method == "DELETE":
        with state_lock:
            sleep_timer = {"enabled": False}
            save_json(SLEEP_FILE, sleep_timer)
        return jsonify({"success": True})
    data = request.get_json(silent=True) or {}
    try:
        minutes = int(data.get("minutes"))
    except (TypeError, ValueError):
        minutes = 0
    entity_id = data.get("entity_id")
    if not 1 <= minutes <= 720 or (entity_id != "browser" and not valid_entity(entity_id)):
        return jsonify({"success": False, "error": "Sleep timer không hợp lệ"}), 400
    return jsonify({"success": True, "sleep": set_sleep(minutes, entity_id)})


@app.route("/api/timers", methods=["GET", "POST"])
def timers_api():
    global timers
    if request.method == "GET":
        return jsonify(timers)
    timer = normalize_timer(request.get_json(silent=True) or {})
    if not timer:
        return jsonify({"success": False, "error": "Lịch phát không hợp lệ"}), 400
    if timer["type"] == "play" and timer["playlist_name"] not in playlists:
        return jsonify({"success": False, "error": "Playlist không tồn tại"}), 400
    with state_lock:
        old = next((item for item in timers if item.get("id") == timer["id"]), None)
        if old:
            timer["last_trigger_date"] = old.get("last_trigger_date")
        timers = [item for item in timers if item.get("id") != timer["id"]]
        timers.append(timer)
        timers = timers[-100:]
        save_json(TIMER_FILE, timers)
    return jsonify({"success": True, "timer": timer})


@app.route("/api/timers/<timer_id>", methods=["DELETE"])
def timer_delete(timer_id):
    global timers
    with state_lock:
        timers = [item for item in timers if item.get("id") != timer_id]
        save_json(TIMER_FILE, timers)
    return jsonify({"success": True})


@app.route("/api/backup", methods=["GET", "POST"])
def backup_api():
    global playlists, queue, history, search_history, timers, sleep_timer
    global playback_sessions, listener_profiles, active_listener_profile_id
    if request.method == "GET":
        return jsonify(
            {
                "version": APP_VERSION,
                "exported_at": now_iso(),
                "playlists": playlists,
                "queue": queue,
                "history": history,
                "search_history": search_history,
                "timers": timers,
                "sleep_timer": sleep_timer,
                "listener_preferences": {
                    "version": LISTENER_PROFILE_GENERATION,
                    "active_profile_id": active_listener_profile_id,
                    "profiles": listener_profiles,
                },
                "playback_sessions": {
                    entity_id: dict(session)
                    for entity_id, session in playback_sessions.items()
                },
            }
        )
    data = request.get_json(silent=True) or {}
    with state_lock:
        playlists = sanitize_playlists(data.get("playlists"))
        queue = [track for track in (sanitize_track(item) for item in safe_list(data.get("queue"), 200)) if track]
        history = [track for track in (sanitize_track(item) for item in safe_list(data.get("history"), 50)) if track]
        search_history = sanitize_search_history(data.get("search_history"))
        timers = [timer for timer in (normalize_timer(item) for item in safe_list(data.get("timers"), 100)) if timer]
        restored_sleep = data.get("sleep_timer")
        sleep_timer = restored_sleep if isinstance(restored_sleep, dict) else {"enabled": False}
        restored_sessions = {}
        raw_sessions = data.get("playback_sessions") if isinstance(data.get("playback_sessions"), dict) else {}
        for entity_id, raw in list(raw_sessions.items())[:50]:
            session = normalize_playback_session(raw)
            if session and session.get("entity_id") == entity_id:
                restored_sessions[entity_id] = session
        playback_sessions = restored_sessions
        save_json(PLAYLIST_FILE, playlists)
        save_json(QUEUE_FILE, queue)
        save_json(HISTORY_FILE, history)
        save_json(SEARCH_HISTORY_FILE, search_history)
        save_json(TIMER_FILE, timers)
        save_json(SLEEP_FILE, sleep_timer)
        if "listener_preferences" in data:
            listener_profiles, active_listener_profile_id = normalize_listener_profiles(
                data.get("listener_preferences")
            )
            persist_listener_profiles()
            invalidate_personal_mix_cache()
        persist_playback_sessions()
    return jsonify({"success": True})


os.makedirs(DATA_DIR, exist_ok=True)
integration_api_token()
license_manager = LicenseManager(
    DATA_DIR,
    APP_VERSION,
    addon_options,
    write_private_text,
    logger,
)
extractor_preferences = normalize_extractor_preferences(load_json(EXTRACTOR_PREF_FILE, {}))
cast_preferences = normalize_cast_preferences(load_json(CAST_PREF_FILE, {}))
raw_playback_sessions = load_json(PLAYBACK_FILE, {})
if isinstance(raw_playback_sessions, dict):
    for entity_id, raw_session in list(raw_playback_sessions.items())[:50]:
        session = normalize_playback_session(raw_session)
        if session and session.get("entity_id") == entity_id:
            if session.get("state") in {"resolving", "starting"}:
                session.update({"state": "stopped", "stop_requested": True})
            playback_sessions[entity_id] = session
playlists = sanitize_playlists(load_json(PLAYLIST_FILE, {}))
queue = [track for track in (sanitize_track(item) for item in safe_list(load_json(QUEUE_FILE, []), 200)) if track]
history = [track for track in (sanitize_track(item) for item in safe_list(load_json(HISTORY_FILE, []), 50)) if track]
search_history = sanitize_search_history(load_json(SEARCH_HISTORY_FILE, []))
sleep_timer = load_json(SLEEP_FILE, {"enabled": False})
timers = safe_list(load_json(TIMER_FILE, []), 100)
listener_profiles, active_listener_profile_id = normalize_listener_profiles(
    load_json(LISTENER_PROFILE_FILE, {})
)
persist_listener_profiles()
migrate_timers()
if os.getenv("YOUTUBE_PRO_DISABLE_WORKERS") != "1":
    threading.Thread(target=sleep_worker, daemon=True).start()
    threading.Thread(target=timer_worker, daemon=True).start()
    threading.Thread(target=ha_websocket_worker, daemon=True).start()
    threading.Thread(target=playback_poll_worker, daemon=True).start()
    threading.Thread(target=interruption_worker, daemon=True).start()
    threading.Thread(target=playback_watchdog_worker, daemon=True).start()
    threading.Thread(target=license_validation_worker, daemon=True).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, threaded=True)
