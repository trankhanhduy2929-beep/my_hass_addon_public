const API_BASE = window.location.pathname.replace(/\/$/, '');
const SILENT_AUDIO = 'data:audio/wav;base64,UklGRnQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YVAAAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgA==';

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];

const elements = {
    appShell: $('.app-shell'),
    licenseGate: $('#licenseGate'),
    licenseGateStatus: $('#licenseGateStatus'),
    licenseGateDescription: $('#licenseGateDescription'),
    licenseGatePortalLink: $('#licenseGatePortalLink'),
    licenseGateForm: $('#licenseGateForm'),
    licenseGateKey: $('#licenseGateKey'),
    licenseGateRefresh: $('#licenseGateRefresh'),
    licenseGateInstallation: $('#licenseGateInstallation'),
    searchForm: $('#searchForm'),
    searchInput: $('#searchInput'),
    searchStatus: $('#searchStatus'),
    resultList: $('#resultList'),
    featuredSection: $('#featuredSection'),
    featuredResults: $('#featuredResults'),
    personalMixSection: $('#personalMixSection'),
    personalMixStatus: $('#personalMixStatus'),
    personalMixList: $('#personalMixList'),
    listenerProfileSelect: $('#listenerProfileSelect'),
    listenerProfileSummary: $('#listenerProfileSummary'),
    createListenerProfile: $('#createListenerProfile'),
    renameListenerProfile: $('#renameListenerProfile'),
    deleteListenerProfile: $('#deleteListenerProfile'),
    playPersonalMix: $('#playPersonalMix'),
    refreshPersonalMix: $('#refreshPersonalMix'),
    loadMore: $('#loadMore'),
    loadMoreSentinel: $('#loadMoreSentinel'),
    loadMoreLabel: $('#loadMoreLabel'),
    viewVideo: $('#viewVideo'),
    videoSearchForm: $('#videoSearchForm'),
    videoSearchInput: $('#videoSearchInput'),
    videoDiscovery: $('#videoDiscovery'),
    videoResults: $('#videoResults'),
    videoResultsTitle: $('#videoResultsTitle'),
    videoSearchStatus: $('#videoSearchStatus'),
    videoLoadMore: $('#videoLoadMore'),
    videoLoadMoreSentinel: $('#videoLoadMoreSentinel'),
    videoLoadMoreLabel: $('#videoLoadMoreLabel'),
    videoWatch: $('#videoWatch'),
    videoWatchStatus: $('#videoWatchStatus'),
    videoPlayer: $('#videoPlayer'),
    videoPlayerEmpty: $('#videoPlayerEmpty'),
    videoWatchTitle: $('#videoWatchTitle'),
    videoWatchChannel: $('#videoWatchChannel'),
    videoWatchViews: $('#videoWatchViews'),
    videoWatchDescription: $('#videoWatchDescription'),
    videoRelated: $('#videoRelated'),
    videoWatchPlay: $('#videoWatchPlay'),
    videoWatchQueue: $('#videoWatchQueue'),
    videoWatchNext: $('#videoWatchNext'),
    videoWatchRadio: $('#videoWatchRadio'),
    videoWatchOpen: $('#videoWatchOpen'),
    closeVideoWatch: $('#closeVideoWatch'),
    deviceSelect: $('#deviceSelect'),
    timerDevice: $('#timerDevice'),
    timerPlaylist: $('#timerPlaylist'),
    queueList: $('#queueList'),
    queueScope: $('#queueScope'),
    queueCurrent: $('#queueCurrent'),
    shuffleQueue: $('#shuffleQueue'),
    saveQueue: $('#saveQueue'),
    playlistTabs: $('#playlistTabs'),
    playlistToolbar: $('#playlistToolbar'),
    playlistTitle: $('#playlistTitle'),
    playlistItems: $('#playlistItems'),
    playlistImportUrl: $('#playlistImportUrl'),
    playlistImportButton: $('#playlistImportButton'),
    refreshStats: $('#refreshStats'),
    statsSummary: $('#statsSummary'),
    statsTracks: $('#statsTracks'),
    statsChannels: $('#statsChannels'),
    historyList: $('#historyList'),
    queueCount: $('#queueCount'),
    playlistCount: $('#playlistCount'),
    historyCount: $('#historyCount'),
    timerList: $('#timerList'),
    timerForm: $('#timerForm'),
    timerType: $('#timerType'),
    timerPlaylistWrap: $('#timerPlaylistWrap'),
    timerDurationWrap: $('#timerDurationWrap'),
    sleepStatus: $('#sleepStatus'),
    systemStatus: $('#systemStatus'),
    integrationToken: $('#integrationToken'),
    integrationTokenStatus: $('#integrationTokenStatus'),
    licensePanel: $('#licensePanel'),
    licenseStatus: $('#licenseStatus'),
    licenseDescription: $('#licenseDescription'),
    licensePortalLink: $('#licensePortalLink'),
    licenseForm: $('#licenseForm'),
    licenseKey: $('#licenseKey'),
    refreshLicense: $('#refreshLicense'),
    deactivateLicense: $('#deactivateLicense'),
    licenseInstallation: $('#licenseInstallation'),
    toggleIntegrationToken: $('#toggleIntegrationToken'),
    copyIntegrationToken: $('#copyIntegrationToken'),
    rotateIntegrationToken: $('#rotateIntegrationToken'),
    themeToggle: $('#themeToggle'),
    themeColor: $('meta[name="theme-color"]'),
    player: $('#player'),
    playerImage: $('#playerImage'),
    playerTitle: $('#playerTitle'),
    playerDevice: $('#playerDevice'),
    playerMessage: $('#playerMessage'),
    togglePlayer: $('#togglePlayer'),
    playerDetails: $('#playerDetails'),
    playerFeedback: $('#playerFeedback'),
    likeCurrent: $('#likeCurrent'),
    dislikeCurrent: $('#dislikeCurrent'),
    blockTrackCurrent: $('#blockTrackCurrent'),
    blockChannelCurrent: $('#blockChannelCurrent'),
    undoFeedback: $('#undoFeedback'),
    audio: $('#audioPlayer'),
    remoteControls: $('#remoteControls'),
    remoteSeek: $('#remoteSeek'),
    remoteVolume: $('#remoteVolume'),
    remoteProgress: $('#remoteProgress'),
    remoteElapsed: $('#remoteElapsed'),
    remoteDuration: $('#remoteDuration'),
    remoteProgressHint: $('#remoteProgressHint'),
    shuffleToggle: $('#shuffleToggle'),
    repeatToggle: $('#repeatToggle'),
    detailsDialog: $('#detailsDialog'),
    detailsTitle: $('#detailsTitle'),
    detailsImage: $('#detailsImage'),
    detailsChannel: $('#detailsChannel'),
    detailsStatus: $('#detailsStatus'),
    detailsDuration: $('#detailsDuration'),
    detailsViews: $('#detailsViews'),
    detailsLikes: $('#detailsLikes'),
    detailsDate: $('#detailsDate'),
    detailsDescription: $('#detailsDescription'),
    detailsLyrics: $('#detailsLyrics'),
    detailsLyricsWrap: $('#detailsLyricsWrap'),
    detailsOpenVideo: $('#detailsOpenVideo'),
    detailsPlay: $('#detailsPlay'),
    detailsNext: $('#detailsNext'),
    detailsRadio: $('#detailsRadio'),
    toast: $('#toast')
};

const state = {
    activeTab: 'home',
    results: [],
    offset: 0,
    query: '',
    devices: [],
    device: localStorage.getItem('youtubeProDevice') || 'browser',
    queue: [],
    queueScope: 'global',
    queueEntityId: null,
    queueCurrent: null,
    playlists: {},
    history: [],
    timers: [],
    current: null,
    token: null,
    selectedPlaylist: null,
    resolveId: 0,
    playingDevice: null,
    loadingUrl: null,
    playingUrl: null,
    hasMore: true,
    videoResults: [],
    videoOffset: 0,
    videoQuery: '',
    videoHasMore: true,
    videoLoading: false,
    videoLoaded: false,
    videoCurrent: null,
    videoResolveId: 0,
    videoModeActive: false,
    videoCastMode: '',
    videoDevice: null,
    prefetched: new Map(),
    remoteChains: new Map(),
    playbackLists: new Map(),
    playbackContext: null,
    detailsCache: new Map(),
    detailsTrack: null,
    detailsContext: null,
    detailsRequestId: 0,
    lyricsRequestId: 0,
    audioUnlocked: false,
    audioPriming: false,
    remotePollHandle: null,
    remotePollEntity: null,
    remoteStateBusy: false,
    remoteStateRequest: 0,
    remoteSeeking: false,
    remoteSeekRequest: 0,
    remotePosition: 0,
    remoteDuration: 0,
    remoteCanSeek: false,
    remoteState: 'idle',
    remoteSyncedAt: 0,
    remoteStartedAt: 0,
    mediaSessionUpdatedAt: 0,
    playbackSession: null,
    radioContext: null,
    radioLoading: false,
    radioRefillLoading: false,
    listenerPreferences: null,
    listenerPreferencesPromise: null,
    personalMix: [],
    personalMixLoading: false,
    personalMixLoaded: false,
    feedbackBusy: false,
    repeatMode: localStorage.getItem('youtubeProRepeatMode') || 'off',
    shuffle: localStorage.getItem('youtubeProShuffle') === '1',
    eventSource: null,
    playerCollapsed: localStorage.getItem('youtubeProPlayerCollapsed') == null
        ? window.matchMedia('(max-width: 820px)').matches
        : localStorage.getItem('youtubeProPlayerCollapsed') === '1',
    sleepHandle: null,
    lastSleepTrigger: localStorage.getItem('youtubeProLastSleepTrigger') || '',
    licensedRuntime: false,
    sleepPollInterval: null,
    progressInterval: null,
    devicePollInterval: null,
    licensePollTimeout: null,
    licenseFastPollUntil: 0,
    licenseReady: false
};

async function api(path, options = {}) {
    const response = await fetch(API_BASE + path, options);
    let data = null;
    try { data = await response.json(); } catch (_) { data = {}; }
    if (!response.ok || data?.success === false) {
        if (response.status === 402 && data?.license) renderLicense(data.license);
        const error = new Error(data?.error || `HTTP ${response.status}`);
        error.status = response.status;
        error.payload = data;
        throw error;
    }
    return data;
}

function toast(message) {
    elements.toast.textContent = message;
    elements.toast.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => elements.toast.classList.remove('show'), 2200);
}

function clearBrowserRadio() {
    const key = state.radioContext?.key;
    if (key) state.playbackLists.delete(key);
    if (state.playbackContext?.key === key) state.playbackContext = null;
    state.radioContext = null;
}

function setMessage(message) {
    elements.playerMessage.textContent = message;
}

function applyTheme(theme, persist = true) {
    const next = theme === 'light' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    document.documentElement.style.colorScheme = next;
    elements.themeColor.content = next === 'light' ? '#f6f6f6' : '#080808';
    elements.themeToggle.textContent = next === 'light' ? '☾' : '☀';
    elements.themeToggle.title = next === 'light' ? 'Bật giao diện tối' : 'Bật giao diện sáng';
    elements.themeToggle.setAttribute('aria-label', elements.themeToggle.title);
    elements.themeToggle.setAttribute('aria-pressed', String(next === 'light'));
    if (persist) localStorage.setItem('youtubeProTheme', next);
}

function updateMediaSessionMetadata(track = state.current) {
    if (!('mediaSession' in navigator) || typeof MediaMetadata === 'undefined' || !track) return;
    const artwork = safeImage(track.thumbnail);
    navigator.mediaSession.metadata = new MediaMetadata({
        title: track.title || 'YouTube Pro',
        artist: track.channel || 'YouTube',
        album: state.playingDevice === 'browser' ? 'Điện thoại này' : 'YouTube Pro',
        artwork: artwork ? [{ src: artwork }] : []
    });
}

function setMediaSessionPlayback(playbackState) {
    if (!('mediaSession' in navigator)) return;
    try { navigator.mediaSession.playbackState = playbackState; } catch (_) {}
}

function updateMediaSessionPosition(position, duration, playbackRate = 1, force = false) {
    if (!('mediaSession' in navigator) || typeof navigator.mediaSession.setPositionState !== 'function') return;
    const safeDuration = Number(duration || 0);
    if (!(safeDuration > 0)) return;
    const now = Date.now();
    if (!force && now - state.mediaSessionUpdatedAt < 950) return;
    const safePosition = Math.max(0, Math.min(Number(position || 0), safeDuration));
    const safeRate = Number(playbackRate) > 0 ? Number(playbackRate) : 1;
    try {
        navigator.mediaSession.setPositionState({ duration: safeDuration, playbackRate: safeRate, position: safePosition });
        state.mediaSessionUpdatedAt = now;
    } catch (_) {}
}

function mediaSessionSeekTarget(offset) {
    if (state.playingDevice === 'browser') {
        const media = state.videoModeActive ? elements.videoPlayer : elements.audio;
        const duration = Number(media.duration || state.current?.duration || 0);
        if (!duration) return;
        media.currentTime = Math.max(0, Math.min(media.currentTime + offset, duration));
        return;
    }
    const elapsed = state.remoteState === 'playing' && state.remoteSyncedAt
        ? Math.max(0, (Date.now() - state.remoteSyncedAt) / 1000)
        : 0;
    seekRemote(Math.max(0, state.remotePosition + elapsed + offset));
}

function setupMediaSession() {
    if (!('mediaSession' in navigator)) return;
    const handlers = {
        play: () => (state.playingDevice || state.device) === 'browser'
            ? (state.videoModeActive ? elements.videoPlayer : elements.audio).play().catch(() => null)
            : remoteControl('play'),
        pause: () => (state.playingDevice || state.device) === 'browser'
            ? (state.videoModeActive ? elements.videoPlayer : elements.audio).pause()
            : remoteControl('pause'),
        stop: () => (state.playingDevice || state.device) === 'browser'
            ? (state.videoModeActive ? stopVideoPlayback() : stopBrowserPlayback())
            : remoteControl('stop'),
        previoustrack: () => state.videoModeActive ? playVideoRelative(-1) : playRelative(-1),
        nexttrack: () => state.videoModeActive ? playVideoRelative(1) : playRelative(1),
        seekbackward: details => mediaSessionSeekTarget(-Number(details.seekOffset || 10)),
        seekforward: details => mediaSessionSeekTarget(Number(details.seekOffset || 10)),
        seekto: details => {
            const target = Number(details.seekTime || 0);
            if ((state.playingDevice || state.device) === 'browser') {
                (state.videoModeActive ? elements.videoPlayer : elements.audio).currentTime = target;
            }
            else seekRemote(target);
        }
    };
    for (const [action, handler] of Object.entries(handlers)) {
        try { navigator.mediaSession.setActionHandler(action, handler); } catch (_) {}
    }
}

function formatDuration(seconds) {
    const value = Number(seconds || 0);
    if (!value) return '';
    const minutes = Math.floor(value / 60);
    const remain = Math.floor(value % 60);
    return `${minutes}:${remain < 10 ? '0' : ''}${remain}`;
}

function formatClock(seconds) {
    const value = Math.max(0, Number(seconds) || 0);
    const total = Math.floor(value);
    const hours = Math.floor(total / 3600);
    const minutes = Math.floor((total % 3600) / 60);
    const remain = total % 60;
    if (hours) return `${hours}:${minutes < 10 ? '0' : ''}${minutes}:${remain < 10 ? '0' : ''}${remain}`;
    return `${minutes}:${remain < 10 ? '0' : ''}${remain}`;
}

function formatCount(value) {
    const count = Number(value || 0);
    return count > 0 ? new Intl.NumberFormat('vi-VN').format(count) : '—';
}

function formatUploadDate(value) {
    const raw = String(value || '').replace(/\D/g, '');
    if (raw.length < 8) return '—';
    return `${raw.slice(6, 8)}/${raw.slice(4, 6)}/${raw.slice(0, 4)}`;
}

function trackMeta(track, fallback = '') {
    const parts = [];
    if (track?.channel) parts.push(track.channel);
    const duration = formatDuration(track?.duration);
    if (duration) parts.push(duration);
    return parts.join(' · ') || fallback || 'YouTube Music';
}

function safeImage(url) {
    try {
        const parsed = new URL(String(url || ''));
        return parsed.protocol === 'https:' ? parsed.href : '';
    } catch (_) {
        return '';
    }
}

function safeYouTubeUrl(url) {
    try {
        const parsed = new URL(String(url || ''));
        const host = parsed.hostname.toLowerCase();
        return parsed.protocol === 'https:' && ['youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com', 'youtu.be'].includes(host)
            ? parsed.href
            : '';
    } catch (_) {
        return '';
    }
}

function listenerChannelKey(track) {
    const raw = String(track?.channel_url || track?.channel || track?.uploader || '').trim().toLowerCase();
    if (!raw) return '';
    if (raw.startsWith('http://') || raw.startsWith('https://')) {
        try {
            const parsed = new URL(raw);
            return `${parsed.hostname}${parsed.pathname}`.replace(/\/$/, '');
        } catch (_) {}
    }
    return raw.replace(/\s+/g, ' ');
}

function activeListenerProfile() {
    return state.listenerPreferences?.active_profile || null;
}

function listenerFeedbackFor(track) {
    const profile = activeListenerProfile();
    const url = track?.url || '';
    const channel = listenerChannelKey(track);
    return {
        liked: Boolean(url && profile?.liked_urls?.includes(url)),
        disliked: Boolean(url && profile?.disliked_urls?.includes(url)),
        blockedTrack: Boolean(url && profile?.blocked_tracks?.includes(url)),
        blockedChannel: Boolean(channel && profile?.blocked_channels?.includes(channel))
    };
}

function trackBlockedByPreferences(track) {
    const feedback = listenerFeedbackFor(track);
    return feedback.blockedTrack || feedback.blockedChannel;
}

function syncFeedbackButtons(container, track) {
    if (!container) return;
    const feedback = listenerFeedbackFor(track);
    const activeByAction = {
        like: feedback.liked,
        dislike: feedback.disliked,
        block_track: feedback.blockedTrack,
        block_channel: feedback.blockedChannel
    };
    container.querySelectorAll('[data-feedback-action]').forEach(button => {
        const action = button.dataset.feedbackAction;
        const active = Boolean(activeByAction[action]);
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
        button.disabled = state.feedbackBusy || !track?.url || (action === 'block_channel' && !listenerChannelKey(track));
    });
}

function syncFeedbackControls(track = state.videoModeActive ? state.videoCurrent : state.current) {
    syncFeedbackButtons(elements.playerFeedback, track);
    syncFeedbackButtons(elements.detailsDialog?.querySelector('[data-feedback-controls]'), state.detailsTrack);
    elements.undoFeedback?.classList.toggle('hidden', !activeListenerProfile()?.can_undo);
    elements.undoFeedback?.toggleAttribute('disabled', state.feedbackBusy);
}

function renderListenerPreferences(preferences) {
    if (!preferences?.active_profile) return;
    state.listenerPreferences = preferences;
    const profiles = Array.isArray(preferences.profiles) ? preferences.profiles : [];
    elements.listenerProfileSelect?.replaceChildren(...profiles.map(profile => new Option(profile.name || profile.id, profile.id)));
    if (elements.listenerProfileSelect) elements.listenerProfileSelect.value = preferences.active_profile_id || 'default';
    const profile = preferences.active_profile;
    if (elements.listenerProfileSummary) {
        elements.listenerProfileSummary.textContent = `${profile.plays || 0} lượt nghe · ${profile.liked_count || 0} thích · ${profile.blocked_track_count || 0} bài ẩn · lưu cục bộ`;
    }
    if (elements.deleteListenerProfile) elements.deleteListenerProfile.disabled = profile.id === 'default';
    syncFeedbackControls();
}

async function loadListenerPreferences() {
    if (state.listenerPreferencesPromise) return state.listenerPreferencesPromise;
    state.listenerPreferencesPromise = (async () => {
        try {
            const data = await api('/api/preferences', { cache: 'no-store' });
            renderListenerPreferences(data);
            return data;
        } catch (error) {
            if (elements.personalMixStatus) elements.personalMixStatus.textContent = 'Không đọc được hồ sơ nghe';
            return null;
        }
    })();
    try {
        return await state.listenerPreferencesPromise;
    } finally {
        state.listenerPreferencesPromise = null;
    }
}

async function updateListenerProfile(action, extra = {}) {
    const data = await api('/api/preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, ...extra })
    });
    renderListenerPreferences(data);
    state.personalMixLoaded = false;
    state.personalMix = [];
    return data;
}

async function switchListenerProfile() {
    const profileId = elements.listenerProfileSelect?.value;
    if (!profileId) return;
    try {
        await updateListenerProfile('switch', { profile_id: profileId });
        await loadPersonalMix({ refresh: false });
    } catch (error) {
        toast(error.message);
    }
}

async function createListenerProfile() {
    const name = prompt('Tên hồ sơ nghe mới');
    if (!name?.trim()) return;
    try {
        await updateListenerProfile('create', { name: name.trim() });
        toast('Đã tạo hồ sơ nghe');
        await loadPersonalMix({ refresh: true });
    } catch (error) {
        toast(error.message);
    }
}

async function renameListenerProfile() {
    const profile = activeListenerProfile();
    if (!profile) return;
    const name = prompt('Tên mới cho hồ sơ nghe', profile.name || '');
    if (!name?.trim() || name.trim() === profile.name) return;
    try {
        await updateListenerProfile('rename', { profile_id: profile.id, name: name.trim() });
        toast('Đã đổi tên hồ sơ');
    } catch (error) {
        toast(error.message);
    }
}

async function deleteListenerProfile() {
    const profile = activeListenerProfile();
    if (!profile || profile.id === 'default') return;
    if (!confirm(`Xóa hồ sơ “${profile.name}” và toàn bộ dữ liệu gu nghe?`)) return;
    try {
        await updateListenerProfile('delete', { profile_id: profile.id });
        toast('Đã xóa hồ sơ nghe');
        await loadPersonalMix({ refresh: true });
    } catch (error) {
        toast(error.message);
    }
}

function renderPersonalMix(tracks = state.personalMix) {
    const profileId = activeListenerProfile()?.id || 'default';
    renderTrackList(
        elements.personalMixList,
        tracks,
        track => ({ queue: true, favorite: true, meta: trackMeta(track, 'Mix cá nhân') }),
        'Hãy nghe hoặc thích vài bài để Mix cá nhân hiểu gu của bạn.',
        `personal-mix:${profileId}`
    );
    if (elements.personalMixStatus) {
        elements.personalMixStatus.textContent = tracks.length ? `${tracks.length} bài dành cho bạn` : 'Chưa đủ dữ liệu nghe';
    }
}

async function loadPersonalMix({ refresh = false, quiet = false } = {}) {
    if (state.personalMixLoading) return state.personalMix;
    state.personalMixLoading = true;
    elements.playPersonalMix?.toggleAttribute('disabled', true);
    elements.refreshPersonalMix?.toggleAttribute('disabled', true);
    if (!quiet && elements.personalMixStatus) elements.personalMixStatus.textContent = 'Đang phối Mix cá nhân…';
    if (!state.personalMix.length && elements.personalMixList) {
        elements.personalMixList.replaceChildren(emptyNode('Đang học từ lịch sử nghe cục bộ…'));
    }
    try {
        const profileId = activeListenerProfile()?.id || 'default';
        const data = await api('/api/personal-mix', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ profile_id: profileId, media_kind: 'audio', limit: 18, refresh })
        });
        if (data.preferences) renderListenerPreferences(data.preferences);
        state.personalMix = (data.tracks || []).filter(track => !trackBlockedByPreferences(track));
        state.personalMixLoaded = true;
        renderPersonalMix();
        prefetchTracks(state.personalMix.slice(0, 4), 80, 420);
        return state.personalMix;
    } catch (error) {
        if (!quiet) toast(`Không tải được Mix cá nhân: ${error.message}`);
        if (elements.personalMixStatus) elements.personalMixStatus.textContent = 'Chưa tạo được Mix';
        if (!state.personalMix.length && elements.personalMixList) {
            elements.personalMixList.replaceChildren(emptyNode('Chưa thể tạo Mix cá nhân lúc này.'));
        }
        return [];
    } finally {
        state.personalMixLoading = false;
        elements.playPersonalMix?.toggleAttribute('disabled', false);
        elements.refreshPersonalMix?.toggleAttribute('disabled', false);
    }
}

async function playPersonalMix() {
    const tracks = state.personalMixLoaded ? state.personalMix : await loadPersonalMix();
    if (!tracks.length) return toast('Mix cá nhân chưa có bài phù hợp');
    const key = `personal-mix:${activeListenerProfile()?.id || 'default'}`;
    state.playbackLists.set(key, tracks);
    await playTrack(tracks[0], { key, index: 0 });
}

async function sendListenerFeedback(action, track = state.videoModeActive ? state.videoCurrent : state.current) {
    if (!track?.url || state.feedbackBusy) return;
    state.feedbackBusy = true;
    syncFeedbackControls(track);
    try {
        const data = await api('/api/preferences/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action, track, profile_id: activeListenerProfile()?.id })
        });
        renderListenerPreferences(data.preferences);
        state.personalMixLoaded = false;
        state.personalMix = state.personalMix.filter(item => !trackBlockedByPreferences(item));
        renderPersonalMix();
        const labels = { like: 'Đã cập nhật lượt thích', dislike: 'Đã cập nhật gu nghe', block_track: 'Đã cập nhật danh sách ẩn bài', block_channel: 'Đã cập nhật danh sách ẩn kênh' };
        toast(labels[action] || 'Đã cập nhật phản hồi');
    } catch (error) {
        toast(error.message);
    } finally {
        state.feedbackBusy = false;
        syncFeedbackControls(track);
    }
}

async function undoListenerFeedback() {
    if (state.feedbackBusy) return;
    state.feedbackBusy = true;
    syncFeedbackControls();
    try {
        const data = await api('/api/preferences/undo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ profile_id: activeListenerProfile()?.id })
        });
        renderListenerPreferences(data.preferences);
        state.personalMixLoaded = false;
        toast('Đã hoàn tác phản hồi gần nhất');
    } catch (error) {
        toast(error.message);
    } finally {
        state.feedbackBusy = false;
        syncFeedbackControls();
    }
}

function emptyNode(message) {
    const node = document.createElement('div');
    node.className = 'empty';
    node.textContent = message;
    return node;
}

function actionButton(label, title, handler, danger = false, action = '') {
    const button = document.createElement('button');
    button.type = 'button';
    const icons = {
        'ⓘ': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 10h2v7h-2v-7Zm0-3h2v2h-2V7Zm1-5a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8Z"/></svg>',
        '+': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6V5Z"/></svg>',
        '⇥': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h2v14H5V5Zm4 2 9 5-9 5V7Z"/></svg>',
        '⌁': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h2v3H6V4Zm10 0h2v3h-2V4ZM4 9h16v2H4V9Zm2 4h12v7H6v-7Zm2 2v3h8v-3H8Z"/></svg>',
        '↑': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 5-7 7 1.4 1.4L11 8.8V20h2V8.8l4.6 4.6L19 12l-7-7Z"/></svg>',
        '↓': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 19 7-7-1.4-1.4L13 15.2V4h-2v11.2l-4.6-4.6L5 12l7 7Z"/></svg>',
        '☆': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.9L12 3.5Zm0 4.5-1.3 2.7-3 .4 2.2 2.1-.5 3 2.6-1.4 2.6 1.4-.5-3 2.2-2.1-3-.4L12 8Z"/></svg>',
        '×': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7.4 6 4.6 4.6L16.6 6 18 7.4 13.4 12l4.6 4.6-1.4 1.4-4.6-4.6L7.4 18 6 16.6l4.6-4.6L6 7.4 7.4 6Z"/></svg>'
    };
    button.innerHTML = icons[label] || label;
    button.title = title;
    button.setAttribute('aria-label', title);
    if (action) button.dataset.action = action;
    if (danger) button.classList.add('danger');
    button.addEventListener('click', event => {
        event.stopPropagation();
        handler();
    });
    return button;
}

function trackRow(track, options = {}) {
    const row = document.createElement('article');
    row.className = 'track-row';
    row.dataset.url = track.url || '';

    const artwork = document.createElement('div');
    artwork.className = 'track-artwork';
    const image = document.createElement('img');
    image.alt = '';
    image.loading = 'lazy';
    image.src = safeImage(track.thumbnail);
    artwork.append(image);

    const main = document.createElement('button');
    main.type = 'button';
    main.className = 'track-main';
    const title = document.createElement('strong');
    title.textContent = track.title || 'Không rõ tên';
    const meta = document.createElement('span');
    meta.textContent = options.meta || trackMeta(track);
    main.append(title, meta);
    const context = options.contextKey ? { key: options.contextKey, index: options.contextIndex } : null;
    const warmTrack = () => prefetchTrack(track);
    main.addEventListener('pointerdown', warmTrack, { passive: true });
    main.addEventListener('focus', warmTrack);
    main.addEventListener('click', () => playTrack(track, context));

    const actions = document.createElement('div');
    actions.className = 'track-actions';
    if (options.moveUp) actions.append(actionButton('↑', 'Đưa lên trên', options.moveUp, false, 'move-up'));
    if (options.moveDown) actions.append(actionButton('↓', 'Đưa xuống dưới', options.moveDown, false, 'move-down'));
    if (options.details !== false) actions.append(actionButton('ⓘ', 'Xem thông tin video', () => openDetails(track, context), false, 'details'));
    if (options.queue !== false) {
        actions.append(actionButton('⇥', 'Phát tiếp theo', () => addQueue(track, 'next'), false, 'queue-next'));
        actions.append(actionButton('+', 'Thêm cuối hàng chờ', () => addQueue(track, 'end'), false, 'queue-end'));
    }
    if (options.radio !== false) actions.append(actionButton('⌁', 'Tạo đài phát', () => startRadio(track), false, 'radio'));
    if (options.favorite !== false) actions.append(actionButton('☆', 'Thêm vào Yêu thích', () => addFavorite(track), false, 'favorite'));
    if (options.remove) actions.append(actionButton('×', 'Xóa', options.remove, true, 'remove'));

    row.append(artwork, main, actions);
    syncTrackRow(row);
    return row;
}

function albumCard(track, index) {
    const card = document.createElement('article');
    card.className = 'album-card';
    card.dataset.url = track.url || '';

    const artwork = document.createElement('div');
    artwork.className = 'album-artwork';
    const image = document.createElement('img');
    image.alt = '';
    image.loading = 'lazy';
    image.src = safeImage(track.thumbnail);
    const play = document.createElement('button');
    play.type = 'button';
    play.className = 'album-play';
    play.setAttribute('aria-label', `Phát ${track.title || 'bài hát'}`);
    play.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 5 11 7-11 7V5Z"/></svg>';
    artwork.append(image, play);

    const copy = document.createElement('div');
    copy.className = 'album-copy';
    const title = document.createElement('strong');
    title.textContent = track.title || 'Không rõ tên';
    const meta = document.createElement('span');
    meta.textContent = track.channel || formatDuration(track.duration) || 'YouTube Music';
    copy.append(title, meta);

    const context = { key: 'search', index };
    const warmTrack = () => prefetchTrack(track);
    play.addEventListener('pointerdown', warmTrack, { passive: true });
    play.addEventListener('click', () => playTrack(track, context));
    artwork.addEventListener('click', event => {
        if (!event.target.closest('button')) playTrack(track, context);
    });
    artwork.addEventListener('dblclick', () => playTrack(track, context));
    card.addEventListener('contextmenu', event => {
        event.preventDefault();
        openDetails(track, context);
    });
    card.append(artwork, copy);
    syncAlbumCard(card);
    return card;
}

function syncAlbumCard(card) {
    const url = card.dataset.url;
    card.classList.toggle('is-loading', Boolean(url && url === state.loadingUrl));
    card.classList.toggle('is-playing', Boolean(url && url === state.playingUrl));
}

function videoMeta(track) {
    const parts = [];
    if (track?.channel) parts.push(track.channel);
    if (track?.view_count) parts.push(`${formatCount(track.view_count)} lượt xem`);
    if (track?.duration) parts.push(formatDuration(track.duration));
    return parts.join(' · ') || 'YouTube Video';
}

function videoCard(track) {
    const card = document.createElement('article');
    card.className = 'video-card';
    card.dataset.url = track.url || '';
    const artwork = document.createElement('div');
    artwork.className = 'video-card-artwork';
    const image = document.createElement('img');
    image.loading = 'lazy';
    image.alt = '';
    image.src = safeImage(track.thumbnail);
    const duration = document.createElement('span');
    duration.className = 'video-duration';
    duration.textContent = formatDuration(track.duration) || (track.is_live ? 'LIVE' : '');
    duration.classList.toggle('hidden', !duration.textContent);
    const play = document.createElement('span');
    play.className = 'video-card-play';
    play.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 5 11 7-11 7V5Z"/></svg>';
    artwork.append(image, duration, play);
    const copy = document.createElement('div');
    copy.className = 'video-card-copy';
    const title = document.createElement('h3');
    title.textContent = track.title || 'Không rõ tên video';
    const meta = document.createElement('span');
    meta.textContent = videoMeta(track);
    const channel = document.createElement('small');
    channel.textContent = track.channel || 'YouTube';
    copy.append(title, meta, channel);
    card.append(artwork, copy);
    const open = () => openVideo(track);
    artwork.addEventListener('click', open);
    copy.addEventListener('click', open);
    card.addEventListener('contextmenu', event => {
        event.preventDefault();
        openVideo(track);
    });
    return card;
}

function renderVideoResults(tracks) {
    if (!elements.videoResults) return;
    elements.videoResults.replaceChildren();
    if (!tracks.length) {
        elements.videoResults.append(emptyNode('Chưa tìm thấy video phù hợp'));
        return;
    }
    elements.videoResults.append(...tracks.map(videoCard));
}

function renderVideoDiscovery(items) {
    if (!elements.videoDiscovery) return;
    elements.videoDiscovery.replaceChildren();
    (items || []).forEach(item => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = item.title || item.query;
        button.dataset.query = item.query || '';
        button.addEventListener('click', () => {
            elements.videoSearchInput.value = button.dataset.query;
            searchVideos(true);
        });
        elements.videoDiscovery.append(button);
    });
}

function updateVideoLoader() {
    const loading = state.videoLoading;
    elements.videoLoadMoreSentinel?.classList.toggle('hidden', !loading && !state.videoHasMore);
    elements.videoLoadMore?.classList.toggle('hidden', loading || !state.videoHasMore || !state.videoResults.length);
    if (elements.videoLoadMoreLabel) elements.videoLoadMoreLabel.textContent = loading ? 'Đang tải video...' : 'Cuộn xuống để tải thêm';
}

async function searchVideos(reset = true) {
    if (state.videoLoading) return;
    state.videoLoading = true;
    const query = elements.videoSearchInput.value.trim();
    if (reset) {
        state.videoOffset = 0;
        state.videoResults = [];
        state.videoHasMore = true;
        state.videoQuery = query;
        elements.videoResults?.replaceChildren(emptyNode('Đang tải video...'));
    }
    if (elements.videoSearchStatus) elements.videoSearchStatus.textContent = 'Đang tải...';
    updateVideoLoader();
    try {
        const data = await api('/api/video/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: state.videoQuery, offset: state.videoOffset })
        });
        const rows = data.results || [];
        const known = new Set(state.videoResults.map(item => item.url));
        const unique = rows.filter(item => item?.url && !known.has(item.url) && (known.add(item.url), true));
        state.videoResults = reset ? unique : state.videoResults.concat(unique);
        state.videoOffset += rows.length;
        state.videoHasMore = Boolean(data.has_more) && rows.length > 0;
        state.videoLoaded = true;
        renderVideoDiscovery(data.discovery || []);
        renderVideoResults(state.videoResults);
        if (elements.videoResultsTitle) elements.videoResultsTitle.textContent = state.videoQuery ? `Kết quả cho “${state.videoQuery}”` : 'Video nổi bật';
        if (elements.videoSearchStatus) elements.videoSearchStatus.textContent = `${state.videoResults.length} video${state.videoHasMore ? ' · kéo xuống để xem thêm' : ''}`;
    } catch (error) {
        state.videoHasMore = false;
        elements.videoResults?.replaceChildren(emptyNode(`Không tải được video: ${error.message}`));
        if (elements.videoSearchStatus) elements.videoSearchStatus.textContent = 'Tìm video thất bại';
    } finally {
        state.videoLoading = false;
        updateVideoLoader();
    }
}

function stopVideoLocal() {
    if (!elements.videoPlayer) return;
    try { elements.videoPlayer.pause(); } catch (_) {}
    elements.videoPlayer.removeAttribute('src');
    try { elements.videoPlayer.load(); } catch (_) {}
    elements.videoPlayer.classList.add('hidden');
    elements.videoPlayerEmpty?.classList.remove('hidden');
}

function stopVideoPlayback() {
    const device = state.videoDevice;
    stopVideoLocal();
    state.videoResolveId += 1;
    state.videoDevice = null;
    state.videoCastMode = '';
    state.videoCurrent = null;
    state.videoModeActive = false;
    if (state.playingDevice === device) state.playingDevice = null;
    if (state.current?.media_kind === 'video') state.current = null;
    elements.player.classList.add('hidden');
    document.body.classList.remove('player-visible');
    updatePlayerMode();
    if (device && device !== 'browser') stopRemotePlayback(device);
}

async function playVideoRelative(step) {
    const remoteEntity = activeRemoteEntity();
    if (
        remoteEntity
        && state.playbackSession?.entity_id === remoteEntity
        && state.videoModeActive
    ) {
        try {
            const data = await api('/api/playback/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    entity_id: remoteEntity,
                    action: step > 0 ? 'next' : 'previous'
                })
            });
            if (data.session) applyPlaybackSession(data.session);
        } catch (error) {
            toast(error.message);
        }
        return;
    }
    let currentIndex = state.videoResults.findIndex(item => item.url === state.videoCurrent?.url);
    if (currentIndex < 0 || !state.videoResults.length) return;
    let target = state.videoResults[currentIndex + step];
    if (!target && step > 0 && state.radioContext?.media_kind === 'video') {
        await refillBrowserRadio();
        currentIndex = state.videoResults.findIndex(item => item.url === state.videoCurrent?.url);
        target = state.videoResults[currentIndex + step];
    }
    if (target) openVideo(target);
}

function renderVideoWatch(track, status = 'Sẵn sàng') {
    if (!track || !elements.videoWatch) return;
    elements.videoWatchTitle.textContent = track.title || 'Không rõ tên video';
    elements.videoWatchChannel.textContent = track.channel || 'YouTube';
    elements.videoWatchViews.textContent = track.view_count ? `${formatCount(track.view_count)} lượt xem` : 'YouTube Video';
    elements.videoWatchDescription.textContent = track.description || 'Không có mô tả cho video này.';
    elements.videoWatchOpen.href = safeYouTubeUrl(track.url) || '#';
    elements.videoWatchStatus.textContent = status;
    renderVideoRelated(track);
    syncFeedbackControls(track);
}

function renderVideoRelated(track) {
    if (!elements.videoRelated) return;
    const related = state.videoResults.filter(item => item.url !== track?.url).slice(0, 5);
    elements.videoRelated.replaceChildren();
    related.forEach(item => {
        const button = document.createElement('button');
        button.type = 'button';
        const image = document.createElement('img');
        image.alt = '';
        image.loading = 'lazy';
        image.src = safeImage(item.thumbnail);
        const copy = document.createElement('span');
        const title = document.createElement('strong');
        title.textContent = item.title || 'Không rõ tên';
        const meta = document.createElement('small');
        meta.textContent = videoMeta(item);
        copy.append(title, meta);
        button.append(image, copy);
        button.addEventListener('click', () => openVideo(item));
        elements.videoRelated.append(button);
    });
}

async function playVideo(track) {
    if (!track?.url) return;
    const radioList = state.radioContext?.media_kind === 'video'
        ? state.playbackLists.get(state.radioContext.key)
        : null;
    if (!radioList || state.videoResults !== radioList) clearBrowserRadio();
    const requestId = ++state.videoResolveId;
    const targetDevice = state.device;
    const previousDevice = state.playingDevice;
    const previousVideoDevice = state.videoDevice;
    state.videoModeActive = true;
    stopVideoLocal();
    if (previousDevice && previousDevice !== 'browser') stopRemotePlayback(previousDevice);
    if (previousVideoDevice && previousVideoDevice !== 'browser' && previousVideoDevice !== previousDevice) {
        stopRemotePlayback(previousVideoDevice);
    }
    stopBrowserPlayback();
    elements.player.classList.add('hidden');
    document.body.classList.remove('player-visible');
    state.playingDevice = null;
    state.videoDevice = targetDevice;
    state.videoCastMode = '';
    renderVideoWatch(track, 'Đang chuẩn bị video...');
    elements.videoPlayerEmpty?.classList.remove('hidden');
    try {
        if (targetDevice === 'browser') {
            const data = await api('/api/video/resolve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: track.url })
            });
            if (requestId !== state.videoResolveId) return;
            state.videoCurrent = data.track || track;
            state.current = state.videoCurrent;
            state.playingDevice = 'browser';
            updateMediaSessionMetadata(state.videoCurrent);
            renderVideoWatch(state.videoCurrent, 'Đang phát trên thiết bị này');
            elements.videoPlayer.src = API_BASE + data.media_path;
            elements.videoPlayer.classList.remove('hidden');
            elements.videoPlayerEmpty?.classList.add('hidden');
            elements.videoPlayer.load();
            try {
                await elements.videoPlayer.play();
            } catch (_) {
                renderVideoWatch(state.videoCurrent, 'Video đã sẵn sàng — nhấn Play');
            }
        } else {
            const data = await api('/api/video/cast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ entity_id: targetDevice, track })
            });
            if (requestId !== state.videoResolveId) return;
            state.videoCurrent = data.track || track;
            state.videoCastMode = data.mode || 'video';
            state.playingDevice = targetDevice;
            state.current = state.videoCurrent;
            if (data.session) applyPlaybackSession(data.session);
            showCurrent(state.videoCurrent);
            resetRemoteProgress(state.videoCurrent.duration || 0);
            updatePlayerMode();
            if (data.mode === 'audio_fallback') {
                renderVideoWatch(state.videoCurrent, 'HomePod/AirPlay đang phát phần âm thanh');
            } else if (data.mode === 'native_youtube') {
                renderVideoWatch(state.videoCurrent, 'Đã mở YouTube trên Apple TV');
            } else {
                renderVideoWatch(state.videoCurrent, 'Đã truyền tới màn hình Cast');
            }
        }
    } catch (error) {
        if (requestId !== state.videoResolveId) return;
        renderVideoWatch(track, `Không phát được: ${error.message}`);
        toast(`Lỗi phát video: ${error.message}`);
    }
}

function openVideo(track) {
    if (!track?.url) return;
    state.videoCurrent = track;
    state.videoModeActive = true;
    elements.videoWatch?.classList.remove('hidden');
    renderVideoWatch(track);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    playVideo(track);
}

function renderFeaturedResults(tracks) {
    if (!elements.featuredSection || !elements.featuredResults) return;
    const featured = tracks.slice(0, 8);
    elements.featuredSection.classList.toggle('hidden', !featured.length);
    elements.featuredResults.replaceChildren(...featured.map(albumCard));
}

function syncTrackRow(row) {
    const url = row.dataset.url;
    row.classList.toggle('is-loading', Boolean(url && url === state.loadingUrl));
    row.classList.toggle('is-playing', Boolean(url && url === state.playingUrl));
    row.setAttribute('aria-busy', String(Boolean(url && url === state.loadingUrl)));
}

function updateTrackStates() {
    $$('.track-row').forEach(syncTrackRow);
    $$('.album-card').forEach(syncAlbumCard);
}

function renderTrackList(container, tracks, optionsFactory, emptyMessage, contextKey = null) {
    container.replaceChildren();
    if (contextKey) state.playbackLists.set(contextKey, tracks);
    if (!tracks.length) {
        container.append(emptyNode(emptyMessage));
        return;
    }
    tracks.forEach((track, index) => {
        const options = optionsFactory?.(track, index) || {};
        container.append(trackRow(track, { ...options, contextKey, contextIndex: index }));
    });
}

function appendTrackList(container, tracks, optionsFactory, startIndex = 0, contextKey = null, fullList = tracks) {
    if (contextKey) state.playbackLists.set(contextKey, fullList);
    tracks.forEach((track, index) => {
        const contextIndex = startIndex + index;
        const options = optionsFactory?.(track, contextIndex) || {};
        container.append(trackRow(track, { ...options, contextKey, contextIndex }));
    });
}

function selectTab(name) {
    const previous = state.activeTab;
    state.activeTab = name;
    $$('.view').forEach(view => view.classList.toggle('active', view.dataset.view === name));
    $$('.bottom-nav button').forEach(button => button.classList.toggle('active', button.dataset.tab === name));
    elements.searchInput.placeholder = name === 'video'
        ? 'Tìm video, kênh, chủ đề...'
        : 'Tìm bài hát, nghệ sĩ, album...';
    if (name === 'queue') loadQueue();
    if (name === 'library') loadLibrary();
    if (name === 'home') {
        setTimeout(maybeLoadMore, 120);
    }
    if (name === 'personal') {
        const preferencesReady = state.listenerPreferences
            ? Promise.resolve(state.listenerPreferences)
            : loadListenerPreferences();
        void preferencesReady.then(() => {
            if (state.activeTab === 'personal' && !state.personalMixLoaded && !state.personalMixLoading) {
                return loadPersonalMix();
            }
            return null;
        });
    }
    if (name === 'video') {
        if (!state.videoLoaded) searchVideos(true);
        else setTimeout(maybeLoadMoreVideos, 120);
    }
    if (previous === 'video' && name !== 'video' && state.videoDevice === 'browser') {
        try { elements.videoPlayer.pause(); } catch (_) {}
    }
    if (name === 'timer') {
        loadSleep();
        loadTimers();
        loadStatus();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function loadDevices() {
    const previousDevices = state.devices;
    try {
        state.devices = await api('/api/entities');
    } catch (error) {
        state.devices = previousDevices;
        if (!state.devices.length) toast(`Không đọc được loa: ${error.message}`);
    }
    elements.deviceSelect.replaceChildren(new Option('Điện thoại này', 'browser'));
    elements.timerDevice.replaceChildren();
    state.devices.forEach(device => {
        const prefix = device.kind === 'homepod'
            ? 'HomePod'
            : device.kind === 'apple_tv'
                ? 'Apple TV'
                : device.is_cast
                    ? 'Cast'
                    : device.is_airplay
                        ? 'AirPlay'
                        : 'Loa';
        const label = `${prefix} · ${device.name}`;
        const option = new Option(label, device.entity_id);
        option.disabled = ['unavailable', 'unknown'].includes(String(device.state || '').toLowerCase());
        elements.deviceSelect.add(option);
        elements.timerDevice.add(new Option(label, device.entity_id));
    });
    const validDevice = state.device === 'browser' || state.devices.some(device => device.entity_id === state.device);
    state.device = validDevice ? state.device : 'browser';
    elements.deviceSelect.value = state.device;
    updatePlayerMode();
}

function updatePlayerMode() {
    const activeDevice = state.playingDevice || state.device;
    const browser = activeDevice === 'browser';
    elements.audio.classList.toggle('hidden', !browser || state.videoModeActive);
    elements.remoteControls.classList.toggle('hidden', browser);
    elements.remoteProgress?.classList.toggle('hidden', browser);
    const device = state.devices.find(item => item.entity_id === activeDevice);
    elements.playerDevice.textContent = browser
        ? (state.videoModeActive ? 'Đang xem trên thiết bị này' : 'Điện thoại này')
        : (device?.name || activeDevice);
    updateMediaSessionMetadata(state.current);
    if (browser || !state.current || state.playingDevice !== activeDevice || state.loadingUrl) stopRemoteProgressPolling();
    else startRemoteProgressPolling(activeDevice);
}

function activeRemoteEntity() {
    const entityId = state.playingDevice && state.playingDevice !== 'browser'
        ? state.playingDevice
        : state.device;
    return entityId && entityId !== 'browser' ? entityId : null;
}

function resetRemoteProgress(duration = 0) {
    state.remoteStateRequest += 1;
    state.remoteStateBusy = false;
    state.remotePosition = 0;
    state.remoteDuration = Math.max(0, Number(duration) || 0);
    state.remoteCanSeek = false;
    state.remoteState = 'idle';
    state.remoteSyncedAt = 0;
    state.remoteStartedAt = Date.now();
    if (!elements.remoteSeek) return;
    elements.remoteSeek.min = '0';
    elements.remoteSeek.max = String(Math.max(1, state.remoteDuration));
    elements.remoteSeek.value = '0';
    elements.remoteSeek.disabled = true;
    elements.remoteElapsed.textContent = '0:00';
    elements.remoteDuration.textContent = state.remoteDuration ? formatClock(state.remoteDuration) : '—';
    elements.remoteProgressHint.textContent = state.remoteDuration
        ? 'Đang chờ loa báo vị trí phát...'
        : 'Loa chưa báo thời lượng';
}

function updateRemoteProgress(position, duration, keepSlider = false) {
    const nextDuration = Math.max(0, Number(duration) || state.remoteDuration || 0);
    const nextPosition = Math.max(0, Math.min(Number(position) || 0, nextDuration || Number.MAX_SAFE_INTEGER));
    state.remoteDuration = nextDuration;
    state.remotePosition = nextPosition;
    if (!elements.remoteSeek) return;
    elements.remoteSeek.max = String(Math.max(1, nextDuration || 1));
    elements.remoteSeek.disabled = nextDuration <= 0 || !state.remoteCanSeek;
    if (!keepSlider && !state.remoteSeeking) elements.remoteSeek.value = String(nextPosition);
    elements.remoteElapsed.textContent = formatClock(nextPosition);
    elements.remoteDuration.textContent = nextDuration ? formatClock(nextDuration) : '—';
    elements.remoteProgressHint.textContent = !nextDuration
        ? 'Loa chưa báo thời lượng'
        : (state.remoteCanSeek ? 'Kéo thanh để tua trên loa' : 'Loa này không hỗ trợ tua');
    updateMediaSessionPosition(nextPosition, nextDuration, state.remoteState === 'playing' ? 1 : 0, true);
}

function tickRemoteProgress() {
    if (
        state.remoteSeeking
        || state.remoteState !== 'playing'
        || !state.remoteSyncedAt
        || !activeRemoteEntity()
    ) return;
    const elapsed = Math.max(0, (Date.now() - state.remoteSyncedAt) / 1000);
    const position = state.remotePosition + elapsed;
    const limited = state.remoteDuration ? Math.min(position, state.remoteDuration) : position;
    elements.remoteElapsed.textContent = formatClock(limited);
    if (state.remoteDuration && !elements.remoteSeek.disabled) {
        elements.remoteSeek.value = String(limited);
    }
    highlightLyrics(limited);
    updateMediaSessionPosition(limited, state.remoteDuration, 1);
}

function stopRemoteProgressPolling() {
    if (state.remotePollHandle) {
        clearTimeout(state.remotePollHandle);
        state.remotePollHandle = null;
    }
    state.remoteStateRequest += 1;
    state.remoteStateBusy = false;
    state.remotePollEntity = null;
    state.remoteSeeking = false;
}

function scheduleRemoteStatePoll(delay = 0) {
    if (state.remotePollHandle) clearTimeout(state.remotePollHandle);
    const entityId = state.playingDevice && state.playingDevice !== 'browser' ? state.playingDevice : null;
    if (!entityId) {
        state.remotePollHandle = null;
        return;
    }
    state.remotePollHandle = setTimeout(async () => {
        state.remotePollHandle = null;
        await pollRemoteState(entityId);
        if (state.playingDevice === entityId) {
            const interval = state.remoteState === 'playing' || state.remoteState === 'buffering' ? 1400 : 2600;
            scheduleRemoteStatePoll(interval);
        }
    }, delay);
}

async function pollRemoteState(entityId = activeRemoteEntity()) {
    if (!entityId || state.remoteStateBusy || state.playingDevice !== entityId) return;
    const requestId = ++state.remoteStateRequest;
    state.remoteStateBusy = true;
    try {
        const data = await api(`/api/state?entity_id=${encodeURIComponent(entityId)}`);
        if (requestId !== state.remoteStateRequest || state.playingDevice !== entityId) return;
        if (data.playback_session) applyPlaybackSession(data.playback_session);
        const fallbackDuration = Number(state.current?.duration || 0);
        const duration = Number(data.duration || 0) || fallbackDuration;
        const position = Number(data.position || 0);
        state.remoteState = String(data.state || 'unknown').toLowerCase();
        state.remoteCanSeek = Boolean(data.supports_seek);
        if (data.volume != null && document.activeElement !== elements.remoteVolume) {
            elements.remoteVolume.value = String(data.volume);
        }
        state.remoteSyncedAt = Date.now();
        updateRemoteProgress(position, duration);
        if (state.remoteState === 'playing') {
            setMediaSessionPlayback('playing');
            setMessage('Đang phát trên loa');
        } else if (state.remoteState === 'buffering') {
            setMediaSessionPlayback('playing');
            setMessage('Loa đang tải audio...');
        } else if (state.remoteState === 'paused') {
            setMediaSessionPlayback('paused');
            setMessage('Đang tạm dừng trên loa');
        } else if (state.remoteState === 'idle' || state.remoteState === 'off') {
            setMediaSessionPlayback('none');
            setMessage(Date.now() - state.remoteStartedAt < 5000
                ? 'Loa đang kết nối audio...'
                : 'Loa đã dừng hoặc chưa nhận audio');
        }
    } catch (_) {
        if (requestId === state.remoteStateRequest && state.playingDevice === entityId) {
            elements.remoteProgressHint.textContent = 'Chưa đọc được trạng thái loa';
        }
    } finally {
        if (requestId === state.remoteStateRequest) state.remoteStateBusy = false;
    }
}

function startRemoteProgressPolling(entityId = activeRemoteEntity()) {
    if (!entityId || entityId === 'browser') return;
    if (state.remotePollEntity === entityId && (state.remotePollHandle || state.remoteStateBusy)) return;
    stopRemoteProgressPolling();
    state.remotePollEntity = entityId;
    resetRemoteProgress(state.current?.duration || 0);
    scheduleRemoteStatePoll(320);
}

async function seekRemote(value) {
    const entityId = activeRemoteEntity();
    const position = Math.max(0, Number(value) || 0);
    if (!entityId || !state.remoteDuration || !state.remoteCanSeek) return;
    const requestId = ++state.remoteSeekRequest;
    state.remoteStateRequest += 1;
    state.remoteStateBusy = false;
    state.remoteSeeking = true;
    updateRemoteProgress(position, state.remoteDuration, true);
    try {
        await enqueueRemoteCommand(entityId, () => remoteControlRequest(entityId, 'seek', {
            seek_position: position
        }));
        if (requestId === state.remoteSeekRequest) {
            state.remoteSeeking = false;
            state.remotePosition = position;
            state.remoteSyncedAt = Date.now();
            scheduleRemoteStatePoll(120);
        }
    } catch (error) {
        if (requestId === state.remoteSeekRequest) {
            state.remoteSeeking = false;
            toast(`Không tua được trên loa: ${error.message}`);
            scheduleRemoteStatePoll(120);
        }
    }
}

function stopBrowserPlayback() {
    state.audioPriming = true;
    try { elements.audio.pause(); } catch (_) {}
    elements.audio.removeAttribute('src');
    try { elements.audio.load(); } catch (_) {}
    setMediaSessionPlayback('none');
}

function unlockBrowserAudio(device = state.device) {
    if (device !== 'browser' || state.audioUnlocked) return;
    state.audioUnlocked = true;
    state.audioPriming = true;
    elements.audio.src = SILENT_AUDIO;
    elements.audio.load();
    try {
        const pending = elements.audio.play();
        if (pending?.catch) pending.catch(() => {
            if (state.audioPriming) state.audioUnlocked = false;
        });
    } catch (_) {
        state.audioUnlocked = false;
    }
}

function enqueueRemoteCommand(entityId, command) {
    const previous = state.remoteChains.get(entityId);
    const invoke = () => {
        try { return Promise.resolve(command()); }
        catch (error) { return Promise.reject(error); }
    };
    const queued = previous ? previous.catch(() => null).then(invoke) : invoke();
    let tail = null;
    tail = queued.catch(() => null).finally(() => {
        if (state.remoteChains.get(entityId) === tail) state.remoteChains.delete(entityId);
    });
    state.remoteChains.set(entityId, tail);
    return queued;
}

function remoteControlRequest(entityId, action, extra = {}) {
    return api('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entity_id: entityId, action, ...extra })
    });
}

function stopRemotePlayback(entityId) {
    if (!entityId || entityId === 'browser') return Promise.resolve();
    const hadPendingCommand = state.remoteChains.has(entityId);
    const immediate = remoteControlRequest(entityId, 'stop').catch(() => null);
    if (!hadPendingCommand) {
        let tail = null;
        tail = immediate.finally(() => {
            if (state.remoteChains.get(entityId) === tail) state.remoteChains.delete(entityId);
        });
        state.remoteChains.set(entityId, tail);
        return immediate;
    }
    return enqueueRemoteCommand(entityId, () => immediate.then(() => remoteControlRequest(entityId, 'stop'))).catch(() => null);
}

function stopPlaybackImmediately(device = state.playingDevice) {
    stopBrowserPlayback();
    state.playingUrl = null;
    updateTrackStates();
    if (!device || device === 'browser') return Promise.resolve();
    return stopRemotePlayback(device);
}

function setPlayerCollapsed(collapsed, persist = true) {
    state.playerCollapsed = Boolean(collapsed);
    elements.player.classList.toggle('collapsed', state.playerCollapsed);
    document.body.classList.toggle('player-collapsed', state.playerCollapsed);
    elements.togglePlayer.textContent = state.playerCollapsed ? '⌃' : '⌄';
    elements.togglePlayer.setAttribute('aria-expanded', String(!state.playerCollapsed));
    elements.togglePlayer.setAttribute('aria-label', state.playerCollapsed ? 'Mở trình phát' : 'Thu gọn trình phát');
    if (persist) localStorage.setItem('youtubeProPlayerCollapsed', state.playerCollapsed ? '1' : '0');
}

function updateSearchLoader() {
    const active = state.hasMore && state.results.length > 0;
    elements.loadMoreSentinel.classList.toggle('hidden', !active);
    elements.loadMoreSentinel.classList.toggle('loading', Boolean(search.loading));
    elements.loadMoreLabel.textContent = search.loading ? 'Đang tải thêm bài hát...' : 'Cuộn xuống để tải thêm';
    elements.loadMore.classList.toggle('hidden', Boolean(search.observer) || !active || search.loading);
}

function maybeLoadMore() {
    if (search.loading || !state.hasMore || !state.results.length || !$('#viewHome').classList.contains('active')) return;
    const top = elements.loadMoreSentinel.getBoundingClientRect().top;
    if (top <= window.innerHeight + 650) setTimeout(() => search(false), 60);
}

function maybeLoadMoreVideos() {
    if (state.videoLoading || !state.videoHasMore || !state.videoResults.length || state.activeTab !== 'video') return;
    const top = elements.videoLoadMoreSentinel?.getBoundingClientRect().top;
    if (top != null && top <= window.innerHeight + 700) setTimeout(() => searchVideos(false), 60);
}

function setupInfiniteScroll() {
    if (!('IntersectionObserver' in window)) {
        updateSearchLoader();
        updateVideoLoader();
        return;
    }
    search.observer = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) maybeLoadMore();
    }, { rootMargin: '650px 0px' });
    search.observer.observe(elements.loadMoreSentinel);
    if (elements.videoLoadMoreSentinel) {
        search.videoObserver = new IntersectionObserver(entries => {
            if (entries.some(entry => entry.isIntersecting)) maybeLoadMoreVideos();
        }, { rootMargin: '700px 0px' });
        search.videoObserver.observe(elements.videoLoadMoreSentinel);
    }
}

function rememberDetails(url, data) {
    const details = data?.details;
    if (!url || !details || !Object.keys(details).length) return;
    state.detailsCache.delete(url);
    state.detailsCache.set(url, { ...details, strategy: data.strategy, format_id: data.format_id });
    while (state.detailsCache.size > 24) state.detailsCache.delete(state.detailsCache.keys().next().value);
}

function resolveCacheKey(url, playbackTarget = state.device === 'browser' ? 'browser' : 'remote') {
    return `${playbackTarget}:${url}`;
}

function getResolveEntry(url, playbackTarget = state.device === 'browser' ? 'browser' : 'remote') {
    const cacheKey = resolveCacheKey(url, playbackTarget);
    const entry = state.prefetched.get(cacheKey);
    if (!entry) return null;
    if (Date.now() - entry.createdAt > 30 * 60 * 1000) {
        state.prefetched.delete(cacheKey);
        return null;
    }
    state.prefetched.delete(cacheKey);
    state.prefetched.set(cacheKey, entry);
    return entry;
}

function startResolve(track) {
    if (!track?.url) return Promise.reject(new Error('Bài hát không hợp lệ'));
    const playbackTarget = state.device === 'browser' ? 'browser' : 'remote';
    const cacheKey = resolveCacheKey(track.url, playbackTarget);
    const existing = getResolveEntry(track.url, playbackTarget);
    if (existing) return existing.promise;
    const entry = { createdAt: Date.now(), promise: null };
    const fastAudio = playbackTarget === 'browser';
    entry.promise = api('/api/resolve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            url: track.url,
            fast: fastAudio,
            playback_target: fastAudio ? 'browser' : 'remote'
        })
    }).then(data => {
        rememberDetails(track.url, data);
        return data;
    }).catch(error => {
        if (state.prefetched.get(cacheKey) === entry) state.prefetched.delete(cacheKey);
        throw error;
    });
    state.prefetched.set(cacheKey, entry);
    while (state.prefetched.size > 10) state.prefetched.delete(state.prefetched.keys().next().value);
    return entry.promise;
}

function prefetchTrack(track) {
    if (!track?.url) return Promise.resolve(null);
    return startResolve(track).catch(() => null);
}

function schedulePrefetch(track, delay = 220) {
    if (!track) return;
    setTimeout(() => prefetchTrack(track), delay);
}

function prefetchTracks(tracks, initialDelay = 100, stepDelay = 220) {
    const seen = new Set();
    tracks.filter(track => {
        if (!track?.url || seen.has(track.url)) return false;
        seen.add(track.url);
        return true;
    }).forEach((track, index) => schedulePrefetch(track, initialDelay + index * stepDelay));
}

async function resolveTrackData(track) {
    return startResolve(track);
}

async function search(reset = true) {
    if (search.loading) return;
    search.loading = true;
    let failed = false;
    const query = elements.searchInput.value.trim();
    if (reset) {
        state.offset = 0;
        state.results = [];
        state.hasMore = true;
        state.query = query;
        elements.resultList.replaceChildren(emptyNode('Đang tìm nhạc...'));
    }
    elements.searchStatus.textContent = 'Đang tải kết quả...';
    updateSearchLoader();
    try {
        const data = await api('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: state.query, offset: state.offset })
        });
        const rows = data.results || [];
        const knownUrls = new Set(state.results.map(item => item.url));
        const uniqueRows = rows.filter(item => {
            if (!item?.url || knownUrls.has(item.url)) return false;
            knownUrls.add(item.url);
            return true;
        });
        const previousCount = state.results.length;
        state.results = reset ? uniqueRows : state.results.concat(uniqueRows);
        state.offset += rows.length;
        state.hasMore = Boolean(data.has_more ?? rows.length >= 20) && rows.length > 0;
        if (reset) {
            renderTrackList(elements.resultList, state.results, null, 'Không tìm thấy bài hát', 'search');
            renderFeaturedResults(state.results);
        }
        else appendTrackList(elements.resultList, uniqueRows, null, previousCount, 'search', state.results);
        elements.searchStatus.textContent = state.hasMore ? `${state.results.length} kết quả · kéo xuống để xem thêm` : `${state.results.length} kết quả`;
        if (reset) prefetchTracks(state.results.slice(0, 6), 0, 360);
    } catch (error) {
        failed = true;
        if (reset) state.hasMore = false;
        if (reset) elements.resultList.replaceChildren(emptyNode(`Không tìm được nhạc: ${error.message}`));
        else toast(`Không tải thêm được: ${error.message}`);
        elements.searchStatus.textContent = reset ? 'Tìm kiếm thất bại' : `${state.results.length} kết quả · thử kéo lại`;
    } finally {
        search.loading = false;
        updateSearchLoader();
        if (!failed) maybeLoadMore();
    }
}

function showCurrent(track) {
    state.current = track;
    elements.player.classList.remove('hidden');
    document.body.classList.add('player-visible');
    elements.playerTitle.textContent = track.title || 'Không rõ tên';
    elements.playerImage.src = safeImage(track.thumbnail);
    const artwork = safeImage(track.thumbnail);
    document.documentElement.style.setProperty('--current-artwork', artwork ? `url("${artwork.replaceAll('"', '%22')}")` : 'none');
    updateMediaSessionMetadata(track);
    syncFeedbackControls(track);
    setPlayerCollapsed(state.playerCollapsed, false);
    updatePlayerMode();
}

function resolvePlaybackContext(track, context = null) {
    if (context?.key) {
        const list = state.playbackLists.get(context.key) || [];
        const direct = Number(context.index);
        const index = list[direct]?.url === track.url ? direct : list.findIndex(item => item.url === track.url);
        if (index >= 0) return { key: context.key, index };
    }
    for (const [key, list] of state.playbackLists) {
        const index = list.findIndex(item => item.url === track.url);
        if (index >= 0) return { key, index };
    }
    return null;
}

function playbackPayload(track, context = state.playbackContext) {
    const key = context?.key || 'single';
    const sourceList = context?.key ? (state.playbackLists.get(context.key) || []) : [track];
    const tracks = sourceList.length ? sourceList : [track];
    const index = Math.max(0, tracks.findIndex(item => item.url === track.url));
    return {
        tracks,
        index,
        repeat: state.repeatMode,
        shuffle: state.shuffle,
        source: key,
        source_name: key.startsWith('playlist:') ? key.slice(9) : key
    };
}

function updatePlaybackModeButtons() {
    elements.shuffleToggle.classList.toggle('active', state.shuffle);
    elements.shuffleToggle.setAttribute('aria-pressed', String(state.shuffle));
    elements.shuffleToggle.title = state.shuffle ? 'Tắt phát ngẫu nhiên' : 'Bật phát ngẫu nhiên';
    const repeatLabels = { off: 'Lặp lại: tắt', all: 'Lặp lại toàn bộ', one: 'Lặp lại một bài' };
    elements.repeatToggle.classList.toggle('active', state.repeatMode !== 'off');
    elements.repeatToggle.setAttribute('aria-pressed', String(state.repeatMode !== 'off'));
    elements.repeatToggle.textContent = state.repeatMode === 'one' ? '↻¹' : '↻';
    elements.repeatToggle.title = repeatLabels[state.repeatMode] || repeatLabels.off;
}

function applyPlaybackSession(session) {
    if (!session?.entity_id) return;
    const relevant = state.playingDevice === session.entity_id || state.device === session.entity_id;
    if (!relevant) return;
    state.playbackSession = session;
    if (Array.isArray(session.tracks)) {
        const currentIndex = Math.max(0, Number(session.index) || 0);
        state.queue = session.tracks.slice(currentIndex + 1);
        state.queueScope = 'session';
        state.queueEntityId = session.entity_id;
        state.queueCurrent = session.current_track || session.tracks[currentIndex] || null;
        state.playbackLists.set('queue', state.queue);
    }
    state.repeatMode = session.repeat || 'off';
    state.shuffle = Boolean(session.shuffle);
    if (session.radio?.enabled && session.radio.seed?.url) {
        state.radioContext = {
            key: `remote-radio:${session.session_id}`,
            seed: session.radio.seed,
            media_kind: session.radio.media_kind === 'video' ? 'video' : 'audio',
            profile_id: session.radio.profile_id || activeListenerProfile()?.id || 'default',
            loading: false,
            remote: true
        };
    } else if (state.radioContext?.remote) {
        clearBrowserRadio();
    }
    localStorage.setItem('youtubeProRepeatMode', state.repeatMode);
    localStorage.setItem('youtubeProShuffle', state.shuffle ? '1' : '0');
    updatePlaybackModeButtons();
    const track = session.current_track;
    const activeStates = ['resolving', 'starting', 'playing', 'paused'];
    if (track) {
        state.current = track;
        if (track.media_kind === 'video' && state.videoModeActive) {
            state.videoCurrent = track;
            renderVideoWatch(track, session.state === 'playing' ? 'Đang phát trên loa' : 'Đang chuyển video...');
        }
        state.playingDevice = activeStates.includes(session.state) ? session.entity_id : null;
        state.playingUrl = activeStates.includes(session.state) ? track.url : null;
        state.loadingUrl = ['resolving', 'starting'].includes(session.state) ? track.url : null;
        showCurrent(track);
    }
    state.remoteState = session.state === 'starting' ? 'buffering' : session.state;
    updateRemoteProgress(session.last_position || 0, session.last_duration || track?.duration || 0);
    const messages = {
        resolving: 'Backend đang chuẩn bị bài hát...',
        starting: 'Đã gửi tới loa · đang kết nối...',
        playing: 'Đang phát trên loa',
        paused: 'Đang tạm dừng trên loa',
        completed: 'Đã phát hết danh sách',
        stopped: 'Loa đã dừng',
        error: `Lỗi playback: ${session.last_error || 'không xác định'}`
    };
    if (messages[session.state]) setMessage(messages[session.state]);
    setMediaSessionPlayback(session.state === 'playing' ? 'playing' : session.state === 'paused' ? 'paused' : 'none');
    elements.player.classList.toggle('loading', ['resolving', 'starting'].includes(session.state));
    updateTrackStates();
    updatePlayerMode();
}

function handleServerEvent(payload) {
    if (!payload || typeof payload !== 'object') return;
    if (payload.type === 'playback') {
        applyPlaybackSession(payload.data);
        if (state.activeTab === 'queue' && payload.data?.entity_id === queueTargetEntity()) {
            void loadQueue();
        }
    }
    if (payload.type === 'snapshot') {
        const sessions = payload.data?.playback_sessions || {};
        const entityId = activeRemoteEntity();
        if (entityId && sessions[entityId]) applyPlaybackSession(sessions[entityId]);
    }
    if (payload.type === 'player_state' && payload.data?.entity_id === activeRemoteEntity()) {
        state.remoteState = payload.data.state || state.remoteState;
        state.remoteSyncedAt = Date.now();
        updateRemoteProgress(payload.data.position || 0, payload.data.duration || 0);
    }
}

function setupEventStream() {
    if (typeof EventSource === 'undefined') return;
    try { state.eventSource?.close(); } catch (_) {}
    const source = new EventSource(`${API_BASE}/api/events`);
    state.eventSource = source;
    source.onmessage = event => {
        try { handleServerEvent(JSON.parse(event.data)); } catch (_) {}
    };
}

async function updatePlaybackModes(nextRepeat = state.repeatMode, nextShuffle = state.shuffle) {
    const entityId = activeRemoteEntity();
    state.repeatMode = nextRepeat;
    state.shuffle = Boolean(nextShuffle);
    localStorage.setItem('youtubeProRepeatMode', state.repeatMode);
    localStorage.setItem('youtubeProShuffle', state.shuffle ? '1' : '0');
    updatePlaybackModeButtons();
    if (!entityId || !state.playbackSession) return;
    try {
        const data = await api('/api/playback/control', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                entity_id: entityId,
                action: 'mode',
                repeat: state.repeatMode,
                shuffle: state.shuffle
            })
        });
        if (data.session) applyPlaybackSession(data.session);
    } catch (error) {
        toast(error.message);
    }
}

function relativeCandidate(step, automatic = false) {
    if (!state.current) return null;
    const context = state.playbackContext;
    let remainingInContext = 0;
    if (context?.key) {
        const list = state.playbackLists.get(context.key) || [];
        const currentIndex = list.findIndex(item => item.url === state.current.url);
        const activeIndex = currentIndex >= 0 ? currentIndex : Number(context.index);
        if (automatic && state.repeatMode === 'one') {
            return { track: list[activeIndex] || state.current, context: { key: context.key, index: activeIndex }, fromQueue: false };
        }
        let index = activeIndex + step;
        if (state.shuffle && step > 0 && list.length > 1) {
            do { index = Math.floor(Math.random() * list.length); } while (index === activeIndex);
        } else if ((index < 0 || index >= list.length) && state.repeatMode === 'all' && list.length) {
            index = index < 0 ? list.length - 1 : 0;
        }
        if (list[index]) return { track: list[index], context: { key: context.key, index }, fromQueue: false };
        remainingInContext = Math.max(0, list.length - activeIndex - 1);
    }
    if (step > 0 && context?.key !== 'queue' && state.queue.length) {
        const queueIndex = Math.max(0, step - remainingInContext - 1);
        if (state.queue[queueIndex]) {
            return { track: state.queue[queueIndex], context: null, fromQueue: true, queueIndex };
        }
    }
    return null;
}

function prefetchRelative(step) {
    const candidate = relativeCandidate(step);
    if (candidate) prefetchTrack(candidate.track);
}

function prefetchFollowingTracks() {
    const tracks = [relativeCandidate(1)?.track, relativeCandidate(2)?.track];
    prefetchTracks(tracks, 100, 260);
}

async function playTrack(track, context = null) {
    if (!track?.url) return;
    if (state.videoModeActive || state.videoCurrent) stopVideoPlayback();
    const requestId = ++state.resolveId;
    const targetDevice = state.device;
    const previousDevice = state.playingDevice;
    stopPlaybackImmediately(previousDevice);
    state.playingDevice = targetDevice;
    state.loadingUrl = track.url;
    state.playingUrl = null;
    const playbackContext = resolvePlaybackContext(track, context);
    if (state.radioContext && playbackContext?.key !== state.radioContext.key) {
        clearBrowserRadio();
    }
    state.playbackContext = playbackContext;
    showCurrent(track);
    if (targetDevice !== 'browser') resetRemoteProgress(track.duration || 0);
    updateTrackStates();
    setMessage('Đang tải nhanh bài hát...');
    elements.player.classList.add('loading');
    unlockBrowserAudio(targetDevice);
    const resolvePromise = resolveTrackData(track);
    let playbackStarted = false;
    try {
        const data = await resolvePromise;
        if (requestId !== state.resolveId) return;
        state.current = data.track || track;
        state.token = data.token;
        rememberDetails(state.current.url, data);
        showCurrent(state.current);
        if (targetDevice === 'browser') {
            elements.audio.src = API_BASE + data.media_path;
            elements.audio.load();
            state.audioPriming = false;
            try {
                await elements.audio.play();
                if (requestId !== state.resolveId) return;
                state.audioUnlocked = true;
                playbackStarted = true;
                setMessage('Đang phát trên điện thoại');
            } catch (_) {
                if (requestId !== state.resolveId) return;
                setMessage('Audio đã sẵn sàng — nhấn Play');
                toast('Nhấn nút Play trong thanh phát để bắt đầu');
            }
        } else {
            const playback = playbackPayload(state.current, state.playbackContext);
            const castData = await enqueueRemoteCommand(targetDevice, () => api('/api/cast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: data.token, entity_id: targetDevice, ...playback })
            }));
            if (requestId !== state.resolveId) return;
            if (castData.session) applyPlaybackSession(castData.session);
            playbackStarted = true;
            setMessage('Đã gửi tới loa · đang kết nối...');
        }
        state.loadingUrl = null;
        state.playingUrl = playbackStarted ? state.current.url : null;
        if (!playbackStarted && state.playingDevice === targetDevice) state.playingDevice = null;
        updateTrackStates();
        updatePlayerMode();
        if (targetDevice === 'browser') {
            prefetchFollowingTracks();
            addHistory(state.current);
        }
    } catch (error) {
        if (requestId !== state.resolveId) return;
        state.loadingUrl = null;
        state.playingUrl = null;
        if (state.playingDevice === targetDevice) state.playingDevice = null;
        updateTrackStates();
        updatePlayerMode();
        setMessage(`Không phát được: ${error.message}`);
        toast(`Lỗi phát nhạc: ${error.message}`);
    } finally {
        if (requestId === state.resolveId) {
            state.loadingUrl = null;
            state.audioPriming = false;
            elements.player.classList.remove('loading');
            updateTrackStates();
        }
    }
}

async function playRelative(step, automatic = false) {
    const entityId = state.playingDevice && state.playingDevice !== 'browser' ? state.playingDevice : null;
    if (entityId && state.playbackSession) {
        try {
            const data = await api('/api/playback/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ entity_id: entityId, action: step > 0 ? 'next' : 'previous' })
            });
            if (data.session) applyPlaybackSession(data.session);
        } catch (error) {
            toast(error.message);
        }
        return;
    }
    let candidate = relativeCandidate(step, automatic);
    if (!candidate && step > 0 && state.radioContext?.media_kind === 'audio') {
        await refillBrowserRadio();
        candidate = relativeCandidate(step, automatic);
    } else if (step > 0 && state.radioContext?.media_kind === 'audio') {
        void refillBrowserRadio();
    }
    if (!candidate) return;
    if (candidate.fromQueue) {
        state.queue.splice(0, 1);
        state.playbackLists.set('queue', state.queue);
        state.playbackLists.set('queue-fallback', [candidate.track]);
        candidate.context = { key: 'queue-fallback', index: 0 };
        api('/api/queue/0', { method: 'DELETE' }).then(loadQueue).catch(loadQueue);
    }
    await playTrack(candidate.track, candidate.context);
}

function showDetailsDialog() {
    if (elements.detailsDialog.open) return;
    if (typeof elements.detailsDialog.showModal === 'function') elements.detailsDialog.showModal();
    else elements.detailsDialog.setAttribute('open', '');
}

function closeDetailsDialog() {
    state.detailsRequestId += 1;
    state.lyricsRequestId += 1;
    if (typeof elements.detailsDialog.close === 'function') elements.detailsDialog.close();
    else elements.detailsDialog.removeAttribute('open');
}

function renderDetails(track, details = {}, loading = false, error = '') {
    const merged = { ...track, ...details };
    elements.detailsTitle.textContent = merged.title || 'Không rõ tên';
    elements.detailsImage.src = safeImage(merged.thumbnail);
    elements.detailsChannel.textContent = merged.channel || 'Chưa rõ kênh';
    elements.detailsDuration.textContent = formatDuration(merged.duration) || '—';
    elements.detailsViews.textContent = formatCount(merged.view_count);
    elements.detailsLikes.textContent = formatCount(merged.like_count);
    elements.detailsDate.textContent = formatUploadDate(merged.upload_date);
    elements.detailsDescription.textContent = loading
        ? 'Đang tải mô tả...'
        : (merged.description || 'Video này không có mô tả.');
    const source = merged.strategy ? ` · ${merged.strategy}${merged.format_id ? ` / ${merged.format_id}` : ''}` : '';
    elements.detailsStatus.textContent = error || (loading ? 'Đang lấy thông tin từ YouTube...' : `Đã tải thông tin${source}`);
    const videoUrl = safeYouTubeUrl(merged.url || track.url);
    elements.detailsOpenVideo.classList.toggle('hidden', !videoUrl);
    if (videoUrl) elements.detailsOpenVideo.href = videoUrl;
    else elements.detailsOpenVideo.removeAttribute('href');
}

function parseSyncedLyrics(text) {
    const lines = [];
    const pattern = /\[(\d{1,2}):(\d{2})(?:[.:](\d{2,3}))?\]/g;
    for (const rawLine of String(text || '').split(/\r?\n/)) {
        const timestamps = [];
        pattern.lastIndex = 0;
        let match;
        while ((match = pattern.exec(rawLine)) !== null) {
            const minutes = Number(match[1]) || 0;
            const seconds = Number(match[2]) || 0;
            const fraction = match[3]
                ? Number(match[3].length === 2 ? `${match[3]}0` : match[3]) / 1000
                : 0;
            timestamps.push(minutes * 60 + seconds + fraction);
        }
        const content = rawLine.replace(pattern, '').trim();
        for (const time of timestamps) lines.push({ time, content });
    }
    lines.sort((a, b) => a.time - b.time);
    return lines;
}

function highlightLyrics(position) {
    const container = elements.detailsLyrics;
    if (!container || container.dataset.synced !== '1') return;
    const rows = container.querySelectorAll('.lyric-line');
    if (!rows.length) return;
    let activeIndex = -1;
    rows.forEach((row, index) => {
        if (Number(row.dataset.time) <= position + 0.2) activeIndex = index;
    });
    rows.forEach((row, index) => row.classList.toggle('active', index === activeIndex));
    if (activeIndex >= 0 && !rows[activeIndex].dataset.scrolled) {
        rows[activeIndex].dataset.scrolled = '1';
        rows[activeIndex].scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
}

async function loadLyrics(track) {
    const wrap = elements.detailsLyricsWrap;
    const container = elements.detailsLyrics;
    if (!wrap || !container || !track?.title) return;
    wrap.classList.remove('hidden');
    container.dataset.synced = '';
    container.textContent = 'Đang tìm lời...';
    const requestId = ++state.lyricsRequestId;
    try {
        const payload = await api('/api/lyrics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: track.title,
                artist: track.channel,
                duration: track.duration
            })
        });
        if (requestId !== state.lyricsRequestId || !elements.detailsDialog.open) return;
        if (!payload.found) {
            container.textContent = 'Không tìm thấy lời cho bài này.';
            return;
        }
        if (payload.synced) {
            container.dataset.synced = '1';
            const lines = parseSyncedLyrics(payload.synced);
            container.replaceChildren();
            if (!lines.length) {
                container.textContent = payload.plain || 'Không có lời đồng bộ.';
                return;
            }
            for (const line of lines) {
                const row = document.createElement('p');
                row.className = 'lyric-line';
                row.dataset.time = String(line.time);
                row.textContent = line.content || '♪';
                container.appendChild(row);
            }
        } else {
            container.textContent = payload.plain || 'Không tìm thấy lời cho bài này.';
        }
    } catch (error) {
        if (requestId !== state.lyricsRequestId) return;
        container.textContent = `Không tải được lời: ${error.message}`;
    }
}

async function openDetails(track, context = null) {
    if (!track?.url) return;
    const requestId = ++state.detailsRequestId;
    state.detailsTrack = track;
    state.detailsContext = context || resolvePlaybackContext(track);
    syncFeedbackControls();
    const cached = state.detailsCache.get(track.url);
    renderDetails(track, cached || {}, !cached);
    loadLyrics(track);
    showDetailsDialog();
    if (cached) return;
    try {
        const pending = getResolveEntry(track.url, 'browser') || getResolveEntry(track.url, 'remote');
        const data = pending
            ? await pending.promise
            : await api('/api/details', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: track.url })
            });
        if (requestId !== state.detailsRequestId || !elements.detailsDialog.open) return;
        rememberDetails(track.url, data);
        const details = state.detailsCache.get(track.url) || data.details || {};
        state.detailsTrack = { ...track, ...(data.track || {}) };
        renderDetails(state.detailsTrack, details);
        syncFeedbackControls();
        if (!pending) schedulePrefetch(state.detailsTrack, 0);
    } catch (error) {
        if (requestId !== state.detailsRequestId || !elements.detailsDialog.open) return;
        renderDetails(track, {}, false, `Không tải được chi tiết: ${error.message}`);
    }
}

function queueTargetEntity() {
    const entityId = activeRemoteEntity();
    return entityId || null;
}

function queueUrl(path, entityId = queueTargetEntity()) {
    return entityId ? `${path}?entity_id=${encodeURIComponent(entityId)}` : path;
}

function applyQueueView(view = {}) {
    state.queue = Array.isArray(view.tracks) ? view.tracks : [];
    state.queueScope = view.scope === 'session' ? 'session' : 'global';
    state.queueEntityId = view.entity_id || null;
    state.queueCurrent = view.current_track || null;
    if (view.session) applyPlaybackSession(view.session);
    if (elements.queueCount) elements.queueCount.textContent = String(state.queue.length);
    if (elements.queueScope) {
        const device = state.devices.find(item => item.entity_id === state.queueEntityId);
        elements.queueScope.textContent = state.queueScope === 'session'
            ? `Đang quản lý danh sách tiếp theo trên ${device?.name || state.queueEntityId}`
            : 'Hàng chờ chung cho trình duyệt và phiên phát mới';
    }
    if (elements.queueCurrent) {
        elements.queueCurrent.replaceChildren();
        elements.queueCurrent.classList.toggle('hidden', !state.queueCurrent);
        if (state.queueCurrent) {
            const label = document.createElement('div');
            label.className = 'queue-now-label';
            label.innerHTML = '<span></span><strong>Đang phát</strong>';
            elements.queueCurrent.append(
                label,
                trackRow(state.queueCurrent, {
                    queue: false,
                    favorite: false,
                    radio: true,
                    meta: `${state.queueCurrent.channel || 'YouTube'} · hiện tại`
                })
            );
        }
    }
    renderTrackList(
        elements.queueList,
        state.queue,
        (_, index) => ({
            favorite: false,
            queue: false,
            radio: false,
            details: false,
            moveUp: index > 0 ? () => moveQueue(index, index - 1) : null,
            moveDown: index < state.queue.length - 1 ? () => moveQueue(index, index + 1) : null,
            remove: () => removeQueue(index),
            meta: `Tiếp theo · vị trí ${index + 1}`
        }),
        state.queueScope === 'session' ? 'Loa không còn bài tiếp theo' : 'Hàng chờ đang trống',
        state.queueScope === 'global' ? 'queue' : null
    );
}

async function addQueue(track, position = 'end') {
    try {
        const data = await api('/api/queue/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                track,
                entity_id: queueTargetEntity(),
                position
            })
        });
        if (data.queue) applyQueueView(data.queue);
        toast(position === 'next' ? 'Đã đặt phát tiếp theo' : 'Đã thêm cuối hàng chờ');
        if (state.activeTab === 'queue') await loadQueue();
    } catch (error) { toast(error.message); }
}

async function startRadio(track) {
    if (!track?.url || state.radioLoading) return;
    state.radioLoading = true;
    const targetDevice = state.device;
    const mediaKind = track.media_kind === 'video' ? 'video' : 'audio';
    const alreadyPlaying = state.current?.url === track.url
        && state.playingDevice === targetDevice;
    try {
        if (!alreadyPlaying) {
            if (mediaKind === 'video') await playVideo(track);
            else await playTrack(track, resolvePlaybackContext(track));
        }
        const data = await api('/api/radio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                seed: track,
                entity_id: targetDevice === 'browser' ? null : targetDevice,
                media_kind: mediaKind,
                limit: 24,
                mode: 'replace',
                start_if_missing: targetDevice !== 'browser',
                profile_id: activeListenerProfile()?.id || 'default'
            })
        });
        if (data.session) {
            applyPlaybackSession(data.session);
            await loadQueue();
        } else {
            const radioTracks = [data.seed || track, ...(data.tracks || [])];
            const key = `radio:${Date.now()}`;
            state.radioContext = {
                key,
                seed: data.seed || track,
                media_kind: mediaKind,
                profile_id: data.profile_id || activeListenerProfile()?.id || 'default',
                loading: false
            };
            state.playbackLists.set(key, radioTracks);
            if (mediaKind === 'video') {
                state.videoResults = radioTracks;
                state.videoCurrent = data.seed || track;
                renderVideoWatch(state.videoCurrent, 'Đài phát đang hoạt động');
            } else {
                state.playbackContext = { key, index: 0 };
            }
            state.current = data.seed || track;
            updateTrackStates();
        }
        toast(`Đài phát đã sẵn sàng · ${data.tracks?.length || 0} bài đề xuất`);
    } catch (error) {
        toast(`Không tạo được đài phát: ${error.message}`);
    } finally {
        state.radioLoading = false;
    }
}

async function refillBrowserRadio() {
    const context = state.radioContext;
    if (!context || context.loading) return;
    const list = state.playbackLists.get(context.key) || [];
    const currentUrl = context.media_kind === 'video' ? state.videoCurrent?.url : state.current?.url;
    const currentIndex = list.findIndex(item => item.url === currentUrl);
    const remaining = currentIndex >= 0 ? list.length - currentIndex - 1 : list.length;
    if (remaining > 5) return;
    context.loading = true;
    try {
        const data = await api('/api/radio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                seed: context.seed,
                media_kind: context.media_kind,
                limit: 12,
                exclude_urls: list.map(item => item.url),
                profile_id: context.profile_id || activeListenerProfile()?.id || 'default'
            })
        });
        const known = new Set(list.map(item => item.url));
        const additions = (data.tracks || []).filter(item => item?.url && !known.has(item.url));
        if (additions.length) {
            const next = list.concat(additions);
            state.playbackLists.set(context.key, next);
            if (context.media_kind === 'video') {
                state.videoResults = next;
                renderVideoRelated(state.videoCurrent);
            }
        }
    } catch (error) {
        console.info('Radio refill skipped', error.message);
    } finally {
        context.loading = false;
    }
}

async function loadQueue() {
    try {
        const data = await api(queueUrl('/api/queue/view'));
        applyQueueView(data);
    } catch (_) {
        try {
            const tracks = await api('/api/queue');
            applyQueueView({ scope: 'global', tracks });
        } catch (_) {
            applyQueueView({ scope: 'global', tracks: [] });
        }
    }
}

async function removeQueue(index) {
    try {
        const data = await api(queueUrl(`/api/queue/items/${index}`, state.queueEntityId), { method: 'DELETE' });
        applyQueueView(data.queue || {});
    } catch (error) { toast(error.message); }
}

async function moveQueue(fromIndex, toIndex) {
    try {
        const data = await api('/api/queue/items', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                entity_id: state.queueEntityId,
                from_index: fromIndex,
                to_index: toIndex
            })
        });
        applyQueueView(data.queue || {});
    } catch (error) { toast(error.message); }
}

async function shuffleQueue() {
    if (state.queue.length < 2) return toast('Cần ít nhất 2 bài để xáo trộn');
    try {
        const data = await api('/api/queue/shuffle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entity_id: state.queueEntityId })
        });
        applyQueueView(data.queue || {});
        toast('Đã xáo trộn các bài tiếp theo');
    } catch (error) { toast(error.message); }
}

async function saveQueue() {
    const suggestion = `Hàng chờ ${new Date().toLocaleDateString('vi-VN')}`;
    const name = prompt('Tên playlist lưu hàng chờ', suggestion);
    if (!name) return;
    try {
        const data = await api('/api/queue/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, entity_id: state.queueEntityId })
        });
        toast(`Đã lưu playlist “${data.name}” · thêm ${data.added} bài`);
        await loadPlaylists();
    } catch (error) { toast(error.message); }
}

async function clearQueue() {
    if ((state.queue.length || state.queueCurrent) && !confirm('Xóa toàn bộ các bài tiếp theo?')) return;
    try {
        const data = await api(queueUrl('/api/queue/view', state.queueEntityId), {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entity_id: state.queueEntityId })
        });
        applyQueueView(data.queue || {});
    } catch (error) { toast(error.message); }
}

async function loadLibrary() {
    await Promise.all([loadPlaylists(), loadHistory()]);
}

async function loadPlaylists() {
    try { state.playlists = await api('/api/playlists'); } catch (_) { state.playlists = {}; }
    const names = Object.keys(state.playlists);
    if (elements.playlistCount) elements.playlistCount.textContent = String(names.length);
    if (!state.selectedPlaylist || !state.playlists[state.selectedPlaylist]) {
        state.selectedPlaylist = names[0] || null;
    }
    elements.playlistTabs.replaceChildren();
    names.forEach(name => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `chip${name === state.selectedPlaylist ? ' active' : ''}`;
        button.textContent = name;
        button.addEventListener('click', () => {
            state.selectedPlaylist = name;
            renderPlaylists();
        });
        elements.playlistTabs.append(button);
    });
    renderPlaylists();
    refreshPlaylistSelect();
}

async function importPlaylistFromUrl() {
    const input = elements.playlistImportUrl;
    const url = String(input?.value || '').trim();
    if (!url) { toast('Dán link playlist YouTube trước'); return; }
    const button = elements.playlistImportButton;
    if (button) { button.disabled = true; button.textContent = 'Đang nhập...'; }
    try {
        const payload = await api('/api/playlists/import-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        toast(`Đã nhập ${payload.count} bài vào "${payload.name}"`);
        if (input) input.value = '';
        await loadPlaylists();
        if (state.playlists[payload.name]) {
            state.selectedPlaylist = payload.name;
            renderPlaylists();
        }
    } catch (error) {
        toast(`Nhập playlist lỗi: ${error.message}`);
    } finally {
        if (button) { button.disabled = false; button.textContent = 'Nhập playlist'; }
    }
}

async function loadStats() {
    if (!elements.statsTracks) return;
    try {
        const payload = await api('/api/stats');
        if (elements.statsSummary) {
            elements.statsSummary.textContent = payload.total_plays
                ? `${payload.total_plays} lượt nghe · ${payload.track_count} bài`
                : 'Chưa có dữ liệu nghe.';
        }
        if (elements.statsChannels) {
            elements.statsChannels.replaceChildren();
            (payload.top_channels || []).forEach(item => {
                const chip = document.createElement('span');
                chip.className = 'chip';
                chip.textContent = `${item.channel} · ${item.plays}`;
                elements.statsChannels.append(chip);
            });
        }
        if (elements.statsTracks) {
            renderTrackList(
                elements.statsTracks,
                payload.top_tracks || [],
                () => ({ queue: true }),
                'Chưa có dữ liệu nghe.',
                'stats'
            );
        }
    } catch (error) {
        if (elements.statsSummary) elements.statsSummary.textContent = `Không tải được thống kê: ${error.message}`;
    }
}

function renderPlaylists() {
    const name = state.selectedPlaylist;
    elements.playlistToolbar.classList.toggle('hidden', !name);
    elements.playlistTitle.textContent = name || '';
    const tracks = name ? state.playlists[name] || [] : [];
    renderTrackList(
        elements.playlistItems,
        tracks,
        (_, index) => ({ queue: true, favorite: false, remove: () => removePlaylistItem(name, index) }),
        name ? 'Playlist đang trống' : 'Chưa có playlist',
        name ? `playlist:${name}` : null
    );
    $$('.chip').forEach(button => button.classList.toggle('active', button.textContent === name));
}

function refreshPlaylistSelect() {
    elements.timerPlaylist.replaceChildren();
    Object.keys(state.playlists).forEach(name => elements.timerPlaylist.add(new Option(name, name)));
}

async function createPlaylist() {
    const name = prompt('Tên playlist mới');
    if (!name) return;
    try {
        await api('/api/playlists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        state.selectedPlaylist = name.trim();
        await loadPlaylists();
    } catch (error) { toast(error.message); }
}

async function deletePlaylist() {
    const name = state.selectedPlaylist;
    if (!name || !confirm(`Xóa playlist “${name}”?`)) return;
    await api(`/api/playlists/${encodeURIComponent(name)}`, { method: 'DELETE' });
    state.selectedPlaylist = null;
    await loadPlaylists();
}

async function removePlaylistItem(name, index) {
    await api(`/api/playlists/${encodeURIComponent(name)}/items/${index}`, { method: 'DELETE' });
    await loadPlaylists();
}

async function ensureFavorites() {
    if (!state.playlists['Yêu thích']) {
        await api('/api/playlists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: 'Yêu thích' })
        });
    }
}

async function addFavorite(track) {
    try {
        await ensureFavorites();
        await api(`/api/playlists/${encodeURIComponent('Yêu thích')}/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(track)
        });
        toast('Đã thêm vào Yêu thích');
        await loadPlaylists();
    } catch (error) { toast(error.message); }
}

async function addHistory(track) {
    try {
        await api('/api/history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(track)
        });
        await loadHistory();
    } catch (_) {}
}

async function loadHistory() {
    try { state.history = await api('/api/history'); } catch (_) { state.history = []; }
    if (elements.historyCount) elements.historyCount.textContent = String(state.history.length);
    const rows = state.history.slice().reverse().slice(0, 20);
    renderTrackList(
        elements.historyList,
        rows,
        track => ({ meta: track.played_at || 'Đã nghe', queue: true, favorite: true }),
        'Chưa có lịch sử nghe',
        'history'
    );
}

async function clearHistory() {
    await api('/api/history', { method: 'DELETE' });
    await loadHistory();
}

function stopBrowserForSleep() {
    state.resolveId += 1;
    state.playingDevice = null;
    state.loadingUrl = null;
    state.playingUrl = null;
    stopBrowserPlayback();
    elements.player.classList.remove('loading');
    updateTrackStates();
    updatePlayerMode();
    setMessage('Đã dừng theo sleep timer');
    toast('Đã dừng nhạc theo hẹn giờ');
}

function syncSleepTimer(data) {
    clearTimeout(state.sleepHandle);
    state.sleepHandle = null;
    if (data.enabled && data.end_at) {
        const delay = new Date(data.end_at).getTime() - Date.now();
        if (data.entity_id === 'browser' && delay > 0) {
            state.sleepHandle = setTimeout(stopBrowserForSleep, delay);
        }
        const seconds = Number(data.remaining || Math.max(0, delay / 1000));
        elements.sleepStatus.textContent = `Còn ${Math.floor(seconds / 60)} phút`;
        return;
    }
    elements.sleepStatus.textContent = 'Chưa bật';
    if (data.entity_id === 'browser' && data.last_triggered_at && data.last_triggered_at !== state.lastSleepTrigger) {
        const age = Date.now() - new Date(data.last_triggered_at).getTime();
        if (age >= 0 && age < 120000) stopBrowserForSleep();
        state.lastSleepTrigger = data.last_triggered_at;
        localStorage.setItem('youtubeProLastSleepTrigger', state.lastSleepTrigger);
    }
}

async function loadSleep() {
    try { syncSleepTimer(await api('/api/sleep')); } catch (_) {}
}

async function setSleep(minutes) {
    try {
        const data = await api('/api/sleep', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ minutes, entity_id: state.device })
        });
        syncSleepTimer(data.sleep);
        toast(`Đã hẹn tắt sau ${minutes} phút`);
    } catch (error) { toast(error.message); }
}

async function cancelSleep() {
    await api('/api/sleep', { method: 'DELETE' });
    await loadSleep();
}

function toggleTimerFields() {
    const stop = elements.timerType.value === 'stop';
    elements.timerPlaylistWrap.classList.toggle('hidden', stop);
    elements.timerDurationWrap.classList.toggle('hidden', stop);
}

async function loadTimers() {
    try { state.timers = await api('/api/timers'); } catch (_) { state.timers = []; }
    elements.timerList.replaceChildren();
    if (!state.timers.length) {
        elements.timerList.append(emptyNode('Chưa có lịch phát'));
        return;
    }
    const dayNames = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];
    state.timers.forEach(timer => {
        const card = document.createElement('article');
        card.className = 'timer-card';
        const title = document.createElement('strong');
        title.textContent = `${timer.time} · ${timer.type === 'play' ? 'Phát' : 'Dừng'}`;
        const meta = document.createElement('p');
        const days = timer.days?.length ? timer.days.map(day => dayNames[day]).join(', ') : 'Mỗi ngày';
        meta.textContent = timer.type === 'play' ? `${timer.playlist_name} · ${days}` : days;
        const remove = actionButton('Xóa', 'Xóa lịch', async () => {
            await api(`/api/timers/${encodeURIComponent(timer.id)}`, { method: 'DELETE' });
            await loadTimers();
        }, true);
        card.append(title, meta, remove);
        elements.timerList.append(card);
    });
}

async function saveTimer(event) {
    event.preventDefault();
    const days = $$('input[name="timerDay"]:checked').map(input => Number(input.value));
    const body = {
        time: $('#timerTime').value,
        entity_id: elements.timerDevice.value,
        type: elements.timerType.value,
        playlist_name: elements.timerPlaylist.value,
        duration: Number($('#timerDuration').value || 0),
        days,
        is_random: $('#timerRandom').checked,
        enabled: true
    };
    try {
        await api('/api/timers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        toast('Đã lưu lịch');
        elements.timerForm.reset();
        $('#timerRandom').checked = true;
        toggleTimerFields();
        await loadTimers();
    } catch (error) { toast(error.message); }
}

async function remoteControl(action) {
    const entityId = activeRemoteEntity();
    if (!entityId || entityId === 'browser') return;
    if (action === 'stop') {
        state.resolveId += 1;
        state.playingDevice = null;
        state.loadingUrl = null;
        state.playingUrl = null;
        elements.player.classList.remove('loading');
        updateTrackStates();
        updatePlayerMode();
    }
    try {
        if (action === 'stop') await stopRemotePlayback(entityId);
        else await enqueueRemoteCommand(entityId, () => remoteControlRequest(entityId, action));
        setMessage(action === 'stop' ? 'Đã dừng loa' : 'Đã gửi lệnh tới loa');
        if (action === 'stop') resetRemoteProgress(state.current?.duration || 0);
        else scheduleRemoteStatePoll(180);
    } catch (error) { toast(error.message); }
}

async function setRemoteVolume(value) {
    const entityId = activeRemoteEntity();
    if (entityId === 'browser') return;
    try {
        await enqueueRemoteCommand(entityId, () => remoteControlRequest(entityId, 'volume', { volume: Number(value) }));
    } catch (_) {}
}

async function loadStatus() {
    elements.systemStatus.textContent = 'Đang kiểm tra...';
    try {
        const data = await api('/api/status');
        const extractor = data.last_extractor || {};
        const preference = data.extractor_preference || {};
        const pot = data.pot_token_provider || {};
        const castProfile = data.cast_preference || {};
        const websocketState = data.ha_websocket || {};
        const integration = data.integration_api || {};
        const license = data.license || {};
        renderLicense(license);
        elements.integrationTokenStatus.textContent = integration.ready
            ? `API v${integration.api_version || 1} · sẵn sàng`
            : 'Chưa sẵn sàng';
        elements.systemStatus.textContent = [
            `Home Assistant: ${data.ha_ok ? 'OK' : 'Lỗi kết nối'}`,
            `Deno: ${data.deno ? 'OK' : 'Chưa có'}`,
            `yt-dlp-ejs: ${data.ejs || 'Chưa có'}`,
            `yt-dlp: ${data.yt_dlp}`,
            `Extractor: ${extractor.strategy || 'Chưa phát'}${extractor.format_id ? ` · format ${extractor.format_id}` : ''}${extractor.cache_hit ? ' · cache' : ''}${extractor.elapsed_ms != null ? ` · ${extractor.elapsed_ms} ms` : ''}`,
            `Ưu tiên lần sau: ${preference.preferred || 'Tự động'}`,
            `PO Token: ${!pot.enabled ? 'Tắt' : (pot.available ? `OK · server ${pot.version || '?'} · plugin ${pot.plugin || '?'}` : `Chưa sẵn sàng${pot.error ? ` · ${pot.error}` : ''}`)}`,
            `Profile loa: ${castProfile.preferred_transport ? `${castProfile.preferred_transport} · ${castProfile.preferred_media_type || 'auto'}` : 'Chưa học'}`,
            `HA WebSocket: ${websocketState.connected ? 'Đã kết nối' : `REST fallback${websocketState.last_error ? ` · ${websocketState.last_error}` : ''}`}`,
            `License: ${license.valid ? `${license.plan_name || license.plan_code || 'Hợp lệ'} · ${formatLicenseExpiry(license.expires_at)}` : `${license.state || 'chưa có'}${license.enforcement ? ' · enforcement bật' : ' · enforcement tắt'}`}`,
            'Tài khoản Google: Không sử dụng',
            `Relay loa: ${data.media_base_url}`,
            data.last_error ? `Lỗi gần nhất: ${data.last_error}` : 'Không có lỗi gần đây'
        ].join('\n');
    } catch (error) {
        elements.systemStatus.textContent = error.message;
    }
}

function formatLicenseExpiry(value) {
    if (!value) return 'Vĩnh viễn';
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleString('vi-VN');
}

function readLicenseBootstrap() {
    const node = $('#licenseBootstrap');
    if (!node) return null;
    try {
        const license = JSON.parse(node.textContent || '{}');
        return license && typeof license === 'object' ? license : null;
    } catch (_) {
        return null;
    }
}

function renderLicense(license) {
    license = license && typeof license === 'object' ? license : {};
    const licenseState = license.state || 'unlicensed';
    const labels = {
        active: 'Đang hoạt động',
        offline_grace: 'Offline grace',
        unlicensed: 'Chưa có license',
        waiting_activation: 'Chờ xác nhận trên web',
        waiting_for_portal: 'Chờ xác nhận trên web',
        linked_no_license: 'Đã liên kết · chưa có gói',
        expired: 'Đã hết hạn',
        invalid: 'Không hợp lệ',
        server_unreachable: 'Không kết nối server'
    };
    const label = labels[licenseState] || licenseState;
    const installation = `Installation: …${license.installation_suffix || '—'}`;
    if (elements.licenseStatus) {
        elements.licenseStatus.textContent = label;
        elements.licenseStatus.dataset.state = licenseState;
    }
    if (elements.licenseGateStatus) elements.licenseGateStatus.textContent = label;
    if (elements.licenseInstallation) elements.licenseInstallation.textContent = installation;
    if (elements.licenseGateInstallation) elements.licenseGateInstallation.textContent = installation;
    if ('portal_url' in license || 'claim_url' in license) {
        const portal = license.portal_url || '';
        for (const link of [elements.licensePortalLink, elements.licenseGatePortalLink]) {
            if (!link) continue;
            if (portal) {
                link.href = license.claim_url || portal;
                link.textContent = license.claim_url ? 'Kích hoạt tự động' : 'Mở trang License';
                link.classList.remove('hidden');
            } else {
                link.classList.add('hidden');
                link.removeAttribute('href');
            }
        }
    }
    let description = '';
    if (license.valid) {
        description = `${license.plan_name || license.plan_code || 'License'} · hết hạn: ${formatLicenseExpiry(license.expires_at)}${license.key_prefix ? ` · ${license.key_prefix}` : ''}`;
        elements.deactivateLicense?.classList.remove('hidden');
    } else if (license.error) {
        description = `Chưa xác minh được license: ${license.error}`;
        elements.deactivateLicense?.classList.add('hidden');
    } else {
        description = license.claim_url
            ? 'Mở trang kích hoạt và đăng nhập bằng email. Add-on tự mở khóa trong vài giây; không dùng tài khoản Google.'
            : 'Đang chuẩn bị liên kết bảo mật với trang kích hoạt.';
        elements.deactivateLicense?.classList.add('hidden');
    }
    if (elements.licenseDescription) elements.licenseDescription.textContent = description;
    if (elements.licenseGateDescription) elements.licenseGateDescription.textContent = description;

    const valid = license.valid === true;
    state.licenseReady = valid;
    document.body.classList.remove('license-pending', 'license-locked', 'license-active');
    document.body.classList.add(valid ? 'license-active' : 'license-locked');
    if (elements.appShell) {
        elements.appShell.inert = !valid;
        elements.appShell.setAttribute('aria-hidden', valid ? 'false' : 'true');
    }
    if (!valid) stopLicensedRuntime();
    return valid;
}

async function loadLicense(force = false) {
    try {
        const data = await api(`/api/license${force ? '?refresh=1' : ''}`, { cache: 'no-store' });
        const license = data.license || {};
        if (renderLicense(license)) await startLicensedRuntime();
        return license;
    } catch (error) {
        const cachedActive = state.licenseReady || state.licensedRuntime
            || document.body.classList.contains('license-active');
        if (!cachedActive) {
            document.body.classList.remove('license-pending', 'license-active');
            document.body.classList.add('license-locked');
            if (elements.licenseDescription) elements.licenseDescription.textContent = error.message;
            if (elements.licenseGateDescription) elements.licenseGateDescription.textContent = error.message;
            if (elements.licenseGateStatus) elements.licenseGateStatus.textContent = 'Không kết nối được License Server';
            return null;
        }
        if (elements.licenseStatus) elements.licenseStatus.textContent = 'Đang dùng license đã lưu';
        return { valid: true, state: 'active' };
    }
}

function scheduleLicensePoll(license) {
    if (state.licensePollTimeout) clearTimeout(state.licensePollTimeout);
    const fast = !license?.valid && Date.now() < state.licenseFastPollUntil;
    const delay = license?.valid ? 60000 : (fast ? 1250 : 30000);
    state.licensePollTimeout = setTimeout(async () => {
        const next = await loadLicense(false);
        scheduleLicensePoll(next);
    }, delay);
}

function formatLicenseKey(value) {
    const compact = String(value || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 23);
    if (compact.length <= 3) return compact;
    const prefix = compact.slice(0, 3);
    const body = compact.slice(3).match(/.{1,5}/g)?.join('-') || '';
    return `${prefix}-${body}`;
}

function syncLicenseInputs(source) {
    const formatted = formatLicenseKey(source.value);
    source.value = formatted;
    $$('[data-license-key]').forEach(input => {
        if (input !== source) input.value = formatted;
    });
}

function setLicenseSubmitBusy(busy) {
    $$('[data-license-submit]').forEach(button => {
        button.disabled = busy;
        button.classList.toggle('loading', busy);
        const label = button.querySelector('span');
        if (label) label.textContent = busy ? 'Đang xác minh' : 'Kích hoạt key';
    });
}

async function activateLicense(event) {
    event.preventDefault();
    const input = event.currentTarget.querySelector('[data-license-key]');
    const key = formatLicenseKey(input?.value).trim();
    if (!key) return toast('Hãy nhập License Key');
    try {
        setLicenseSubmitBusy(true);
        if (elements.licenseGateStatus) elements.licenseGateStatus.textContent = 'Đang xác minh License Key';
        const data = await api('/api/license', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ license_key: key })
        });
        $$('[data-license-key]').forEach(field => { field.value = ''; });
        const valid = renderLicense(data.license || {});
        toast('Đã kích hoạt License Key');
        if (valid) await startLicensedRuntime();
    } catch (error) {
        toast(error.message);
        const license = error.payload?.license;
        if (license) renderLicense(license);
        if (elements.licenseGateStatus) elements.licenseGateStatus.textContent = 'Kích hoạt chưa thành công';
    } finally {
        setLicenseSubmitBusy(false);
    }
}

async function deactivateLicense() {
    if (!confirm('Gỡ liên kết license khỏi installation này?')) return;
    try {
        const data = await api('/api/license', { method: 'DELETE' });
        renderLicense(data.license || {});
        toast('Đã gỡ liên kết license');
    } catch (error) {
        toast(error.message);
    }
}

async function fetchIntegrationToken() {
    const data = await api('/api/integration-token', { cache: 'no-store' });
    elements.integrationToken.value = data.token || '';
    elements.integrationTokenStatus.textContent = data.updated_at
        ? `Sẵn sàng · ${data.updated_at}`
        : 'Sẵn sàng';
    return elements.integrationToken.value;
}

async function toggleIntegrationToken() {
    try {
        if (!elements.integrationToken.value) await fetchIntegrationToken();
        const reveal = elements.integrationToken.type === 'password';
        elements.integrationToken.type = reveal ? 'text' : 'password';
        elements.toggleIntegrationToken.textContent = reveal ? 'Ẩn token' : 'Hiện token';
    } catch (error) {
        toast(error.message);
    }
}

async function copyIntegrationToken() {
    try {
        const token = elements.integrationToken.value || await fetchIntegrationToken();
        if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(token);
        } else {
            const previousType = elements.integrationToken.type;
            elements.integrationToken.type = 'text';
            elements.integrationToken.select();
            document.execCommand('copy');
            elements.integrationToken.type = previousType;
        }
        toast('Đã sao chép integration token');
    } catch (error) {
        toast(error.message);
    }
}

async function rotateIntegrationToken() {
    if (!confirm('Tạo token mới? Custom integration đang dùng token cũ sẽ mất kết nối ngay.')) return;
    try {
        const data = await api('/api/integration-token', {
            method: 'POST',
            cache: 'no-store',
            headers: { 'X-YouTube-Pro-Action': 'rotate-token' }
        });
        elements.integrationToken.value = data.token || '';
        elements.integrationToken.type = 'password';
        elements.toggleIntegrationToken.textContent = 'Hiện token';
        elements.integrationTokenStatus.textContent = data.updated_at
            ? `Đã tạo mới · ${data.updated_at}`
            : 'Đã tạo mới';
        toast('Đã tạo integration token mới');
    } catch (error) {
        toast(error.message);
    }
}

async function resetCastProfile() {
    const entityId = activeRemoteEntity();
    try {
        await api('/api/cast-preferences', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entity_id: entityId || '' })
        });
        toast(entityId ? 'Đã quên profile của loa đang chọn' : 'Đã xóa mọi profile loa');
        await loadStatus();
    } catch (error) {
        toast(error.message);
    }
}

function bindEvents() {
    elements.themeToggle.addEventListener('click', () => {
        applyTheme(document.documentElement.dataset.theme === 'light' ? 'dark' : 'light');
    });
    elements.searchForm.addEventListener('submit', event => {
        event.preventDefault();
        if (state.activeTab === 'video') {
            elements.videoSearchInput.value = elements.searchInput.value;
            searchVideos(true);
        } else {
            search(true);
        }
    });
    elements.videoSearchForm?.addEventListener('submit', event => {
        event.preventDefault();
        searchVideos(true);
    });
    $$('.quick-search').forEach(button => button.addEventListener('click', () => {
        elements.searchInput.value = button.dataset.query || '';
        selectTab('home');
        search(true);
    }));
    $('#refreshSearch').addEventListener('click', () => search(true));
    elements.loadMore.addEventListener('click', () => search(false));
    elements.videoLoadMore?.addEventListener('click', () => searchVideos(false));
    elements.closeVideoWatch?.addEventListener('click', () => {
        stopVideoPlayback();
        elements.videoWatch.classList.add('hidden');
    });
    elements.videoWatchPlay?.addEventListener('click', () => state.videoCurrent && playVideo(state.videoCurrent));
    elements.videoWatchQueue?.addEventListener('click', () => state.videoCurrent && addQueue(state.videoCurrent, 'end'));
    elements.videoWatchNext?.addEventListener('click', () => state.videoCurrent && addQueue(state.videoCurrent, 'next'));
    elements.videoWatchRadio?.addEventListener('click', () => state.videoCurrent && startRadio(state.videoCurrent));
    elements.videoPlayer?.addEventListener('playing', () => {
        if (state.videoModeActive) {
            setMediaSessionPlayback('playing');
            renderVideoWatch(state.videoCurrent, 'Đang phát trên thiết bị này');
        }
    });
    elements.videoPlayer?.addEventListener('pause', () => {
        if (state.videoModeActive && !elements.videoPlayer.ended) setMediaSessionPlayback('paused');
    });
    elements.videoPlayer?.addEventListener('timeupdate', () => {
        if (state.videoModeActive) {
            updateMediaSessionPosition(
                elements.videoPlayer.currentTime,
                elements.videoPlayer.duration || state.videoCurrent?.duration || 0,
                elements.videoPlayer.playbackRate || 1
            );
        }
    });
    elements.videoPlayer?.addEventListener('ended', () => {
        if (state.videoModeActive) {
            renderVideoWatch(state.videoCurrent, 'Đang chuyển video tiếp theo...');
            setTimeout(() => playVideoRelative(1), 650);
        }
    });
    elements.videoPlayer?.addEventListener('error', () => {
        if (state.videoModeActive) renderVideoWatch(state.videoCurrent, 'Video không thể phát — thử mở YouTube');
    });
    elements.deviceSelect.addEventListener('change', () => {
        const previousDevice = state.playingDevice;
        state.resolveId += 1;
        stopPlaybackImmediately(previousDevice);
        state.device = elements.deviceSelect.value;
        state.playingDevice = null;
        state.loadingUrl = null;
        state.playingUrl = null;
        if (state.videoModeActive && state.videoCurrent) playVideo(state.videoCurrent);
        localStorage.setItem('youtubeProDevice', state.device);
        elements.player.classList.remove('loading');
        updateTrackStates();
        updatePlayerMode();
        if (state.current) setMessage('Đã đổi thiết bị — chọn bài để phát');
    });
    $$('.bottom-nav button').forEach(button => button.addEventListener('click', () => selectTab(button.dataset.tab)));
    $('#clearQueue').addEventListener('click', clearQueue);
    elements.shuffleQueue?.addEventListener('click', shuffleQueue);
    elements.saveQueue?.addEventListener('click', saveQueue);
    $('#createPlaylist').addEventListener('click', createPlaylist);
    $('#deletePlaylist').addEventListener('click', deletePlaylist);
    $('#clearHistory').addEventListener('click', clearHistory);
    elements.playlistImportButton?.addEventListener('click', importPlaylistFromUrl);
    elements.playlistImportUrl?.addEventListener('keydown', event => {
        if (event.key === 'Enter') { event.preventDefault(); importPlaylistFromUrl(); }
    });
    elements.refreshStats?.addEventListener('click', loadStats);
    $('#favoriteCurrent').addEventListener('click', () => state.current && addFavorite(state.current));
    elements.playerDetails.addEventListener('click', () => state.current && openDetails(state.current, state.playbackContext));
    elements.togglePlayer.addEventListener('click', event => {
        event.stopPropagation();
        setPlayerCollapsed(!state.playerCollapsed);
    });
    $('#playerInfo').addEventListener('click', event => {
        if (state.playerCollapsed && !event.target.closest('button')) setPlayerCollapsed(false);
    });
    $('#previousTrack').addEventListener('pointerdown', () => prefetchRelative(-1), { passive: true });
    $('#nextTrack').addEventListener('pointerdown', () => prefetchRelative(1), { passive: true });
    $('#previousTrack').addEventListener('click', () => playRelative(-1));
    $('#nextTrack').addEventListener('click', () => playRelative(1));
    elements.shuffleToggle.addEventListener('click', () => updatePlaybackModes(state.repeatMode, !state.shuffle));
    elements.repeatToggle.addEventListener('click', () => {
        const next = state.repeatMode === 'off' ? 'all' : state.repeatMode === 'all' ? 'one' : 'off';
        updatePlaybackModes(next, state.shuffle);
    });
    $('#closeDetails').addEventListener('click', closeDetailsDialog);
    elements.detailsDialog.addEventListener('cancel', () => { state.detailsRequestId += 1; });
    elements.detailsDialog.addEventListener('click', event => {
        if (event.target === elements.detailsDialog) closeDetailsDialog();
    });
    elements.detailsPlay.addEventListener('click', () => {
        const track = state.detailsTrack;
        const context = state.detailsContext;
        closeDetailsDialog();
        if (track) playTrack(track, context);
    });
    elements.detailsNext?.addEventListener('click', () => {
        const track = state.detailsTrack;
        closeDetailsDialog();
        if (track) addQueue(track, 'next');
    });
    elements.detailsRadio?.addEventListener('click', () => {
        const track = state.detailsTrack;
        closeDetailsDialog();
        if (track) startRadio(track);
    });
    elements.detailsDialog?.addEventListener('click', event => {
        const button = event.target.closest('[data-feedback-controls] [data-feedback-action]');
        if (button && state.detailsTrack) sendListenerFeedback(button.dataset.feedbackAction, state.detailsTrack);
    });
    elements.audio.addEventListener('ended', () => {
        if (!state.audioPriming) {
            setMediaSessionPlayback('none');
            playRelative(1, true);
        }
    });
    elements.audio.addEventListener('playing', () => {
        if (!state.audioPriming) {
            state.audioUnlocked = true;
            state.playingDevice = 'browser';
            state.loadingUrl = null;
            state.playingUrl = state.current?.url || null;
            updateTrackStates();
            updatePlayerMode();
            setMediaSessionPlayback('playing');
            setMessage('Đang phát trên điện thoại');
        }
    });
    elements.audio.addEventListener('pause', () => {
        if (!state.audioPriming && !elements.audio.ended) setMediaSessionPlayback('paused');
    });
    elements.audio.addEventListener('timeupdate', () => {
        if (!state.audioPriming) {
            highlightLyrics(elements.audio.currentTime);
            updateMediaSessionPosition(
                elements.audio.currentTime,
                elements.audio.duration || state.current?.duration || 0,
                elements.audio.playbackRate || 1
            );
        }
    });
    elements.audio.addEventListener('waiting', () => { if (!state.audioPriming) setMessage('Đang tải thêm dữ liệu...'); });
    elements.audio.addEventListener('error', () => {
        if (!state.audioPriming) {
            setMediaSessionPlayback('none');
            setMessage('Audio lỗi — thử phát lại bài hát');
        }
    });
    $('#sleepButtons').addEventListener('click', event => {
        const minutes = Number(event.target.closest('button')?.dataset.minutes);
        if (minutes) setSleep(minutes);
    });
    $('#cancelSleep').addEventListener('click', cancelSleep);
    elements.timerType.addEventListener('change', toggleTimerFields);
    elements.timerForm.addEventListener('submit', saveTimer);
    elements.remoteControls.addEventListener('click', event => {
        const action = event.target.closest('button')?.dataset.control;
        if (action) remoteControl(action);
    });
    elements.remoteVolume.addEventListener('change', () => setRemoteVolume(elements.remoteVolume.value));
    elements.remoteSeek.addEventListener('pointerdown', () => { state.remoteSeeking = true; });
    elements.remoteSeek.addEventListener('input', () => {
        state.remoteSeeking = true;
        updateRemoteProgress(elements.remoteSeek.value, state.remoteDuration, true);
    });
    elements.remoteSeek.addEventListener('change', () => seekRemote(elements.remoteSeek.value));
    $('#refreshStatus').addEventListener('click', loadStatus);
    elements.refreshLicense.addEventListener('click', () => loadLicense(true));
    elements.licenseGateRefresh.addEventListener('click', () => loadLicense(true));
    [elements.licensePortalLink, elements.licenseGatePortalLink].forEach(link => link?.addEventListener('click', () => {
        if (elements.licenseGateStatus) elements.licenseGateStatus.textContent = 'Chờ xác nhận trên trang kích hoạt';
        state.licenseFastPollUntil = Date.now() + 90 * 1000;
        scheduleLicensePoll({ valid: false });
    }));
    window.addEventListener('focus', async () => {
        if (!state.licensedRuntime) state.licenseFastPollUntil = Date.now() + 60 * 1000;
        const license = await loadLicense(false);
        scheduleLicensePoll(license);
    });
    $$('[data-license-form]').forEach(form => form.addEventListener('submit', activateLicense));
    $$('[data-license-key]').forEach(input => input.addEventListener('input', () => syncLicenseInputs(input)));
    elements.deactivateLicense.addEventListener('click', deactivateLicense);
    $('#resetCastProfile').addEventListener('click', resetCastProfile);
    elements.toggleIntegrationToken.addEventListener('click', toggleIntegrationToken);
    elements.copyIntegrationToken.addEventListener('click', copyIntegrationToken);
    elements.rotateIntegrationToken.addEventListener('click', rotateIntegrationToken);
    elements.listenerProfileSelect?.addEventListener('change', switchListenerProfile);
    elements.createListenerProfile?.addEventListener('click', createListenerProfile);
    elements.renameListenerProfile?.addEventListener('click', renameListenerProfile);
    elements.deleteListenerProfile?.addEventListener('click', deleteListenerProfile);
    elements.playPersonalMix?.addEventListener('click', playPersonalMix);
    elements.refreshPersonalMix?.addEventListener('click', () => loadPersonalMix({ refresh: true }));
    elements.playerFeedback?.addEventListener('click', event => {
        const button = event.target.closest('[data-feedback-action]');
        if (button) sendListenerFeedback(button.dataset.feedbackAction);
    });
    elements.undoFeedback?.addEventListener('click', undoListenerFeedback);
    window.addEventListener('keydown', event => {
        const target = event.target;
        const typing = target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target instanceof HTMLSelectElement;
        if (event.key === '/' && !typing && !event.metaKey && !event.ctrlKey && !event.altKey) {
            event.preventDefault();
            elements.searchInput.focus();
            return;
        }
        if (event.key === 'Escape' && document.activeElement === elements.searchInput) {
            elements.searchInput.blur();
            return;
        }
        if (typing || event.metaKey || event.ctrlKey || event.altKey || event.repeat) return;
        const browser = (state.playingDevice || state.device) === 'browser';
        if (event.code === 'Space') {
            event.preventDefault();
            if (state.videoModeActive) {
                if (elements.videoPlayer.paused) elements.videoPlayer.play().catch(() => null);
                else elements.videoPlayer.pause();
            } else if (browser) {
                if (elements.audio.paused) elements.audio.play().catch(() => null);
                else elements.audio.pause();
            } else {
                remoteControl(state.remoteState === 'playing' ? 'pause' : 'play');
            }
        } else if (event.key === 'n') {
            state.videoModeActive ? playVideoRelative(1) : playRelative(1);
        } else if (event.key === 'p') {
            state.videoModeActive ? playVideoRelative(-1) : playRelative(-1);
        } else if (event.key === 'ArrowRight' && !state.videoModeActive) {
            event.preventDefault();
            mediaSessionSeekTarget(10);
        } else if (event.key === 'ArrowLeft' && !state.videoModeActive) {
            event.preventDefault();
            mediaSessionSeekTarget(-10);
        }
    });
    window.addEventListener('scroll', () => {
        maybeLoadMore();
        maybeLoadMoreVideos();
    }, { passive: true });
}

function stopLicensedRuntime() {
    if (!state.licensedRuntime) return;
    state.licensedRuntime = false;
    try { state.eventSource?.close(); } catch (_) {}
    state.eventSource = null;
    if (state.videoModeActive) stopVideoPlayback();
    stopRemoteProgressPolling();
    clearInterval(state.sleepPollInterval);
    clearInterval(state.progressInterval);
    clearInterval(state.devicePollInterval);
    state.sleepPollInterval = null;
    state.progressInterval = null;
    state.devicePollInterval = null;
    if (!elements.audio.paused) elements.audio.pause();
}

async function startLicensedRuntime() {
    if (state.licensedRuntime) return;
    state.licensedRuntime = true;
    setupEventStream();
    await Promise.all([loadDevices(), loadPlaylists(), loadQueue(), loadHistory()]);
    void loadStats();
    toggleTimerFields();
    await search(true);
    void loadListenerPreferences();
    await loadSleep();
    await loadStatus();
    if (!state.licensedRuntime) return;
    state.sleepPollInterval = setInterval(loadSleep, 5000);
    state.progressInterval = setInterval(tickRemoteProgress, 500);
    state.devicePollInterval = setInterval(loadDevices, 30000);
}

async function init() {
    applyTheme(document.documentElement.dataset.theme || 'dark', false);
    setupMediaSession();
    updatePlaybackModeButtons();
    bindEvents();
    setPlayerCollapsed(state.playerCollapsed, false);
    setupInfiniteScroll();
    const bootstrap = readLicenseBootstrap();
    if (bootstrap?.valid && renderLicense(bootstrap)) void startLicensedRuntime();
    const license = await loadLicense(false);
    scheduleLicensePoll(license);
}

init();
