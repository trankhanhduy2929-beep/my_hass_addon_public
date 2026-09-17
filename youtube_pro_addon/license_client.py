import json
import os
import re
import secrets
import threading
import time
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import requests

LICENSE_KEY_PATTERN = re.compile(r"^YTP(?:-[23456789ABCDEFGHJKLMNPQRSTUVWXYZ]{5}){4}$")
TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{24,256}$")
REFRESH_SECONDS = 5 * 60
REGISTER_REFRESH_SECONDS = 20 * 60
DEFAULT_OFFLINE_GRACE_SECONDS = 72 * 60 * 60
MAX_OFFLINE_GRACE_SECONDS = 7 * 24 * 60 * 60
DEFAULT_LICENSE_API_URL = "https://youtube-pro-license-api.trankhanhduy2929.workers.dev"
DEFAULT_LICENSE_PORTAL_URL = "https://youtube-pro-license-portal.vercel.app"


class LicenseManager:
    def __init__(
        self,
        data_dir,
        app_version,
        options_loader,
        private_writer,
        logger,
        http_session=None,
        clock=None,
    ):
        self.data_dir = data_dir
        self.app_version = app_version
        self.options_loader = options_loader
        self.private_writer = private_writer
        self.logger = logger
        self.http = http_session or requests.Session()
        self.clock = clock or time.time
        self.installation_file = os.path.join(data_dir, "youtube_pro_license_installation_id_v400")
        self.installation_secret_file = os.path.join(data_dir, "youtube_pro_license_installation_secret_v400")
        self.activation_file = os.path.join(data_dir, "youtube_pro_license_activation_token_v400")
        self.activation_backup_file = os.path.join(data_dir, "youtube_pro_license_activation_token_v400.bak")
        self.state_file = os.path.join(data_dir, "youtube_pro_license_state_v400.json")
        self.lock = threading.RLock()
        self.validation_lock = threading.Lock()
        self.state_repair_pending = False
        self.state = self._load_state()
        if self.state_repair_pending:
            try:
                self._save_state()
            except OSError as error:
                self.logger.warning("Unable to persist repaired license state: %s", error)

    def _load_state(self):
        try:
            with open(self.state_file, "r", encoding="utf-8") as handle:
                value = json.load(handle)
                if not isinstance(value, dict):
                    return {}
                return self._repair_loaded_state(value)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def _timestamp(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            try:
                return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
            except (TypeError, ValueError):
                return None

    def _repair_loaded_state(self, value):
        state = dict(value)
        if not state.get("valid") or state.get("state") not in {"active", "offline_grace"}:
            return state
        last_success_at = self._timestamp(state.get("last_success_at"))
        if last_success_at is None:
            last_success_at = self._timestamp(state.get("last_checked_at"))
            if last_success_at is not None:
                state["last_success_at"] = last_success_at
                self.state_repair_pending = True
        if last_success_at is None:
            return state
        grace_until = self._timestamp(state.get("offline_grace_until"))
        maximum_grace_until = last_success_at + MAX_OFFLINE_GRACE_SECONDS
        if grace_until is None or not last_success_at <= grace_until <= maximum_grace_until:
            state["offline_grace_until"] = last_success_at + DEFAULT_OFFLINE_GRACE_SECONDS
            self.state_repair_pending = True
        return state

    def _save_state(self):
        os.makedirs(self.data_dir, exist_ok=True)
        temp_path = f"{self.state_file}.{secrets.token_hex(8)}.tmp"
        descriptor = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(self.state, handle, ensure_ascii=False, separators=(",", ":"))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.state_file)
            os.chmod(self.state_file, 0o600)
        except (TypeError, ValueError):
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _read_private_token(self, path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                value = handle.read(512).strip()
        except OSError:
            return ""
        if not TOKEN_PATTERN.fullmatch(value):
            return ""
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
        return value

    def installation_id(self):
        with self.lock:
            value = self._read_private_token(self.installation_file)
            if value:
                return value
            value = secrets.token_urlsafe(32)
            self.private_writer(self.installation_file, value + "\n")
            return value

    def installation_secret(self):
        with self.lock:
            value = self._read_private_token(self.installation_secret_file)
            if value:
                return value
            value = secrets.token_urlsafe(32)
            self.private_writer(self.installation_secret_file, value + "\n")
            return value

    def activation_token(self):
        with self.lock:
            token = self._read_private_token(self.activation_file)
            if token:
                if self._read_private_token(self.activation_backup_file) != token:
                    try:
                        self.private_writer(self.activation_backup_file, token + "\n")
                    except OSError as error:
                        self.logger.warning("Unable to save the license activation backup: %s", error)
                return token
            token = self._read_private_token(self.activation_backup_file)
            if token:
                try:
                    self.private_writer(self.activation_file, token + "\n")
                except OSError as error:
                    self.logger.warning("Unable to restore the license activation token: %s", error)
                return token
            return ""

    def options(self):
        value = self.options_loader()
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _service_url(env_name, default):
        value = str(os.getenv(env_name) or default).strip().rstrip("/")
        try:
            parsed = urlparse(value)
        except (TypeError, ValueError):
            return None
        allow_http = os.getenv("YOUTUBE_PRO_LICENSE_ALLOW_HTTP") == "1"
        if (
            parsed.scheme not in ({"https", "http"} if allow_http else {"https"})
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            return None
        return value

    def server_url(self):
        return self._service_url("YOUTUBE_PRO_LICENSE_API_URL", DEFAULT_LICENSE_API_URL)

    def portal_url(self):
        return self._service_url("YOUTUBE_PRO_LICENSE_PORTAL_URL", DEFAULT_LICENSE_PORTAL_URL)

    def enforcement_enabled(self):
        return True

    def configured(self):
        return bool(self.server_url())

    @staticmethod
    def normalize_key(value):
        compact = re.sub(r"[^A-Za-z0-9]", "", str(value or "")).upper()
        if not compact.startswith("YTP") or len(compact) != 23:
            return None
        normalized = "YTP-" + "-".join(compact[index:index + 5] for index in range(3, 23, 5))
        return normalized if LICENSE_KEY_PATTERN.fullmatch(normalized) else None

    @staticmethod
    def _parse_time(value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
        except (TypeError, ValueError):
            return None

    def _safe_portal_url(self, value):
        portal = self.portal_url()
        if not portal:
            return None
        try:
            expected = urlparse(portal)
            parsed = urlparse(str(value or ""))
            if parsed.scheme != expected.scheme or parsed.hostname != expected.hostname:
                return None
            if parsed.port != expected.port or parsed.username or parsed.password:
                return None
            return parsed.geturl()
        except (TypeError, ValueError):
            return None

    def _claim_token(self):
        token = str(self.state.get("claim_token") or "")
        if TOKEN_PATTERN.fullmatch(token):
            return token
        claim_url = self._safe_portal_url(self.state.get("claim_url"))
        if not claim_url:
            return ""
        return self._claim_token_from_url(claim_url)

    @staticmethod
    def _claim_token_from_url(claim_url):
        try:
            parsed = urlparse(claim_url)
            token = parse_qs(parsed.fragment or parsed.query).get("token", [""])[0]
        except (TypeError, ValueError):
            return ""
        return token if TOKEN_PATTERN.fullmatch(token) else ""

    def _offline_grace_available_locked(self, now=None):
        current = self.clock() if now is None else now
        grace_until = self._timestamp(self.state.get("offline_grace_until"))
        last_success_at = self._timestamp(self.state.get("last_success_at"))
        if grace_until is None or last_success_at is None:
            return False
        expiry = self._parse_time(self.state.get("expires_at"))
        return last_success_at >= 0 and current <= grace_until and (
            expiry is None or current < expiry
        )

    def _cached_status_usable_locked(self, status):
        if not status.get("valid"):
            return False
        return self._offline_grace_available_locked()

    def _public_status_locked(self):
        now = self.clock()
        expires_at = self.state.get("expires_at")
        expiry = self._parse_time(expires_at)
        valid = bool(self.state.get("valid")) and (expiry is None or expiry > now)
        current_state = str(self.state.get("state") or "unlicensed")
        if expiry is not None and expiry <= now:
            valid = False
            current_state = "expired"
        if valid and "last_success_at" in self.state and not self._offline_grace_available_locked(now):
            valid = False
            if current_state in {"active", "offline_grace"}:
                current_state = "server_unreachable"
        configured = self.configured()
        if not configured:
            current_state = "not_configured"
            valid = False
        return {
            "configured": configured,
            "enforcement": self.enforcement_enabled(),
            "valid": valid,
            "state": current_state,
            "code": self.state.get("code"),
            "plan_code": self.state.get("plan_code"),
            "plan_name": self.state.get("plan_name"),
            "key_prefix": self.state.get("key_prefix"),
            "expires_at": expires_at,
            "last_checked_at": self.state.get("last_checked_at"),
            "last_success_at": self.state.get("last_success_at"),
            "offline_grace_until": self.state.get("offline_grace_until"),
            "portal_url": self._safe_portal_url(self.state.get("portal_url")) or self.portal_url(),
            "claim_url": self._safe_portal_url(self.state.get("claim_url")),
            "claim_expires_at": self.state.get("claim_expires_at"),
            "installation_suffix": self.installation_id()[-8:],
            "error": self.state.get("error"),
        }

    def current_status(self):
        with self.lock:
            return self._public_status_locked()

    def integration_status(self):
        status = self.current_status()
        return {
            "valid": status["valid"],
            "state": status["state"],
            "code": status["code"],
            "plan_code": status["plan_code"],
            "expires_at": status["expires_at"],
        }

    def _update_from_valid_response(self, data, activation_token=None):
        now = self.clock()
        grace_seconds = max(
            0,
            min(int(data.get("offline_grace_seconds") or DEFAULT_OFFLINE_GRACE_SECONDS), MAX_OFFLINE_GRACE_SECONDS),
        )
        self.state.update(
            {
                "valid": True,
                "state": "active",
                "code": str(data.get("code") or "active"),
                "plan_code": data.get("plan_code"),
                "plan_name": data.get("plan_name"),
                "key_prefix": data.get("key_prefix"),
                "expires_at": data.get("expires_at"),
                "last_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "last_success_at": now,
                "offline_grace_until": now + grace_seconds,
                "next_check_at": now + max(300, min(int(data.get("refresh_after_seconds") or REFRESH_SECONDS), REFRESH_SECONDS)),
                "error": None,
            }
        )
        if activation_token:
            self.private_writer(self.activation_file, activation_token + "\n")
            try:
                self.private_writer(self.activation_backup_file, activation_token + "\n")
            except OSError as error:
                self.logger.warning("Unable to save the license activation backup: %s", error)
        for key in ("claim_url", "claim_token", "claim_expires_at", "claim_refresh_at", "next_claim_check_at"):
            self.state.pop(key, None)
        self._save_state()
        return self._public_status_locked()

    def _update_invalid_response(self, data):
        self.state.update(
            {
                "valid": False,
                "state": "invalid",
                "code": str(data.get("code") or "license_invalid"),
                "last_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "next_check_at": self.clock() + 15 * 60,
                "error": None,
            }
        )
        self._save_state()
        return self._public_status_locked()

    def _offline_status(self, error):
        now = self.clock()
        can_use_grace = self._offline_grace_available_locked(now)
        self.state.update(
            {
                "valid": can_use_grace,
                "state": "offline_grace" if can_use_grace else "server_unreachable",
                "last_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "next_check_at": now + 10 * 60,
                "error": str(error)[:240],
            }
        )
        self._save_state()
        return self._public_status_locked()

    def register_installation(self, force=False):
        with self.lock:
            server = self.server_url()
            if not server:
                return self._public_status_locked()
            now = self.clock()
            if not force and self.state.get("claim_url") and now < float(self.state.get("claim_refresh_at") or 0):
                return self._public_status_locked()
        try:
            response = self.http.post(
                f"{server}/api/installations/register",
                json={
                    "installation_id": self.installation_id(),
                    "installation_secret": self.installation_secret(),
                    "addon_version": self.app_version,
                },
                timeout=12,
            )
            data = response.json() if response.content else {}
            if response.status_code >= 400 or not data.get("ok"):
                raise RuntimeError(str(data.get("code") or f"HTTP {response.status_code}"))
            with self.lock:
                now = self.clock()
                expires_in = max(60, min(int(data.get("claim_expires_in") or 1800), 3600))
                self.state.update(
                    {
                        "valid": False,
                        "state": "unlicensed",
                        "code": "license_required",
                        "portal_url": self._safe_portal_url(data.get("portal_url")) or self.portal_url(),
                        "claim_url": self._safe_portal_url(data.get("claim_url")),
                        "claim_token": self._claim_token_from_url(str(data.get("claim_url") or "")),
                        "claim_expires_at": now + expires_in,
                        "claim_refresh_at": now + min(expires_in - 30, REGISTER_REFRESH_SECONDS),
                        "next_claim_check_at": now,
                        "last_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "next_check_at": now + REGISTER_REFRESH_SECONDS,
                        "error": None,
                    }
                )
                self._save_state()
                return self._public_status_locked()
        except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
            with self.lock:
                return self._offline_status(error)

    def complete_installation(self, force=False):
        with self.lock:
            server = self.server_url()
            claim_token = self._claim_token()
            if not server or not claim_token:
                return self._public_status_locked()
            if not force and self.clock() < float(self.state.get("next_claim_check_at") or 0):
                return self._public_status_locked()
        try:
            response = self.http.post(
                f"{server}/api/installations/complete",
                json={
                    "claim_token": claim_token,
                    "installation_id": self.installation_id(),
                    "installation_secret": self.installation_secret(),
                    "addon_version": self.app_version,
                },
                timeout=10,
            )
            data = response.json() if response.content else {}
            if response.status_code == 429 or response.status_code >= 500:
                raise RuntimeError(f"HTTP {response.status_code}")
            activation_token = str(data.get("activation_token") or "")
            if data.get("valid") and TOKEN_PATTERN.fullmatch(activation_token):
                with self.lock:
                    return self._update_from_valid_response(data, activation_token=activation_token)
            with self.lock:
                now = self.clock()
                code = str(data.get("code") or "activation_pending")
                if code == "claim_expired":
                    for key in ("claim_url", "claim_token", "claim_expires_at", "claim_refresh_at"):
                        self.state.pop(key, None)
                self.state.update(
                    {
                        "valid": False,
                        "state": str(data.get("state") or "waiting_activation"),
                        "code": code,
                        "last_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "next_claim_check_at": now + 1,
                        "error": None,
                    }
                )
                self._save_state()
                return self._public_status_locked()
        except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
            with self.lock:
                return self._offline_status(error)

    def activate(self, raw_key):
        key = self.normalize_key(raw_key)
        if not key:
            raise ValueError("License Key không đúng định dạng")
        server = self.server_url()
        if not server:
            raise ValueError("License Server tạm thời chưa sẵn sàng")
        response = self.http.post(
            f"{server}/api/licenses/activate",
            json={
                "license_key": key,
                "installation_id": self.installation_id(),
                "installation_secret": self.installation_secret(),
                "addon_version": self.app_version,
            },
            timeout=15,
        )
        data = response.json() if response.content else {}
        if response.status_code == 429 or response.status_code >= 500:
            raise RuntimeError("License server tạm thời không sẵn sàng")
        if not data.get("valid"):
            with self.lock:
                return self._update_invalid_response(data)
        activation_token = str(data.get("activation_token") or "")
        if not TOKEN_PATTERN.fullmatch(activation_token):
            raise RuntimeError("License server không trả activation token hợp lệ")
        with self.lock:
            return self._update_from_valid_response(data, activation_token=activation_token)

    def validate(self, force=False):
        if not self.validation_lock.acquire(blocking=False):
            with self.lock:
                return self._public_status_locked()
        try:
            return self._validate(force=force)
        finally:
            self.validation_lock.release()

    def _validate(self, force=False):
        token = self.activation_token()
        if not token:
            with self.lock:
                cached = self._public_status_locked()
                claim_token = self._claim_token()
                if self._cached_status_usable_locked(cached) and (not force or not claim_token):
                    return cached
            if claim_token:
                status = self.complete_installation(force=force)
                if status.get("valid") or status.get("code") != "claim_expired":
                    return status
            return self.register_installation(force=False)
        server = self.server_url()
        if not server:
            with self.lock:
                return self._public_status_locked()
        with self.lock:
            if not force and self.clock() < float(self.state.get("next_check_at") or 0):
                return self._public_status_locked()
        try:
            response = self.http.post(
                f"{server}/api/licenses/validate",
                json={
                    "activation_token": token,
                    "installation_id": self.installation_id(),
                    "installation_secret": self.installation_secret(),
                    "addon_version": self.app_version,
                },
                timeout=12,
            )
            data = response.json() if response.content else {}
            if response.status_code == 429 or response.status_code >= 500:
                raise RuntimeError(f"HTTP {response.status_code}")
            with self.lock:
                if data.get("valid"):
                    return self._update_from_valid_response(data)
                return self._update_invalid_response(data)
        except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
            with self.lock:
                return self._offline_status(error)

    def status(self, force=False):
        if not self.configured():
            return self.current_status()
        if not force:
            with self.lock:
                cached = self._public_status_locked()
                usable = self._cached_status_usable_locked(cached)
            if usable:
                return cached
        return self.validate(force=force)

    def deactivate(self):
        token = self.activation_token()
        server = self.server_url()
        if token and server:
            try:
                self.http.post(
                    f"{server}/api/licenses/deactivate",
                    json={
                        "activation_token": token,
                        "installation_id": self.installation_id(),
                        "installation_secret": self.installation_secret(),
                    },
                    timeout=8,
                )
            except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
                self.logger.warning("License deactivate remote call failed: %s", error)
        with self.lock:
            try:
                os.unlink(self.activation_file)
            except FileNotFoundError:
                pass
            try:
                os.unlink(self.activation_backup_file)
            except FileNotFoundError:
                pass
            self.state = {
                "valid": False,
                "state": "unlicensed",
                "code": "license_required",
                "portal_url": self.portal_url(),
                "next_check_at": 0,
            }
            self._save_state()
        return self.register_installation(force=True) if server else self.current_status()

    def permits_use(self):
        with self.lock:
            status = self._public_status_locked()
            if not status["valid"]:
                return False
            if "last_success_at" in self.state:
                return self._offline_grace_available_locked()
            return True

    def worker(self):
        while True:
            try:
                if self.configured():
                    self.validate(force=False)
            except (OSError, RuntimeError, TypeError, ValueError, requests.RequestException) as error:
                self.logger.warning("License worker failed: %s", error)
            time.sleep(60)
