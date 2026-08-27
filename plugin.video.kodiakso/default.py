# -*- coding: utf-8 -*-
import time
import sys
import re
import json
import base64
import gzip
import io
import zipfile
import os
import pickle
import hashlib
import hmac
import html
import uuid
import threading
import urllib.parse
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree as ET
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import requests

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE = sys.argv[0]
NAME = ADDON.getAddonInfo('name')

DEFAULT_URL = 'https://luishighnest.github.io/kodi/playlist.m3u'
REPO_BASE = 'https://luishighnest.github.io/kodi'
PLAYLIST_URL = ADDON.getSetting('playlist_url').strip() or DEFAULT_URL
PLAYLIST_TS = ADDON.getSetting('playlist_timestamp') == 'true'

API = ADDON.getSetting('sky_api').strip() or 'https://test34344.herokuapp.com/filter.php'
SECRET = b'my_secret_key'
API_UA = ADDON.getSetting('sky_api_ua').strip() or 'Kodi/19.0 (Windows NT 10.0; Win64; x64) App_Bitness/64 Version/19.0-Matrix'

UA = ADDON.getSetting('sky_stream_ua').strip() or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
HOST = ADDON.getSetting('sky_host').strip() or 'https://www.nowtv.it'
LOGO_BASE = 'https://luishighnest.github.io/kodi/logos/'
SQUARE_ICON = LOGO_BASE + 'square.png'
SEARCH_ICON = LOGO_BASE + 'search.png'
HOME_ICON = LOGO_BASE + 'home.png'
BACK_ICON = LOGO_BASE + 'back.png?v=3'
LABEL = '[B][COLOR snow]%s[/COLOR][/B]'
BANNER_LOGO = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'banner.png')
ICON_LOGO = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'icon.png')
EMPTY_LOGO = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'empty.png')
_VOD_SRC = ''
VIXSRC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'

EPG_URL_DEFAULT = 'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'
EPG_KEEP_HOURS = 6
_EPG_SESSION = {'data': None}

EXP_OK_COLOR = '00FF00'
EXP_SOON_COLOR = 'FFFF00'
EXP_EXP_COLOR = 'FF0000'
EXP_SOON_MINS = 60
_SKY_SESS = requests.Session()
_SKY_SESS.headers['User-Agent'] = API_UA
_EXP_CACHE = {}
_EXP_CACHE_DIRTY = False
_EXP_CACHE_TTL = 180
_EXP_CACHE_TTL_FAIL = 60

# === VAVOO AUTH (OwnerPlugins/vavoo - port for Kodi) ===
_VAVOO_PING_URL = 'https://www.vavoo.tv/api/app/ping'
_VAVOO_PING_URL2 = 'https://www.vypn.net/api/app/ping'
_VAVOO_VYPN_PKG = 'net.vypn.app'
_VAVOO_VYPN_VER = '1.4.1'
_VAVOO_BASES = ['https://vavoo.to', 'https://kool.to']
_VAVOO_SIG = {'sig': None, 'ts': 0}
_VAVOO_CAT_CACHE = {'data': None, 'ts': 0, 'sig': ''}
_VAVOO_CAT_TTL = 1800
_VAVOO_RESOLVE_CACHE = {}
_VAVOO_RESOLVE_TTL = 300

# === HTSPORT (Hattrick Sport) eventi ===
HTSPORT_BASE = 'https://htsport.org'
HTSPORT_INDEX = 'https://htsport.org/index.htm'
HTSPORT_TTL = 600
_HT = {'data': None, 'ts': 0}
_HT_RES = {'data': {}, 'ts': {}}
_HT_RES_TTL = 300

# === EVENTI 5 (Canali Sport 24/7 da iptv-org) ===
SPORTS_PLAYLIST_URL = 'https://iptv-org.github.io/iptv/categories/sports.m3u'
SPORTS_TTL = 21600
_SPORTS = {'data': None, 'ts': 0}


def _vavoo_rewrite_sig_ip(sig):
    try:
        padded = sig + '=' * (-len(sig) % 4)
        dec = base64.b64decode(padded).decode('utf-8')
        obj = json.loads(dec)
        if not isinstance(obj, dict) or 'data' not in obj:
            return sig
        data = json.loads(obj['data'])
        try:
            ip = requests.get('https://api.ipify.org', timeout=8).text.strip()
        except Exception:
            return sig
        if not ip:
            return sig
        ips = data.get('ips')
        if not isinstance(ips, list):
            ips = []
        data['ips'] = [ip] + [x for x in ips if x and x != ip]
        if isinstance(data.get('ip'), str):
            data['ip'] = ip
        obj['data'] = json.dumps(data)
        nsig = base64.b64encode(json.dumps(obj).encode('utf-8')).decode('ascii')
        return nsig
    except Exception:
        return sig


def _vavoo_get_sig(force=False):
    now = time.time()
    if not force and _VAVOO_SIG['sig'] and (now - _VAVOO_SIG['ts'] < 480):
        return _VAVOO_SIG['sig']
    try:
        uid = str(uuid.uuid4())
        ts = int(time.time() * 1000)
        payload = {
            'token': '', 'reason': 'app-focus', 'locale': 'it', 'theme': 'dark',
            'metadata': {'device': {'type': 'phone', 'uniqueId': uid}, 'os': {'name': 'android', 'version': '14', 'abis': ['arm64-v8a'], 'host': 'android'}, 'app': {'platform': 'android'}, 'version': {'package': _VAVOO_VYPN_PKG, 'binary': _VAVOO_VYPN_VER, 'js': _VAVOO_VYPN_VER}},
            'appFocusTime': 0, 'playerActive': False, 'playDuration': 0, 'devMode': False, 'hasAddon': True, 'castConnected': False,
            'package': _VAVOO_VYPN_PKG, 'version': _VAVOO_VYPN_VER, 'process': 'app', 'firstAppStart': ts - 86400000, 'lastAppStart': ts,
            'ipLocation': None, 'adblockEnabled': True, 'migrationApplied': False, 'migrationTargetInstalled': False,
            'proxy': {'supported': ['ss'], 'engine': 'Mu', 'ssVersion': '2022', 'enabled': False, 'autoServer': True, 'id': ''},
            'iap': {'supported': False, 'error': ''}}
        headers = {'user-agent': 'okhttp/4.11.0', 'accept': 'application/json', 'content-type': 'application/json; charset=utf-8', 'accept-encoding': 'gzip'}
        sig = None
        for url in [_VAVOO_PING_URL, _VAVOO_PING_URL2]:
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                if r.status_code == 200:
                    j = r.json()
                    sig = j.get('addonSig') or j.get('mhub')
                    if sig:
                        break
            except Exception:
                continue
        if sig:
            sig = _vavoo_rewrite_sig_ip(sig)
            _VAVOO_SIG['sig'] = sig
            _VAVOO_SIG['ts'] = now
            return sig
    except Exception as e:
        log('vavoo sig ERR: ' + str(e))
    return _VAVOO_SIG['sig']


def _vavoo_catalog():
    now = time.time()
    if _VAVOO_CAT_CACHE['data'] is not None and (now - _VAVOO_CAT_CACHE['ts'] < _VAVOO_CAT_TTL):
        return _VAVOO_CAT_CACHE['data']
    sig = _vavoo_get_sig()
    if not sig:
        return []
    all_ch = []
    cursor = None
    for page in range(15):
        ok = False
        for base in _VAVOO_BASES:
            try:
                h = {'content-type': 'application/json; charset=utf-8', 'mediahubmx-signature': sig, 'user-agent': 'MediaHubMX/2', 'accept': '*/*', 'Accept-Language': 'it', 'Accept-Encoding': 'gzip, deflate'}
                body = {'language': 'it', 'region': 'IT', 'catalogId': 'iptv', 'id': 'iptv', 'adult': False, 'search': '', 'sort': '', 'filter': {}, 'cursor': cursor, 'clientVersion': '3.0.2'}
                r = requests.post(base + '/mediahubmx-catalog.json', json=body, headers=h, timeout=30)
                if r.status_code == 451:
                    continue
                r.raise_for_status()
                j = r.json()
                items = j.get('items', [])
                if items:
                    all_ch.extend(items)
                cursor = j.get('nextCursor')
                ok = True
                break
            except Exception as e:
                log('vavoo catalog %s: %s' % (base, e))
                continue
        if not ok or not cursor:
            break
    _VAVOO_CAT_CACHE['data'] = all_ch
    _VAVOO_CAT_CACHE['ts'] = now
    _VAVOO_CAT_CACHE['sig'] = sig
    return all_ch


def _vavoo_resolve(play_url):
    now = time.time()
    hit = _VAVOO_RESOLVE_CACHE.get(play_url)
    if hit and (now - hit[0] < _VAVOO_RESOLVE_TTL):
        return hit[1]
    sig = _vavoo_get_sig()
    if not sig:
        return None
    for attempt in range(2):
        for base in _VAVOO_BASES:
            try:
                h = {'content-type': 'application/json; charset=utf-8', 'mediahubmx-signature': sig, 'user-agent': 'MediaHubMX/2', 'accept': '*/*', 'Accept-Language': 'it', 'Accept-Encoding': 'gzip, deflate'}
                body = {'language': 'it', 'region': 'IT', 'url': play_url, 'clientVersion': '3.0.2'}
                r = requests.post(base + '/mediahubmx-resolve.json', json=body, headers=h, timeout=20)
                if r.status_code == 451:
                    continue
                r.raise_for_status()
                j = r.json()
                stream = None
                if isinstance(j, list) and j:
                    stream = j[0].get('url')
                elif isinstance(j, dict):
                    stream = j.get('url') or j.get('streamUrl')
                if stream:
                    _VAVOO_RESOLVE_CACHE[play_url] = (now, stream)
                    return stream
            except Exception as e:
                log('vavoo resolve %s: %s' % (base, e))
                continue
        sig = _vavoo_get_sig(force=True)
        if not sig:
            break
    return None


def lbl(txt):
    if not isinstance(txt, str):
        txt = str(txt)
    txt = html.unescape(txt)
    return LABEL % txt


def _top_button(label, icon, url):
    li = xbmcgui.ListItem(label=lbl(label))
    li.setArt({'thumb': icon})
    li.setProperty('IsPlayable', 'false')
    nav = BASE + '?action=nav&url=' + urllib.parse.quote(url, safe='')
    xbmcplugin.addDirectoryItem(HANDLE, nav, li, isFolder=False)


def home_button():
    _top_button('Home', HOME_ICON, BASE + '?action=root')


def back_button(url=''):
    if not url:
        url = BASE + '?action=root'
    _top_button('Indietro', BACK_ICON, url)

LOGOS = {
    'tg24': 'skytg24.png',
    'skyuno': 'skyuno.png',
    'skyunoplus': 'skyunoplus.png',
    'skyatlantic': 'skyatlantic.png',
    'skyserie': 'skyserie.png',
    'skycollection': 'skycollection.png',
    'skyinvestigation': 'skyinvestigation.png',
    'skyadventure': 'skyadventure.png',
    'skycrime': 'skycrime.png',
    'skydocumentaries': 'skydocumentaries.png',
    'skynature': 'skynature.png',
    'historychannel': 'history.png',
    'comedycentral': 'comedycentral.png',
    'skyarte': 'skyarte.png',
    'mtv': 'mtv.png',
    'skysportuno': 'sksportuno.png',
    'skysport24': 'sksport24.png',
    'skysportarena': 'sksportarena.png',
    'skysportbasket': 'sksportbasket.png',
    'skysportcalcio': 'sksportcalcio.png',
    'skysportf1': 'sksportf1.png',
    'skysportgolf': 'sksportgolf.png',
    'skysportlegend': 'sksportlegend.png',
    'skysportmax': 'sksportmax.png',
    'skysportmix': 'sksportmix.png',
    'skysportmotogp': 'sksportmotogp.png',
    'skysporttennis': 'sksporttennis.png',
    'skysport251': 'sksport.png',
    'skysport252': 'sksport.png',
    'skysport253': 'sksport.png',
    'skysport254': 'sksport.png',
    'skysport255': 'sksport.png',
    'skysport256': 'sksport.png',
    'skysport257': 'sksport.png',
    'skysport258': 'sksport.png',
    'skysport259': 'sksport.png',
}

CAT_INT = 'SKY INTRATTENIMENTO'
CAT_SPORT = 'SKY SPORT'

_GUIDA = [
    ('Serie A', 'italy/serie-a', '', 'DAZN | Sky Sport Calcio, Sky Sport 251, NOW'),
    ('Serie B', 'italy/serie-b', '', 'DAZN | Amazon LaB Channel | OneFootball TV'),
    ('Coppa Italia', 'italy/coppa-italia', '', 'Mediaset Canale 5 / Italia 1 | DAZN'),
    ('Supercoppa Italiana', 'italy/supercoppa-italiana', '', 'Mediaset | DAZN'),
    ('Champions League', 'international/uefa-champions-league', '', 'Sky | NOW | Amazon 18 gare | TV8 estero'),
    ('Europa League', 'international/uefa-europa-league', '', 'Sky | NOW | Diretta Gol'),
    ('Conference League', 'international/uefa-europa-conference-league', '', 'Sky | NOW'),
    ('Premier League', 'england/premier-league', '', 'Sky fino 2028 | NOW | TV8'),
    ('LaLiga', 'spain/primera-division', '', 'DAZN fino 2029'),
    ('Bundesliga', 'germany/bundesliga', '', 'Sky fino 2029 | NOW'),
    ('Ligue 1', 'france/ligue-1', '', 'Sky | NOW'),
    ('Primeira Liga', 'portugal/liga-sagres', '', 'DAZN | Sky'),
    ('Eredivisie', 'netherlands/eredivisie', '', 'Como TV (gratis)'),
    ('Saudi Pro League', 'saudi-arabia/saudi-pro-league', '', 'Como TV'),
    ('FA Cup', 'england/fa-cup', '', 'DAZN | Sky'),
]

SKY_DEFS = {
    'tg24': ('Sky TG 24', CAT_INT),
    'skyuno': ('Sky Uno', CAT_INT),
    'skyunoplus': ('Sky Uno +1', CAT_INT),
    'skyatlantic': ('Sky Atlantic', CAT_INT),
    'skyserie': ('Sky Serie', CAT_INT),
    'skycollection': ('Sky Collection', CAT_INT),
    'skyinvestigation': ('Sky Investigation', CAT_INT),
    'skyadventure': ('Sky Adventure', CAT_INT),
    'skycrime': ('Sky Crime', CAT_INT),
    'skydocumentaries': ('Sky Documentaries', CAT_INT),
    'skynature': ('Sky Nature', CAT_INT),
    'historychannel': ('History', CAT_INT),
    'comedycentral': ('Comedy Central', CAT_INT),
    'skyarte': ('Sky Arte', CAT_INT),
    'mtv': ('MTV', CAT_INT),
    'skysportuno': ('Sky Sport Uno', CAT_SPORT),
    'skysport24': ('Sky Sport 24', CAT_SPORT),
    'skysportarena': ('Sky Sport Arena', CAT_SPORT),
    'skysportbasket': ('Sky Sport Basket', CAT_SPORT),
    'skysportcalcio': ('Sky Sport Calcio', CAT_SPORT),
    'skysportf1': ('Sky Sport F1', CAT_SPORT),
    'skysportgolf': ('Sky Sport Golf', CAT_SPORT),
    'skysportlegend': ('Sky Sport Legend', CAT_SPORT),
    'skysportmax': ('Sky Sport Max', CAT_SPORT),
    'skysportmix': ('Sky Sport Mix', CAT_SPORT),
    'skysportmotogp': ('Sky Sport MotoGP', CAT_SPORT),
    'skysporttennis': ('Sky Sport Tennis', CAT_SPORT),
}


def log(m):
    xbmc.log('KODIAKSO: ' + m, xbmc.LOGINFO)


def _sky_name(cid):
    disp = SKY_DEFS.get(cid, ('', ''))[0]
    if cid.startswith('skysport'):
        m = re.match(r'^skysport(.+)$', cid)
        rest = m.group(1) if m else ''
        return ('SPORT ' + rest).upper()
    return disp.upper() if disp else cid.upper()


def xor_decrypt(b64data):
    data = base64.b64decode(b64data)
    out = bytes(b ^ SECRET[i % len(SECRET)] for i, b in enumerate(data))
    return out.decode('utf-8')


def strip_color(txt):
    if not isinstance(txt, str):
        txt = str(txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\[COLOR.*?\]', '', txt, flags=re.IGNORECASE)
    txt = re.sub(r'\[/COLOR\]', '', txt, flags=re.IGNORECASE)
    return txt.strip()


def clean_title(txt):
    txt = strip_color(txt)
    txt = re.sub(r'\bFHD\b', '', txt, flags=re.IGNORECASE)
    txt = re.sub(r'\s{2,}', ' ', txt).strip()
    return txt


def get_playlist():
    url = PLAYLIST_URL
    if PLAYLIST_TS:
        url += ('&' if '?' in url else '?') + '_=' + str(int(time.time()))
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def notify(title, msg, err=False):
    if ADDON.getSetting('show_warnings') == 'true' or not err:
        xbmcgui.Dialog().notification(title, msg, xbmcgui.NOTIFICATION_ERROR if err else xbmcgui.NOTIFICATION_INFO)


def fetch_channels():
    try:
        return parse_m3u(get_playlist())
    except Exception:
        notify(NAME, 'Impossibile scaricare la playlist', True)
        return []


def parse_m3u(text):
    channels = []
    props = {}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('#KODIPROP:'):
            key, _, value = line[len('#KODIPROP:'):].partition('=')
            props[key.strip()] = urllib.parse.unquote(value.strip().strip('"'))
        elif line.startswith('#EXTINF:'):
            meta = line[8:]
            label = clean_title(meta.partition(',')[2])
            current = {'label': label, 'logo': '', 'group': 'Altri', 'props': {}}
            m = re.search(r'tvg-logo="([^"]*)"', meta)
            if m:
                current['logo'] = m.group(1)
            m = re.search(r'group-title="([^"]*)"', meta)
            if m:
                current['group'] = m.group(1)
        elif not line.startswith('#') and current is not None:
            current['url'] = line
            current['props'] = dict(props)
            channels.append(current)
            current = None
            props = {}
    return channels


def sky_channels():
    order = []
    seen = set()

    def push(cid):
        if cid not in seen:
            seen.add(cid)
            order.append(cid)

    try:
        data = _SKY_SESS.get(API + '?numTest=A1A260', timeout=15).json()
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            mr = it.get('myresolve', '') or ''
            if mr.startswith('sky@@'):
                push(mr.split('@@', 1)[1])
    except Exception as e:
        log('sky A1A260 fail: ' + str(e))
    try:
        data = _SKY_SESS.get(API + '?numTest=A1A122', timeout=15).json()
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            title = clean_title(it.get('title', ''))
            if 'Sky' in title and ('IT:' in title or 'IT ' in title):
                clean = title.replace('IT:', '').replace('IT', '').strip().replace('  ', ' ')
                cid = clean.replace(' ', '').lower()
                if cid == 'skytg24':
                    cid = 'tg24'
                push(cid)
    except Exception as e:
        log('sky A1A122 fail: ' + str(e))
    for cid in SKY_DEFS:
        push(cid)
    for n in range(251, 260):
        push('skysport%d' % n)
    channels = {CAT_INT: [], CAT_SPORT: []}
    for cid in order:
        name = _sky_name(cid)
        cat = SKY_DEFS.get(cid, (cid, CAT_SPORT if cid.startswith('skysport') else CAT_INT))[1]
        channels[cat].append((name, cid))
    return channels


def _profile_path():
    p = ADDON.getAddonInfo('profile')
    try:
        return xbmc.translatePath(p)
    except Exception:
        return p


def _exp_cache_path():
    return os.path.join(_profile_path(), 'exp_cache.pkl')


def _exp_cache_load():
    try:
        if os.path.exists(_exp_cache_path()):
            with open(_exp_cache_path(), 'rb') as f:
                return pickle.load(f)
    except Exception:
        pass
    return {}


def _exp_cache_save(c):
    try:
        d = os.path.dirname(_exp_cache_path())
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(_exp_cache_path(), 'wb') as f:
            pickle.dump(c, f)
    except Exception:
        pass


def _parse_fine(fine):
    if not fine or 'EXPIRE' in fine:
        return None
    m = re.match(r'(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})', fine)
    if not m:
        return None
    g = m.groups()
    try:
        return datetime(int(g[2]), int(g[1]), int(g[0]), int(g[3]), int(g[4]), int(g[5]))
    except ValueError:
        return None


def _exp_status(exp):
    if exp is None:
        return None
    now = datetime.now()
    if exp < now:
        return 'exp'
    if exp <= now + timedelta(minutes=EXP_SOON_MINS):
        return 'soon'
    return 'ok'


def _exp_color(st):
    if st == 'ok':
        return EXP_OK_COLOR
    if st == 'soon':
        return EXP_SOON_COLOR
    if st == 'exp':
        return EXP_EXP_COLOR
    return ''


def _exp_col(exp):
    st = _exp_status(exp) or 'ok'
    if st == 'soon':
        return EXP_SOON_COLOR
    if st == 'exp':
        return 'FF6B6B'
    return '00FF00'


def _sky_epg_label(cur):
    name = ' '.join(str(cur[2]).split())
    return '%02d:%02d %s' % (cur[0].hour, cur[0].minute, name)


def _sky_parts(title, exp, prog=''):
    full = title
    l2 = ''
    t = ''
    if prog:
        full += ' \u2022 %s' % prog
        l2 = '[COLOR 00FF00]%s[/COLOR]' % prog
    if exp:
        t = exp.strftime('%d/%m %H:%M')
        tf = exp.strftime('%d/%m/%Y %H:%M')
        full += ' \u2022 %s' % t
        l2 = ((l2 + '    ') if l2 else '') + '[COLOR %s]SCADENZA %s[/COLOR]' % (_exp_col(exp), tf)
    label = full
    tname = title
    if exp:
        tname += ' | SCADENZA %s' % tf
    return label, l2, tname


def _sky_expiry(cid):
    t = time.time()
    hit = _EXP_CACHE.get(cid)
    if hit:
        ts, exp = hit
        ttl = _EXP_CACHE_TTL if exp is not None else _EXP_CACHE_TTL_FAIL
        if t - ts < ttl:
            return exp
    disk = _exp_cache_load()
    if not _EXP_CACHE:
        _EXP_CACHE.update(disk)
    hit = disk.get(cid)
    if hit:
        ts, exp = hit
        ttl = _EXP_CACHE_TTL if exp is not None else _EXP_CACHE_TTL_FAIL
        if t - ts < ttl:
            _EXP_CACHE[cid] = (ts, exp)
            return exp
    exp = None
    try:
        resp = _SKY_SESS.get(API + '?numTest=A1A159&id=' + urllib.parse.quote(cid), timeout=20)
        resp.raise_for_status()
        data = json.loads(xor_decrypt(resp.json()['data']))
        exp = _parse_fine(data.get('fine', ''))
        if exp:
            exp += timedelta(hours=2)
    except Exception as e:
        xbmc.log('KODIAKSO sky expiry ERR %s: %s' % (cid, e), xbmc.LOGERROR)
        try:
            import traceback
            xbmc.log('KODIAKSO sky expiry TB:\n' + traceback.format_exc(), xbmc.LOGERROR)
        except Exception:
            pass
    _EXP_CACHE[cid] = (time.time(), exp)
    global _EXP_CACHE_DIRTY
    _EXP_CACHE_DIRTY = True
    return exp


def resolve_sky(parIn, title, prog=''):
    try:
        resp = requests.get(API + '?numTest=A1A159&id=' + urllib.parse.quote(parIn),
                            headers={'User-Agent': API_UA}, timeout=20)
        resp.raise_for_status()
        data = json.loads(xor_decrypt(resp.json()['data']))
    except Exception as e:
        xbmc.log('KODIAKSO sky resolve ERR: ' + str(e), xbmc.LOGERROR)
        notify(title or parIn, 'Errore risoluzione link', True)
        return xbmcgui.ListItem()

    manifest = data['manifest']
    kid = data['kid']
    key = data['key']
    fine = data.get('fine', '')
    exp = _parse_fine(fine)
    if exp:
        exp += timedelta(hours=2)
        if exp < datetime.now():
            notify(title or parIn, 'Link scaduto ' + exp.strftime('%d/%m/%Y %H:%M:%S'), True)

    hdrs = 'User-Agent=' + UA + '&Referer=' + HOST + '/&Origin=' + HOST + '&verifypeer=false'
    li = xbmcgui.ListItem(path=manifest, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    li.setProperty('inputstream.adaptive.drm_legacy', 'org.w3.clearkey|' + kid + ':' + key)
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    if ADDON.getSetting('live_async') == 'true':
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    if ADDON.getSetting('manifest_upd') == 'true':
        li.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    pname = title
    if parIn.startswith('skysport') and not pname.upper().startswith('SKY'):
        pname = 'SKY ' + pname

    cur_prog = (prog or '').strip()
    if not cur_prog:
        try:
            cur, _ = _epg_now(parIn)
            if cur and cur[2]:
                cur_prog = str(cur[2]).strip()
        except Exception:
            pass

    if cur_prog:
        pname = pname + ' • ' + cur_prog

    li.setLabel(pname)
    li.setInfo('video', {'title': pname})
    return li


def group_view(group, deep=False, back=''):
    if deep:
        back_button(back or (BASE + '?action=tv'))
    else:
        home_button()
    channels = fetch_channels()
    for ch in channels:
        if ch['group'] != group:
            continue
        li = xbmcgui.ListItem(label=lbl(ch['label']), path=ch['url'])
        if ch['logo']:
            logo = ch['logo']
            if logo.startswith('/logos/'):
                logo = LOGO_BASE + logo[len('/logos/'):]
            li.setArt({'thumb': logo})
        else:
            li.setArt({'thumb': SQUARE_ICON})
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        for k, v in ch['props'].items():
            if k == 'inputstream' and not v:
                continue
            li.setProperty(k, v)
        xbmcplugin.addDirectoryItem(HANDLE, ch['url'], li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def gsearch_view(q=''):
    did_kbd = False
    if not q:
        kb = xbmc.Keyboard('', 'Ricerca globale (canali ed eventi)')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            xbmcplugin.endOfDirectory(HANDLE)
            return
        q = kb.getText().strip()
        did_kbd = True
    ql = q.lower()
    search_back = BASE + '?action=gsearch&q=' + urllib.parse.quote(q)
    home_button()
    added = 0

    def header(txt):
        li = xbmcgui.ListItem(label=lbl(txt))
        li.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)

    try:
        chs = fetch_channels()
    except Exception:
        chs = []
    matches = [c for c in chs if ql in c['label'].lower()]
    if matches:
        header('[COLOR A9A9A9]Canali (%d)[/COLOR]' % len(matches))
        for c in matches:
            li = xbmcgui.ListItem(label=lbl(c['label']), path=c['url'])
            if c['logo']:
                logo = c['logo']
                if logo.startswith('/logos/'):
                    logo = LOGO_BASE + logo[len('/logos/'):]
                li.setArt({'thumb': logo})
            else:
                li.setArt({'thumb': SQUARE_ICON})
            li.setProperty('isPlayable', 'true')
            li.setProperty('inputstream', 'inputstream.adaptive')
            for k, v in c['props'].items():
                if k == 'inputstream' and not v:
                    continue
                li.setProperty(k, v)
            xbmcplugin.addDirectoryItem(HANDLE, c['url'], li, isFolder=False)
            added += 1

    skyall = []
    for cat in (CAT_INT, CAT_SPORT):
        try:
            skyall += sky_channels().get(cat, [])
        except Exception:
            pass
    sm = [x for x in skyall if ql in x[0].lower()]
    if sm:
        header('[COLOR A9A9A9]Sky (%d)[/COLOR]' % len(sm))
        for t, cid in sm:
            try:
                exp = _sky_expiry(cid)
                label, l2, tname = _sky_parts(t, exp)
            except Exception:
                exp = None
                label, l2, tname = t, '', t
            li = xbmcgui.ListItem(label=label)
            if l2:
                li.setLabel2(l2)
            logo = LOGOS.get(cid, '')
            li.setArt({'thumb': (LOGO_BASE + logo) if logo else SQUARE_ICON})
            li.setProperty('isPlayable', 'true')
            li.setInfo('video', {'title': tname})
            url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(t)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
            added += 1

    try:
        evs = _szx_load('events', 'events.json')
    except Exception:
        evs = []
    em = [e for e in evs if ql in (e.get('title') or '').lower()]
    if em:
        header('[COLOR A9A9A9]Sportzx (%d)[/COLOR]' % len(em))
        for e in em:
            title = e.get('title') or ''
            li = xbmcgui.ListItem(label=lbl(title))
            li.setProperty('isPlayable', 'false')
            url = _tmdb_url('szx_event', id=str(e.get('id', '')), back=search_back)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
            added += 1

    dc = []
    dm = []
    try:
        cats = _daddy_fetch()
    except Exception:
        cats = []
    for idx, c in enumerate(cats):
        cname = strip_color(c.get('name') or '')
        if cname and ql in cname.lower():
            dc.append((cname, idx))
        for it in c.get('items') or []:
            t = strip_color(it.get('title') or '')
            mr = it.get('myresolve') or ''
            code = mr.split('@@', 1)[1] if '@@' in mr else ''
            if t and code and ql in t.lower():
                dm.append((t, code))
    if dc:
        header('[COLOR A9A9A9]Daddy - Categorie (%d)[/COLOR]' % len(dc))
        for cname, idx in dc:
            li = xbmcgui.ListItem(label=lbl(cname))
            xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy_cat', i=str(idx)), li, isFolder=True)
            added += 1
    if dm:
        header('[COLOR A9A9A9]Daddy - Eventi (%d)[/COLOR]' % len(dm))
        for t, code in dm:
            li = xbmcgui.ListItem(label=lbl(t))
            li.setProperty('isPlayable', 'true')
            xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy_play', c=code), li, isFolder=False)
            added += 1

    if not added:
        li = xbmcgui.ListItem(label=lbl('Nessun risultato per "%s"' % q))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)
    if did_kbd:
        xbmc.executebuiltin('Container.Update("%s", replace)' % _tmdb_url('gsearch', q=q))


def _sky_counts(cat):
    counts = {'ok': 0, 'soon': 0, 'exp': 0}
    for title, cid in sky_channels().get(cat, []):
        st = _exp_status(_sky_expiry(cid)) or 'ok'
        counts[st] = counts.get(st, 0) + 1
    return counts


def resolve_vavoo(url, title='', prog=''):
    try:
        pname = title or ''
        cur_prog = (prog or '').strip()
        if not cur_prog:
            try:
                cur, _ = _epg_now(title)
                if cur and len(cur) >= 3 and cur[2]:
                    cur_prog = str(cur[2]).strip()
            except Exception:
                pass
        if cur_prog:
            pname = pname + ' \u2022 ' + cur_prog
        # url is the vavoo play URL (https://vavoo.to/vavoo-iptv/play/...), resolve to HLS
        stream = _vavoo_resolve(url) if url else None
        if not stream:
            notify(title or 'SKY 2', 'Impossibile risolvere lo stream Vavoo', True)
            return xbmcgui.ListItem()
        li = xbmcgui.ListItem(path=stream, label=lbl(pname), offscreen=True)
        li.setContentLookup(False)
        li.setMimeType('application/x-mpegURL')
        li.setProperty('inputstream', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', 'hls')
        # Vavoo HLS non richiede header firmati, UA generico
        hdrs = 'User-Agent=%s' % UA
        li.setProperty('inputstream.adaptive.stream_headers', hdrs)
        li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
        li.setInfo('video', {'title': pname, 'tvshowtitle': '', 'season': 0, 'episode': 0, 'mediatype': 'video'})
        return li
    except Exception as e:
        xbmc.log('KODIAKSO vavoo resolve ERR: ' + str(e), xbmc.LOGERROR)
        return xbmcgui.ListItem()


def sky_view():
    home_button()
    # Lista Canali 1 - SKY SPORT diretto (ex SKY 1)
    try:
        c = _sky_counts(CAT_SPORT)
        label_sport = lbl('Lista Canali 1 - ' + CAT_SPORT) + ' | CANALI ATTIVI: %d \u2022 CANALI IN SCADENZA: %d \u2022 CANALI SCADUTI: %d' % (c.get('ok', 0), c.get('soon', 0), c.get('exp', 0))
    except Exception:
        label_sport = lbl('Lista Canali 1 - ' + CAT_SPORT)
    li0 = xbmcgui.ListItem(label=label_sport)
    li0.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li0.setInfo('video', {'title': 'Lista Canali 1 - ' + CAT_SPORT, 'plot': 'Canali Sky Sport Italia'})
    url0 = BASE + '?action=skycat&cat=' + urllib.parse.quote(CAT_SPORT) + '&back=' + urllib.parse.quote(BASE + '?action=sky')
    xbmcplugin.addDirectoryItem(HANDLE, url0, li0, isFolder=True)

    sky2_url = BASE + '?action=sky2'
    li2 = xbmcgui.ListItem(label=lbl('Lista Canali 2'))
    li2.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li2.setInfo('video', {'title': 'Lista Canali 2', 'plot': 'Canali Sky Italia 24/7'})
    xbmcplugin.addDirectoryItem(HANDLE, sky2_url, li2, isFolder=True)

    sky3_url = BASE + '?action=sky3'
    li3 = xbmcgui.ListItem(label=lbl('Lista Canali 3'))
    li3.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li3.setInfo('video', {'title': 'Lista Canali 3', 'plot': 'Eventi live esclusivamente Sky Sport Italia'})
    xbmcplugin.addDirectoryItem(HANDLE, sky3_url, li3, isFolder=True)

    sky4_url = BASE + '?action=sky4'
    li4 = xbmcgui.ListItem(label=lbl('Lista Canali 4'))
    li4.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li4.setInfo('video', {'title': 'Lista Canali 4', 'plot': 'Eventi HD7/HD8 ITALIAN'})
    xbmcplugin.addDirectoryItem(HANDLE, sky4_url, li4, isFolder=True)

    sky5_url = BASE + '?action=sky5'
    li5 = xbmcgui.ListItem(label=lbl('Lista Canali 5'))
    li5.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li5.setInfo('video', {'title': 'Lista Canali 5', 'plot': 'Eventi CalcioStreaming DiretteCommunity'})
    xbmcplugin.addDirectoryItem(HANDLE, sky5_url, li5, isFolder=True)

    sky6_url = BASE + '?action=sky6'
    li6 = xbmcgui.ListItem(label=lbl('Lista Canali 6 (MPD)'))
    li6.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li6.setInfo('video', {'title': 'Lista Canali 6 (MPD)', 'plot': 'Categoria vuota'})
    xbmcplugin.addDirectoryItem(HANDLE, sky6_url, li6, isFolder=True)

    sky7_url = BASE + '?action=sky7'
    li7 = xbmcgui.ListItem(label=lbl('Lista Canali 7 (IPTV)'))
    li7.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
    li7.setInfo('video', {'title': 'Lista Canali 7 (IPTV)', 'plot': 'Canali live IPTV Xtream'})
    xbmcplugin.addDirectoryItem(HANDLE, sky7_url, li7, isFolder=True)

    xbmcplugin.endOfDirectory(HANDLE)


_FLAGS = {
    'Australia': 'https://flagcdn.com/w80/au.png',
    'Brasile': 'https://flagcdn.com/w80/br.png',
    'USA': 'https://flagcdn.com/w80/us.png',
    'Irlanda': 'https://flagcdn.com/w80/ie.png',
    'Paesi Bassi': 'https://flagcdn.com/w80/nl.png',
    'Slovacchia': 'https://flagcdn.com/w80/sk.png',
    'Messico': 'https://flagcdn.com/w80/mx.png',
    'Croazia': 'https://flagcdn.com/w80/hr.png',
    'Montenegro': 'https://flagcdn.com/w80/me.png',
    'Portogallo': 'https://flagcdn.com/w80/pt.png',
    'Svizzera/Francia': 'https://flagcdn.com/w80/ch.png',
    'Austria': 'https://flagcdn.com/w80/at.png',
    'Israele': 'https://flagcdn.com/w80/il.png',
    'Grecia': 'https://flagcdn.com/w80/gr.png',
    'Germania': 'https://flagcdn.com/w80/de.png',
    'Singapore': 'https://flagcdn.com/w80/sg.png',
    'Malaysia': 'https://flagcdn.com/w80/my.png',
    'Altro': 'https://flagcdn.com/w80/un.png',
}

_MPD6 = [
    {'nation': 'Singapore', 'title': 'Channel 5', 'mpd': 'https://tglmp02.akamaized.net/out/v1/5081e069e08140c9b95f89a1659cf4dd/manifest.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=607b7d22565c4bc3b95ff6c33ce65425&key=28cc5367df666c44be4382e64af64d57'},
    {'nation': 'Singapore', 'title': 'Channel 8', 'mpd': 'https://tglmp02.akamaized.net/out/v1/4f6561ad194b49ae93f4e1b075afdf41/manifest.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=2448fc561b0c4220a81f1008971d3088&key=f48eb6753f3d1774da682970c93cf260'},
    {'nation': 'Singapore', 'title': 'Channel U', 'mpd': 'https://tglmp03.akamaized.net/out/v1/1057d89ee3d94148b430b5866e3a540a/manifest.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=0328a153c2994b279ab03ab25102fc59&key=2cc69eaaa858fed24c5623654daf8d3d'},
    {'nation': 'Singapore', 'title': 'Suria', 'mpd': 'https://tglmp04.akamaized.net/out/v1/b200e885125f4787bd2329952ff28fa1/manifest.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=7a9ea6df52044841b0c562766e602610&key=b9380188b4896b25e8d419dfce938c6e'},
    {'nation': 'Singapore', 'title': 'Vasantham', 'mpd': 'https://tglmp03.akamaized.net/out/v1/14eb6e921cae41298efaa4d9db0f2875/manifest.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=9970038ef6c548e39768f3a1ff6f5081&key=3e19d54b7bcd8bb336776fe136d48f57'},
    {'nation': 'Malaysia', 'title': 'CNA', 'mpd': 'https://linearjitp-playback.astro.com.my/dash-wv/linear/605/default_ott.mpd', 'keys': 'https://clearkey-base64-2-hex-json.herokuapp.com/results.php?keyid=f812aeae6be5b924a8181b512d5d7910&key=44275884ee394d05081fde395ff6e415'},
]

_AK47_MPD = [
    {'nation': 'Australia', 'title': 'Bein Sports 1 [Australia]', 'mpd': 'https://aba5sdmaaaaaaaamooyrewxky2c4j.otte.live.cf.ww.aiv-cdn.net/syd-nitro/live/clients/dash/enc/ghwcl6hv68/out/v1/83536910d8034e9b9895a20fbe1c1687/cenc.mpd', 'keys': '335dad778109954503dcbb21dc92015f:24bfd75d436cbf73168a2a2dccd40281'},
    {'nation': 'Australia', 'title': 'Bein Sports 2 [Australia]', 'mpd': 'https://aba5sdmaaaaaaaamdwujas5g6mg4r.otte.live.cf.ww.aiv-cdn.net/syd-nitro/live/clients/dash/enc/8m8cd46i1t/out/v1/83985c68e4174e90a58a1f2c024be4c9/cenc.mpd', 'keys': '0b42be2664d7e811d04f3e504e0924c5:ae24090123b8c72ac5404dc152847cb8'},
    {'nation': 'Australia', 'title': 'Bein Sports 3 [Australia]', 'mpd': 'https://aba5sdmaaaaaaaamhq2w5oosrf5ae.otte.live.cf.ww.aiv-cdn.net/syd-nitro/live/clients/dash/enc/q4u5nwaogz/out/v1/18de6d3e65934f3a8de4358e69eab86c/cenc.mpd', 'keys': '7995c724a13748ed970840a8ab5bb9b3:67bdaf1e2175b9ff682fcdf0e2354b1e'},
    {'nation': 'Austria', 'title': 'Sky Sport Austria HD', 'mpd': 'https://at-live-6.tentcdn.eu/bpk-tv/Sky_Sport_Austria_HD/default/index.mpd', 'keys': ''},
    {'nation': 'Israele', 'title': 'ESPNHDH265', 'mpd': 'https://nog-live1-ott.izzigo.tv/6/out/u/dash/ESPNHDH265/default.mpd', 'keys': ''},
    {'nation': 'Israele', 'title': 'ESPN2HDH265', 'mpd': 'https://nog-live1-ott.izzigo.tv/7/out/u/dash/ESPN2HDH265/default.mpd', 'keys': ''},
    {'nation': 'Israele', 'title': 'ESPN3HDH265', 'mpd': 'https://nog-live1-ott.izzigo.tv/6/out/u/dash/ESPN3HDH265/default.mpd', 'keys': ''},
    {'nation': 'Israele', 'title': 'ESPN4HDH265', 'mpd': 'https://nog-live1-ott.izzigo.tv/6/out/u/dash/ESPN4HDH265/default.mpd', 'keys': ''},
    {'nation': 'Brasile', 'title': 'Brasile abc3orwaaaaa', 'mpd': 'https://abc3orwaaaaaaaamhpui7wlnmfqgh.ottb.live.cf.ww.aiv-cdn.net/gru-nitro/live/clients/dash/enc/nelfyucw9a/out/v1/6ffb2c365ad14f88b154591beb43d1f6/cenc.mpd', 'keys': '56b79c1782b30e6b6fc973b0e8fd4104:fa38aaa865a57eda7c77444697ba8ed3'},
    {'nation': 'Brasile', 'title': 'Brasile abc3orwaaaaa', 'mpd': 'https://abc3orwaaaaaaaamliumq7klym4kj.ottb.live.cf.ww.aiv-cdn.net/gru-nitro/live/clients/dash/enc/oy6rp0jwmf/out/v1/580ecf12bad24979baf8dd993dce053e/cenc.mpd', 'keys': '9dc40460c93087aea84d6315f08ecb64:f69c8d4624fddff4ca89bd0b31bdc4a7'},
    {'nation': 'USA', 'title': 'TSN Logo [USA]', 'mpd': 'https://abkf7g7aaaaaaaamcmmhhhyli5fwh.otte.live.cf.ww.aiv-cdn.net/pdx-nitro/live/clients/dash/enc/u142pfptsm/out/v1/1caa3b2dfa9e448d8f61209bdfc1acdc/cenc.mpd', 'keys': '7e99f734748d098cbfa2f7bde968dd44:98ea6088c3222e9abaf61e537804d6cc'},
    {'nation': 'USA', 'title': 'USA abfjk4haaaaa', 'mpd': 'https://abfjk4haaaaaaaampv6ofhkihi4r6.bia-cf.live.pv-cdn.net/iad-nitro/live/clients/dash/enc/cllekigzzn/out/v1/bd3b0c314fff4bb1ab4693358f3cd2d3/cenc.mpd', 'keys': ''},
    {'nation': 'USA', 'title': 'KTVB NBC 7 Boise Idaho Logo [USA]', 'mpd': 'https://otte.live.fly.ww.aiv-cdn.net/iad-nitro/live/clients/dash/enc/3b7qwiqzk3/out/v1/9f14895badca43e6a716db021dcd0c31/cenc.mpd', 'keys': 'dc69b6159a0f9f0a4e03b3ff91cbacd5:d0dcbcd7723bc40df0bf34c9c092d51f'},
    {'nation': 'USA', 'title': 'USA otte.live.fl', 'mpd': 'https://otte.live.fly.ww.aiv-cdn.net/pdx-nitro/live/clients/dash/enc/uiffe4jhf0/out/v1/3534efafca8c4815adbb4d2e9a1fe003/cenc.mpd', 'keys': '3dcfbec0e7146928baa55210bf2cb62f:bc85f74f815d9be5ae1dd6defaa05135'},
    {'nation': 'USA', 'title': 'USA netskrt.live', 'mpd': 'https://netskrt.live.pv-cdn.net/OTTB/iad-nitro/live/clients/dash/enc/rbem8rorcw/out/v1/5318821e2c3c44c2a439681b9aa86e9b/cenc.mpd', 'keys': 'd9623774ac5c8c351aafe97c5fe70267:5164e6d05164a2d65fa8fcc962aa4861'},
    {'nation': 'USA', 'title': 'USA abfjk4haaaaa', 'mpd': 'https://abfjk4haaaaaaaampv6ofhkihi4r6.bia-cf.live.pv-cdn.net/iad-nitro/live/clients/dash/enc/fb6jy4pxts/out/v1/f8fa17f087564f51aa4d5c700be43ec4/cenc.mpd', 'keys': ''},
    {'nation': 'Slovacchia', 'title': 'SK Antik nvidia_sport_1', 'mpd': 'https://dash2.antik.sk/stream/nvidia_sport_1/playlist_cenc.mpd', 'keys': ''},
    {'nation': 'Slovacchia', 'title': 'SK Antik nvidia_sport2', 'mpd': 'https://dash2.antik.sk/stream/nvidia_sport2/playlist_cenc.mpd?ck=', 'keys': ''},
    {'nation': 'Slovacchia', 'title': '031133-50', 'mpd': 'https://linear207-de-dash1-prd-ak.cdn12.skycdp.com/031133-50/index.mpd', 'keys': ''},
    {'nation': 'Messico', 'title': 'ESPN HD MX', 'mpd': 'https://covoslivechannels2dash.clarovideo.com/Content/DASH_DASH_FK/Live/Channel(ESPN_HD)/manifest.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena1_n', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena1_n/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena2', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena2/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena3', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena3/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena4', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena4/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena5', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena5/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena6', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena6/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena7', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena7/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'arena8', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/arena8/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk1', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk1/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk2', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk2/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk3', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk3/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk4', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk4/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk5', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk5/default/index.mpd', 'keys': ''},
    {'nation': 'Croazia', 'title': 'sk6', 'mpd': 'https://bpcdnmanprod.nexttv.ht.hr/bpk-tv/sk6/default/index.mpd', 'keys': ''},
    {'nation': 'Svizzera/Francia', 'title': 'browser-dash', 'mpd': 'https://viamotionhsi.netplus.ch/live/eds/tf1hd/browser-dash/tf1hd.mpd', 'keys': ''},
    {'nation': 'Svizzera/Francia', 'title': 'browser-dash', 'mpd': 'https://viamotionhsi.netplus.ch/live/eds/france2hd/browser-dash/france2hd.mpd', 'keys': ''},
    {'nation': 'Svizzera/Francia', 'title': 'browser-dash', 'mpd': 'https://viamotionhsi.netplus.ch/live/eds/6ter/browser-dash/6ter.mpd', 'keys': ''},
    {'nation': 'Svizzera/Francia', 'title': '0c5c7fb388c649f78a1be36fc4bd365e', 'mpd': 'https://origin-18cd60dea8190528-rtlhu.live.6cloud.fr/out/v1/0c5c7fb388c649f78a1be36fc4bd365e/dash_long_cenc10_ucl1_hd_index.mpd', 'keys': ''},
    {'nation': 'Germania', 'title': '3221228661', 'mpd': 'https://svc40.main.sl.t-online.de/LCID3221228661.originalserver.prod.sngtv.t-online.de/PLTV/88888888/224/3221228661/3221228661.mpd', 'keys': ''},
    {'nation': 'Grecia', 'title': 'Dash', 'mpd': 'https://ocdn.antennaplus.gr/live/media0/Sports1/Dash/Sports1.mpd', 'keys': ''},
    {'nation': 'Paesi Bassi', 'title': 'NL 86', 'mpd': 'https://mag03.tvx.prd.tv.odido.nl/wh7f454c46tw75168188_-627298088/PLTV/86/224/3221241590/3221241590.mpd?zoneoffset=0&devkbps=1-7000&servicetype=1&icpid=86&accounttype=1&limitflux=-1&limitdur=-1&tenantId=3103&accountinfo=%7E%7EV2.0%7EqbcsJh_jU5C9BcZc959e_wae44b4867b3417aa76b5db2da20fe46c%7EKZzTWjB8qD1zdgbJjRPVLJX-tV0qiN9RBHC_iseGrsmTSRjj06oGDtGlpSCRGOwF3626cf085c08d024c7e4aafc18c32440%7EExtInfo5Ro3VppWiUusj2ippqUPkQ%3D%3D4a2d2c8ce133f43026d0e31b822b8474%3A20240601012829%3AUTC%2C10001003329222%2C87.212.140.171%2C20240601012829%2C3103_SP1S%2C10001003329222%2C-1%2C0%2C1%2C%2C%2C2%2C3103_Sport1%2C%2C%2C2%2C10000044444303%2C0%2C10000025050255%2CNDEzODg2NTY3MzEwMzI2NzMwNjMwNTY%3D%2C%2C%2C5%2C1%2CEND&GuardEncType=2&RTS=1717205309&from=11&hms_devid=1008&online=1717205309&mag_hms=1008,311,305&_=1717205322621', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 151', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$151/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 152', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$152/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 153', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$153/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 10', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$10/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 112', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$112/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 566', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$566/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Portogallo', 'title': 'PT LIVE 597', 'mpd': 'https://rr.cdn.vodafone.pt/LIVE/sdash/LIVE$597/index.mpd/Manifest.mpd?start=LIVE&end=END&device=DASH_AVC_FULLHD', 'keys': ''},
    {'nation': 'Montenegro', 'title': 'default', 'mpd': 'https://bpkcdn.telekom.me/bpk-tv/arena_premium_1/default/index.mpd', 'keys': ''},
    {'nation': 'Montenegro', 'title': 'default', 'mpd': 'https://bpkcdn.telekom.me/bpk-tv/arenasport_1/default/index.mpd', 'keys': ''},
    {'nation': 'Irlanda', 'title': 'NBC Logo [Irlanda]', 'mpd': 'https://ottb.live.cf.ww.aiv-cdn.net/dub-nitro/live/clients/dash/enc/2jbycgm3g3/out/v1/066dd9325648468c9ecdc8b272370931/cenc.mpd', 'keys': '84077d18bcf234a42de3745be106a87f:aee3069c062ec8ee6bfdd32985f287ef'},
]

_IPTV_LISTS = [
    {'type': 'm3u', 'name': 'Canali ITALIANI FREE (Rai, Mediaset, FAST)', 'url': 'https://iptv-org.github.io/iptv/countries/it.m3u'},
    {'type': 'm3u', 'name': 'Free-TV Italia + Internazionali', 'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8'},
    {'type': 'm3u', 'name': 'SPORT FREE (internazionale)', 'url': 'https://iptv-org.github.io/iptv/categories/sports.m3u'},
    {'type': 'm3u', 'name': 'FILM & SERIE TV FREE (internazionale)', 'url': 'https://iptv-org.github.io/iptv/categories/movies.m3u'},
    {'type': 'xtream', 'name': 'FXMAG1', 'host': 'http://fxmag1.com:8080', 'user': 'xsQPubvz', 'pass': 'nUwvSEkc'},
    {'type': 'xtream', 'name': 'FORYOU4K (IPTV Sport)', 'host': 'http://foryou4k.shop:80', 'user': '7V67W15L6V8QE5C', 'pass': 'mEgBBrYXiC'},
    {'type': 'xtream', 'name': 'FORYOU4K (Backup 2)', 'host': 'http://foryou4k.shop:80', 'user': '3063A2A9818F832', 'pass': 'kW2zcvXUUB'},
]
_IPTV7_CACHE = {}


def _m3u_parse(url):
    """Scarica e parsa una playlist M3U -> (gruppi ordinati, dict gruppo->[ (nome,url) ])."""
    key = 'm3u|' + url
    now = _iptv_now()
    c = _IPTV7_CACHE.get(key)
    if c and now - c[0] < 3600:
        return c[1], c[2]
    r = requests.get(url, headers={'User-Agent': UA}, timeout=30)
    r.encoding = 'utf-8'
    groups = {}
    cur_name, cur_group = '', ''
    for line in r.text.splitlines():
        line = line.strip()
        if line.startswith('#EXTINF'):
            nm = line.split(',', 1)[1].strip() if ',' in line else ''
            gm = re.search(r'group-title="([^"]*)"', line)
            cur_name = nm
            cur_group = gm.group(1).strip() if gm else 'Varie'
        elif line.startswith('http'):
            groups.setdefault(cur_group or 'Varie', []).append((cur_name or line, line))
    keys = sorted(groups.keys(), key=lambda x: x.lower())
    _IPTV7_CACHE[key] = (now, keys, groups)
    return keys, groups


def _xtrem_api(lst, action=''):
    url = '%s/player_api.php?username=%s&password=%s' % (lst['host'], lst['user'], lst['pass'])
    if action:
        url += '&action=' + action
    r = requests.get(url, timeout=15, headers={'User-Agent': UA})
    return json.loads(r.text)


def _xtrem_info(lst):
    key = lst['host'] + '|' + lst['user']
    now = _iptv_now()
    c = _IPTV7_CACHE.get(key + '|info')
    if c and now - c[0] < 300:
        return c[1]
    try:
        d = _xtrem_api(lst)
        info = (d.get('user_info') or {}) if isinstance(d, dict) else {}
        res = {'exp': '', 'act': '?', 'max': '?'}
        exp = info.get('exp_date')
        if exp:
            try:
                res['exp'] = _iptv_fmt_date(int(exp))
            except Exception:
                pass
        res['act'] = info.get('active_cons', '?')
        res['max'] = info.get('max_connections', '?')
        res['status'] = info.get('status', '')
    except Exception as e:
        log('sky7 info ERR: %s' % e)
        res = {'exp': '', 'act': '?', 'max': '?', 'status': 'offline'}
    _IPTV7_CACHE[key + '|info'] = (now, res)
    return res


def _iptv_now():
    import time
    return time.time()


def _iptv_fmt_date(ts):
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime('%d/%m/%Y')


def sky7_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    xbmcplugin.setContent(HANDLE, 'videos')
    for n, lst in enumerate(_IPTV_LISTS):
        if lst.get('type') == 'm3u':
            label = lst['name']
            plot = 'Lista M3U gratuita - canali riproducibili'
        else:
            i = _xtrem_info(lst)
            label = '%s | Scadenza: %s | Connessi: %s/%s' % (
                lst['name'], i.get('exp') or 'n/d', i.get('act', '?'), i.get('max', '?'))
            plot = 'Lista IPTV Xtream\nServer: %s\nStato: %s' % (lst['host'], i.get('status') or 'n/d')
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
        li.setInfo('video', {'title': label, 'plot': plot})
        url = BASE + '?action=sky7list&idx=' + urllib.parse.quote(str(n)) + '&back=' + urllib.parse.quote(BASE + '?action=sky7')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sky7_list_view(idx, back=''):
    back_button(back or (BASE + '?action=sky7'))
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        lst = _IPTV_LISTS[int(idx)]
    except Exception:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    if lst.get('type') == 'm3u':
        try:
            keys, groups = _m3u_parse(lst['url'])
        except Exception as e:
            log('sky7 m3u ERR: %s' % e)
            keys, groups = [], {}
        for g in keys:
            cnt = len(groups[g])
            li = xbmcgui.ListItem(label=lbl('%s (%d)' % (g, cnt)))
            li.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
            li.setInfo('video', {'title': g, 'plot': '%d canali IPTV' % cnt})
            url = BASE + '?action=sky7cat&idx=' + urllib.parse.quote(str(idx)) + '&cat=' + urllib.parse.quote(g) + '&back=' + urllib.parse.quote(BASE + '?action=sky7list&idx=' + urllib.parse.quote(str(idx)))
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    key = lst['host'] + '|' + lst['user']
    now = _iptv_now()
    c = _IPTV7_CACHE.get(key)
    if not c or now - c[0] > 600:
        try:
            cats = _xtrem_api(lst, 'get_live_categories') or []
            streams = _xtrem_api(lst, 'get_live_streams') or []
            _IPTV7_CACHE[key] = (now, cats, streams)
        except Exception as e:
            log('sky7 xtream ERR: %s' % e)
            cats, streams = [], []
    else:
        cats, streams = c[1], c[2]
    cat_names = {}
    for cc in cats:
        cat_names[str(cc.get('category_id'))] = cc.get('category_name', '?')
    groups = {}
    for s in streams:
        cid = str(s.get('category_id'))
        groups.setdefault(cid, []).append(s)
    for cid in sorted(groups, key=lambda x: cat_names.get(x, '?').lower()):
        name = cat_names.get(cid, 'Categoria %s' % cid)
        cnt = len(groups[cid])
        li = xbmcgui.ListItem(label=lbl('%s (%d)' % (name, cnt)))
        li.setArt({'thumb': LOGO_BASE + 'skyhd.png', 'icon': LOGO_BASE + 'skyhd.png'})
        li.setInfo('video', {'title': name, 'plot': '%d canali IPTV' % cnt})
        url = BASE + '?action=sky7cat&idx=' + urllib.parse.quote(str(idx)) + '&cat=' + urllib.parse.quote(cid) + '&back=' + urllib.parse.quote(BASE + '?action=sky7list&idx=' + urllib.parse.quote(str(idx)))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sky7_cat_view(idx, cat, back=''):
    back_button(back or (BASE + '?action=sky7list&idx=' + urllib.parse.quote(str(idx))))
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        lst = _IPTV_LISTS[int(idx)]
    except Exception:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    if lst.get('type') == 'm3u':
        try:
            _, groups = _m3u_parse(lst['url'])
        except Exception as e:
            log('sky7 m3u ERR: %s' % e)
            groups = {}
        for name, url in groups.get(cat, []):
            li = xbmcgui.ListItem(label=lbl(name), path=url)
            li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
            li.setProperty('isPlayable', 'true')
            li.setProperty('inputstream', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            hdrs = 'User-Agent=%s' % UA
            li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
            li.setProperty('inputstream.adaptive.stream_headers', hdrs)
            li.setInfo('video', {'title': name, 'mediatype': 'video'})
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    key = lst['host'] + '|' + lst['user']
    now = _iptv_now()
    c = _IPTV7_CACHE.get(key)
    if not c or now - c[0] > 600:
        try:
            cats = _xtrem_api(lst, 'get_live_categories') or []
            streams = _xtrem_api(lst, 'get_live_streams') or []
            _IPTV7_CACHE[key] = (now, cats, streams)
        except Exception as e:
            log('sky7 xtream ERR: %s' % e)
            streams = []
    else:
        streams = c[2]
    for s in [x for x in streams if str(x.get('category_id')) == str(cat)]:
        name = s.get('name', s.get('stream_id'))
        sid = s.get('stream_id')
        url = '%s/%s/%s/%s.m3u8' % (lst['host'], lst['user'], lst['pass'], sid)
        li = xbmcgui.ListItem(label=lbl(name), path=url)
        li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', 'hls')
        hdrs = 'User-Agent=VLC/3.0.20 LibVLC/3.0.20'
        li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
        li.setProperty('inputstream.adaptive.stream_headers', hdrs)
        li.setInfo('video', {'title': name, 'mediatype': 'video'})
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sky6_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    xbmcplugin.setContent(HANDLE, 'videos')
    # raggruppa per nazione
    from collections import Counter
    nations = {}
    for ch in _MPD6:
        nations.setdefault(ch['nation'], []).append(ch)
    for nation in sorted(nations):
        cnt = len(nations[nation])
        flag = _FLAGS.get(nation, LOGO_BASE + 'skyhd.png')
        li = xbmcgui.ListItem(label=lbl('%s (%d)' % (nation, cnt)))
        li.setArt({'thumb': flag, 'icon': flag})
        li.setInfo('video', {'title': nation, 'plot': '%d canali MPD LIVE' % cnt})
        url = BASE + '?action=sky6nation&nation=' + urllib.parse.quote(nation) + '&back=' + urllib.parse.quote(BASE + '?action=sky6')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sky6_nation_view(nation, back=''):
    back_button(back or (BASE + '?action=sky6'))
    xbmcplugin.setContent(HANDLE, 'videos')
    for ch in [c for c in _MPD6 if c['nation'] == nation]:
        mpd = ch['mpd']
        keys = ch.get('keys') or ch.get('key') or ''
        # nome completo già in ch['title']
        li = xbmcgui.ListItem(label=lbl(ch['title']), path=mpd)
        li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
        # headers come Mandrakodi amstaffTest: Host + UA + Referer/Origin
        try:
            host = 'https://' + mpd.split('/')[2]
        except Exception:
            host = mpd
        ua = UA
        hdrs = 'User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (ua, host, host)
        li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
        li.setProperty('inputstream.adaptive.stream_headers', hdrs)
        if keys:
            # piu chiavi separate da virgola -> passa tutte (Mandrakodi fa drm_legacy con full)
            li.setProperty('inputstream.adaptive.license_type', 'org.w3.clearkey')
            li.setProperty('inputstream.adaptive.license_key', keys)
            # compat legacy
            li.setProperty('inputstream.adaptive.drm_legacy', 'org.w3.clearkey|' + keys)
        li.setInfo('video', {'title': ch['title'], 'plot': '', 'mediatype': 'video'})
        xbmcplugin.addDirectoryItem(HANDLE, mpd, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sky1_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    for cat in (CAT_INT, CAT_SPORT):
        label = lbl(cat)
        try:
            c = _sky_counts(cat)
            label += ' | CANALI ATTIVI: %d • CANALI IN SCADENZA: %d • CANALI SCADUTI: %d' % (c.get('ok', 0), c.get('soon', 0), c.get('exp', 0))
        except Exception as e:
            log('sky_counts %s: %s' % (cat, e))
        li = xbmcgui.ListItem(label=label)
        url = BASE + '?action=skycat&cat=' + urllib.parse.quote(cat) + '&back=' + urllib.parse.quote(BASE + '?action=sky1')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sky2_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    epg = epg_load() if ADDON.getSetting('epg_enabled') == 'true' else None
    try:
        catalog = _vavoo_catalog()
        # filtra Italy + sky, deduplica per nome base (rimuove .c/.s e backup)
        seen = {}
        for it in catalog:
            grp = it.get('group', '')
            if 'Italy' not in grp:
                continue
            name = (it.get('name') or '').strip()
            if 'sky' not in name.lower():
                continue
            play_url = it.get('url', '')
            if not play_url:
                continue
            # normalizza: toglie suffissi .c/.s, (BACKUP), spazi doppi, (7)
            base = re.sub(r'\s*\.(c|s)\s*$', '', name, flags=re.IGNORECASE).strip()
            base = re.sub(r'\s*\(BACKUP\)\s*', ' ', base, flags=re.IGNORECASE).strip()
            base = re.sub(r'\s*\(\d+\)\s*$', '', base).strip()
            base = re.sub(r'\s+', ' ', base)
            key = base.lower()
            # preferisci .c (cloud) al .s, e la prima occorrenza vince
            if key not in seen:
                seen[key] = (base, play_url, it.get('logo') or '')
            elif '.c' in name.lower() and '.s' in seen[key][0].lower():
                seen[key] = (base, play_url, it.get('logo') or seen[key][2])

        if not seen:
            raise Exception('catalogo Vavoo vuoto')

        sky_list = sorted(seen.values(), key=lambda x: x[0].lower())

        xbmcplugin.setContent(HANDLE, 'videos')
        for cname, ch_url, logo in sky_list:
            cur, nxt = _epg_now(cname, epg)
            cur_prog = str(cur[2]).strip() if (cur and len(cur) >= 3 and cur[2]) else ''
            lines = []
            if cur:
                lines.append('Ora %02d:%02d %s' % (cur[0].hour, cur[0].minute, _epg_short(cur[2], 60)))
            if nxt:
                lines.append('%02d:%02d %s' % (nxt[0].hour, nxt[0].minute, _epg_short(nxt[2], 60)))
            # logo mappato o da catalog
            lkey = cname.lower().replace('sky ', '').replace(' ', '')
            mapped = LOGOS.get(lkey, '')
            thumb = (LOGO_BASE + mapped) if mapped else (logo or SQUARE_ICON)
            li = xbmcgui.ListItem(label=lbl(cname))
            li.setArt({'thumb': thumb, 'icon': thumb, 'poster': thumb})
            li.setProperty('isPlayable', 'true')
            li.setInfo('video', {'title': cname, 'plot': ' | '.join(lines), 'mediatype': 'video'})
            url = BASE + '?action=vavooplay&url=' + urllib.parse.quote(ch_url) + '&t=' + urllib.parse.quote(cname) + '&p=' + urllib.parse.quote(cur_prog)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    except Exception as e:
        xbmc.log('KODIAKSO sky2_view ERR: ' + str(e), xbmc.LOGERROR)
        import traceback
        xbmc.log('KODIAKSO sky2_view TB: ' + traceback.format_exc(), xbmc.LOGERROR)
        notify('SKY 2', 'Errore caricamento canali (Vavoo auth)', True)

    xbmcplugin.endOfDirectory(HANDLE)


def sky3_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    try:
        cats = _daddy_fetch()
        xbmcplugin.setContent(HANDLE, 'videos')
        added = 0
        for cat in cats:
            for it in (cat.get('items') or []):
                raw_title = it.get('title') or ''
                title = strip_color(raw_title)
                # filtro esclusivo: deve contenere Sky Sport e IT
                if not re.search(r'Sky Sport', title, re.I):
                    continue
                if not re.search(r'\bIT\b', title):
                    continue
                # escludi DE/UK residui
                if ' DE' in title or ' UK' in title:
                    continue
                mr = it.get('myresolve') or ''
                code = mr.split('@@', 1)[1] if '@@' in mr else ''
                if not code:
                    continue
                # label pulita: data/ora + evento + canale
                label = lbl(title)
                # EPG per Sky channel estratto dal titolo (es. Sky Sport Calcio IT)
                mch = re.search(r'(Sky Sport[^\[\]]*?IT)', title, re.I)
                ch_name = mch.group(1).strip() if mch else 'Sky Sport IT'
                li = xbmcgui.ListItem(label=label)
                lkey = re.sub(r'[^a-z]', '', ch_name.lower().replace('sky', '').replace('sport', 'skysport'))
                # mappa skysport -> logo
                mapped = LOGOS.get(lkey, '') or LOGOS.get(ch_name.lower().replace('sky ', '').replace(' ', ''), '')
                thumb = (LOGO_BASE + mapped) if mapped else SQUARE_ICON
                li.setArt({'thumb': thumb, 'icon': thumb, 'poster': thumb})
                li.setProperty('isPlayable', 'true')
                li.setInfo('video', {'title': title, 'plot': it.get('info') or title, 'mediatype': 'video'})
                url = _tmdb_url('ddy_play', c=code)
                xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
                added += 1
        if not added:
            li = xbmcgui.ListItem(label=lbl('Nessun evento Sky Sport Italia al momento (DaddyLive)'))
            xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sky', li, isFolder=False)
    except Exception as e:
        xbmc.log('KODIAKSO sky3_view ERR: ' + str(e), xbmc.LOGERROR)
        import traceback
        xbmc.log('KODIAKSO sky3_view TB: ' + traceback.format_exc(), xbmc.LOGERROR)
        notify('SKY 3', 'Errore caricamento DaddyLive', True)
    xbmcplugin.endOfDirectory(HANDLE)


def _sportonline_fetch():
    cached = _VAVOO_CAT_CACHE.get('sportonline')
    # reuse short TTL 15min
    try:
        if cached and (time.time() - cached[1] < 900):
            return cached[0]
    except Exception:
        pass
    events = []
    try:
        # prog.txt SportOnline - HD7/HD8 ITALIAN
        urls = ['https://sportsonline.vc/prog.txt', 'https://sportsonline.gl/prog.txt']
        txt = ''
        for u in urls:
            try:
                r = requests.get(u, headers={'User-Agent': UA}, timeout=12)
                if r.status_code == 200 and r.text:
                    txt = r.text
                    break
            except Exception:
                continue
        if not txt:
            return []
        for line in txt.splitlines():
            line = line.strip()
            if not line or line.startswith('=') or line.startswith('|') or 'INFO:' in line or '24/7' in line or 'LAST UPDATE' in line or line.startswith('(') or 'HD' not in line and 'http' not in line:
                if '|' not in line:
                    continue
            if '|' not in line:
                continue
            # entry format: 17:30   Udinese x Como | https://w2.sportsonlinee.click/channels/hd/hd8.php
            left, right = line.split('|', 1)
            left = left.strip()
            url = right.strip()
            # filtra solo HD7/HD8 ITALIAN
            if 'hd7.php' not in url.lower() and 'hd8.php' not in url.lower():
                continue
            # left contains time + event
            m = re.match(r'(\d{1,2}:\d{2})\s+(.*)', left)
            if m:
                t = m.group(1)
                ev = m.group(2).strip()
                # pulizia
                ev = re.sub(r'\s+', ' ', ev)
                title = '%s  %s [HD7/HD8 IT]' % (t, ev) if 'hd7' in url.lower() and 'hd8' in url.lower() else ('%s  %s [%s]' % (t, ev, 'HD7 IT' if 'hd7' in url.lower() else 'HD8 IT'))
                # prefer title with channel tag
                events.append({'title': title, 'url': url, 'time': t, 'event': ev})
            else:
                events.append({'title': left[:80], 'url': url})
        _VAVOO_CAT_CACHE['sportonline'] = (events, time.time())
    except Exception as e:
        log('sportonline fetch ERR: ' + str(e))
    return events


def _sportonline_unpack(packed):
    try:
        # P.A.C.K.E.R. unpack minimal
        import re as _re
        m = _re.search(r"}\('(.*)',\s*(\d+),\s*(\d+),\s*'(.*)'\.split\('\|'\)", packed, _re.S)
        if not m:
            return None
        p, a, c, k = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).split('|')
        # base36 decode
        def base36(n):
            chars = '0123456789abcdefghijklmnopqrstuvwxyz'
            s = ''
            if n == 0:
                return '0'
            while n:
                n, r = divmod(n, 36)
                s = chars[r] + s
            return s
        # build dict
        d = {}
        for i in range(c):
            d[base36(i)] = k[i] if i < len(k) else base36(i)
        # replace
        def repl(mo):
            w = mo.group(0)
            return d.get(w, w)
        unpacked = _re.sub(r'\b\w+\b', repl, p)
        return unpacked
    except Exception:
        return None


def resolve_sportonline(url):
    try:
        sess = requests.Session()
        sess.headers.update({'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'})
        # handle w2 vs sportzonline domain fallback
        urls_try = [url]
        if 'w2.sportsonlinee.click' in url:
            urls_try.append(url.replace('w2.sportsonlinee.click', 'sportsonline.click'))
            urls_try.append(url.replace('w2.sportsonlinee.click', 'w2.sportsonline.click'))
        html_txt = ''
        last_err = None
        for u in urls_try:
            try:
                r = sess.get(u, headers={'Referer': 'https://sportsonline.vc/'}, timeout=15, verify=False)
                if r.status_code == 200 and '<iframe' in r.text:
                    html_txt = r.text
                    url = u
                    break
                last_err = 'http %s' % r.status_code
            except Exception as e:
                last_err = str(e)
        if not html_txt or '<iframe' not in html_txt:
            raise ValueError('iframe non trovato (%s)' % last_err)
        m = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', html_txt, re.I)
        if not m:
            raise ValueError('iframe src non trovato')
        iframe = m.group(1)
        if iframe.startswith('//'):
            iframe = 'https:' + iframe
        elif iframe.startswith('/'):
            iframe = 'https://w2.sportsonlinee.click' + iframe
        # second level with full browser headers
        h2 = {'User-Agent': UA, 'Referer': url, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'it-IT,it;q=0.9', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'navigate'}
        r2 = sess.get(iframe, headers=h2, timeout=15, verify=False)
        txt2 = r2.text if r2.status_code == 200 else ''
        if r2.status_code == 403:
            # Cloudflare block - try with barecrop direct via textise and retry with extra headers
            h2b = dict(h2)
            h2b['Accept'] = '*/*'
            h2b['Referer'] = 'https://w2.sportsonlinee.click/'
            try:
                r2b = sess.get(iframe, headers=h2b, timeout=15, verify=False)
                if r2b.status_code == 200:
                    txt2 = r2b.text
            except Exception:
                pass
        # cerca m3u8 diretto
        m3 = re.search(r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)', txt2)
        if m3:
            link = m3.group(1).replace('\\/', '/').replace('&amp;', '&')
            li = xbmcgui.ListItem(path=link, offscreen=True)
            li.setContentLookup(False)
            li.setProperty('inputstream', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            hdrs = 'Referer=%s&User-Agent=%s&Origin=%s' % (iframe, UA, 'https://' + iframe.split('/')[2])
            li.setProperty('inputstream.adaptive.stream_headers', hdrs)
            li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
            return li
        # packer unpack
        m4 = re.search(r'eval\(function\(p,a,c,k,e,d\).*?\)\)', txt2, re.S)
        if m4:
            unpacked = _sportonline_unpack(m4.group(0))
            if unpacked:
                m5 = re.search(r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)', unpacked)
                if m5:
                    link = m5.group(1).replace('\\/', '/')
                    li = xbmcgui.ListItem(path=link, offscreen=True)
                    li.setContentLookup(False)
                    li.setProperty('inputstream', 'inputstream.adaptive')
                    li.setProperty('inputstream.adaptive.manifest_type', 'hls')
                    hdrs = 'Referer=%s&User-Agent=%s' % (iframe, UA)
                    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
                    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
                    return li
                # se unpack ha file: "...file":"https://..."
                m6 = re.search(r'"file"\s*:\s*"([^"]+m3u8[^"]*)"', unpacked)
                if m6:
                    link = m6.group(1).replace('\\/', '/')
                    li = xbmcgui.ListItem(path=link, offscreen=True)
                    li.setProperty('inputstream', 'inputstream.adaptive')
                    li.setProperty('inputstream.adaptive.manifest_type', 'hls')
                    return li
            # fallback: ritorna iframe con header (Kodi potrebbe seguire redirect 302)
            li = xbmcgui.ListItem(path=iframe, offscreen=True)
            li.setContentLookup(False)
            li.setProperty('inputstream', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            hdrs = 'Referer=%s&User-Agent=%s' % (url, UA)
            li.setProperty('inputstream.adaptive.stream_headers', hdrs)
            li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
            log('sportonline packer fallback iframe %s' % iframe)
            return li
        # fallback generico: prova iframe diretto come HLS (Kodi segue redirect)
        if iframe:
            li = xbmcgui.ListItem(path=iframe, offscreen=True)
            li.setContentLookup(False)
            li.setProperty('inputstream', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            hdrs = 'Referer=%s&User-Agent=%s' % (url, UA)
            li.setProperty('inputstream.adaptive.stream_headers', hdrs)
            li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
            log('sportonline fallback iframe %s' % iframe)
            return li
        raise ValueError('stream non estratto (len=%s iframe=%s)' % (len(txt2), iframe[:60]))
    except Exception as e:
        log('sportonline resolve %s: %s' % (url, e))
        import traceback
        log('sportonline TB: ' + traceback.format_exc())
        notify('SKY 4', 'Errore risoluzione SportOnline', True)
        return xbmcgui.ListItem()


def sky4_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    try:
        evs = _sportonline_fetch()
        xbmcplugin.setContent(HANDLE, 'videos')
        if not evs:
            li = xbmcgui.ListItem(label=lbl('Nessun evento HD7/HD8 IT al momento (SportOnline)'))
            xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sky', li, isFolder=False)
            xbmcplugin.endOfDirectory(HANDLE)
            return
        for ev in evs:
            title = ev.get('title') or 'Evento'
            url = ev.get('url') or ''
            li = xbmcgui.ListItem(label=lbl(title))
            li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
            li.setProperty('isPlayable', 'true')
            li.setInfo('video', {'title': title, 'plot': title})
            play_url = BASE + '?action=sportplay&url=' + urllib.parse.quote(url) + '&t=' + urllib.parse.quote(title)
            xbmcplugin.addDirectoryItem(HANDLE, play_url, li, isFolder=False)
    except Exception as e:
        xbmc.log('KODIAKSO sky4_view ERR: ' + str(e), xbmc.LOGERROR)
        notify('SKY 4', 'Errore caricamento SportOnline', True)
    xbmcplugin.endOfDirectory(HANDLE)


_CALCIO_CACHE = {'data': None, 'ts': 0}
_CALCIO_TTL = 1800


def _calcio_fetch():
    now = time.time()
    if _CALCIO_CACHE['data'] is not None and (now - _CALCIO_CACHE['ts'] < _CALCIO_TTL):
        return _CALCIO_CACHE['data']
    events = []
    try:
        rss_urls = ['https://fifa.direttecommunity.online/rss.xml', 'https://live.direttecommunity.online/rss.xml']
        xml_txt = ''
        for u in rss_urls:
            try:
                r = requests.get(u, headers={'User-Agent': UA}, timeout=12)
                if r.status_code == 200 and '<item>' in r.text:
                    xml_txt = r.text
                    break
            except Exception:
                continue
        if not xml_txt:
            return []
        root = ET.fromstring(xml_txt.encode('utf-8'))
        for item in root.findall('.//item'):
            title = (item.findtext('title') or '').strip()
            link = (item.findtext('link') or '').strip()
            cat = (item.findtext('category') or '').strip()
            pub = (item.findtext('pubDate') or '').strip()
            if not title or not link:
                continue
            # filtro data: mostra solo eventi di oggi/domani, scarta ieri
            try:
                import email.utils as eut
                dt = eut.parsedate_to_datetime(pub) if pub else None
                if dt is not None:
                    # normalizza a UTC poi confronta con oggi UTC
                    now_dt = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
                    # scarta se più vecchio di 6 ore rispetto a now (ieri)
                    if (now_dt - dt).total_seconds() > 6*3600 and dt.date() < now_dt.date():
                        continue
            except Exception:
                pass
            events.append({'title': html.unescape(title), 'link': link, 'category': cat, 'pubDate': pub})
        # ordina per data crescente (prossimi prima)
        try:
            import email.utils as eut2
            def _k(ev):
                try:
                    d = eut2.parsedate_to_datetime(ev.get('pubDate') or '')
                    return d.timestamp() if d else 0
                except Exception:
                    return 0
            events.sort(key=_k)
        except Exception:
            pass
        _CALCIO_CACHE['data'] = events
        _CALCIO_CACHE['ts'] = now
    except Exception as e:
        log('calcio fetch ERR: ' + str(e))
    return events


def _calcio_links(event_url):
    try:
        r = requests.get(event_url, headers={'User-Agent': UA, 'Referer': 'https://live.direttecommunity.online/', 'Accept': 'text/html,*/*'}, timeout=15)
        r.raise_for_status()
        html_txt = r.text
        links = re.findall(r'data-link="([^"]+)"', html_txt)
        # fallback: cerca w2.sportsonlinee.click links diretti
        if not links:
            links = re.findall(r'(https?://w2\.sportsonlinee\.click[^\s"\'<>]+)', html_txt)
        uniq = []
        seen = set()
        for u in links:
            if u not in seen:
                seen.add(u)
                uniq.append(u)
        return uniq
    except Exception as e:
        log('calcio links %s: %s' % (event_url, e))
        return []


def sky5_view(back=''):
    back_button(back or (BASE + '?action=sky'))
    try:
        evs = _calcio_fetch()
        xbmcplugin.setContent(HANDLE, 'videos')
        if not evs:
            li = xbmcgui.ListItem(label=lbl('Nessun evento CalcioStreaming al momento'))
            xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sky', li, isFolder=False)
            xbmcplugin.endOfDirectory(HANDLE)
            return
        for ev in evs[:50]:
            title = ev.get('title') or 'Evento'
            cat = ev.get('category') or ''
            pub = ev.get('pubDate') or ''
            label = title
            if cat:
                label += '  [COLOR FF99CC33]%s[/COLOR]' % cat
            li = xbmcgui.ListItem(label=lbl(label))
            li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
            li.setProperty('isPlayable', 'false')
            li.setInfo('video', {'title': title, 'plot': '%s | %s | %s' % (title, cat, pub)})
            url = BASE + '?action=calcioevent&url=' + urllib.parse.quote(ev.get('link') or '') + '&t=' + urllib.parse.quote(title)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    except Exception as e:
        xbmc.log('KODIAKSO sky5_view ERR: ' + str(e), xbmc.LOGERROR)
        notify('SKY 5', 'Errore caricamento CalcioStreaming', True)
    xbmcplugin.endOfDirectory(HANDLE)


def calcio_event_view(url, title=''):
    back_button(BASE + '?action=sky5')
    try:
        links = _calcio_links(url)
        xbmcplugin.setContent(HANDLE, 'videos')
        if not links:
            li = xbmcgui.ListItem(label=lbl('Nessun flusso disponibile per %s' % (title or 'evento')))
            xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sky5', li, isFolder=False)
            xbmcplugin.endOfDirectory(HANDLE)
            return
        for idx, link in enumerate(links):
            # etichetta canale: estrae hd7/hd8 etc o nome
            ch = 'Canale %d' % (idx + 1)
            m = re.search(r'/([^/]+)\.php', link)
            if m:
                ch = m.group(1).upper()
                if 'hd7' in ch.lower():
                    ch += ' [HD7 IT]'
                elif 'hd8' in ch.lower():
                    ch += ' [HD8 IT]'
            li = xbmcgui.ListItem(label=lbl('%s - %s' % (title or 'Evento', ch)))
            li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
            li.setProperty('isPlayable', 'true')
            li.setInfo('video', {'title': ch})
            play_url = BASE + '?action=sportplay&url=' + urllib.parse.quote(link) + '&t=' + urllib.parse.quote(title or ch)
            xbmcplugin.addDirectoryItem(HANDLE, play_url, li, isFolder=False)
    except Exception as e:
        xbmc.log('KODIAKSO calcio_event ERR: ' + str(e), xbmc.LOGERROR)
        notify('Calcio', 'Errore', True)
    xbmcplugin.endOfDirectory(HANDLE)


def _epg_cache_path():
    return os.path.join(_profile_path(), 'epg_cache.pkl')


def _epg_candidates(cid):
    cands = {cid.lower()}
    disp = SKY_DEFS.get(cid, ('', ''))[0]
    if disp:
        cands.add(' '.join(disp.lower().split()))
    if cid == 'tg24':
        cands.add('sky tg24')
    if cid == 'mtv':
        cands.add('mtv hd')
        cands.add('mtv music')
    if cid.startswith('skysport'):
        m = re.match(r'^skysport(.+)$', cid)
        rest = m.group(1) if m else ''
        base = 'sky sport ' + rest
        cands.add(base)
        cands.add(base + ' hd')
        cands.add(base + ' fhd')
        cands.add(base + ' ultra hd')
    return cands


def _epg_dt(val):
    if not val:
        return None
    m = re.match(r'(\d{14})', val)
    if not m:
        return None
    try:
        s = m.group(1)
        return datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]),
                        int(s[8:10]), int(s[10:12]), int(s[12:14])) + timedelta(hours=2)
    except ValueError:
        return None


def _epg_parse(raw):
    root = ET.fromstring(raw)
    want = set()
    for cid in list(SKY_DEFS) + ['skysport%d' % n for n in range(251, 260)]:
        want |= _epg_candidates(cid)
    chmap = {}
    for ch in root.findall('channel'):
        chid = (ch.get('id') or '').lower()
        if not chid:
            continue
        chmap.setdefault(chid, chid)
        for dn in ch.findall('display-name'):
            nm = ' '.join((dn.text or '').split()).lower()
            if nm:
                chmap.setdefault(nm, chid)
    keep = set()
    for k, v in chmap.items():
        if k in want or v in want:
            keep.add(v)
    progs = {}
    now = datetime.now() - timedelta(hours=3)
    end = datetime.now() + timedelta(hours=30)
    for p in root.findall('programme'):
        chid = (p.get('channel') or '').lower()
        if chid not in keep:
            continue
        s = _epg_dt(p.get('start'))
        e = _epg_dt(p.get('stop'))
        if not s or not e:
            continue
        if e < now or s > end:
            continue
        t = p.find('title')
        title = ' '.join((t.text or '').split()) if t is not None else ''
        progs.setdefault(chid, []).append((s, e, title))
    for chid in progs:
        progs[chid].sort(key=lambda x: x[0])
    return {'chmap': chmap, 'progs': progs}


def _http_get_bytes(url):
    last = None
    try:
        r = requests.get(url, timeout=30, headers={'User-Agent': API_UA})
        r.raise_for_status()
        return r.content
    except Exception as e:
        last = e
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': API_UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except Exception as e:
        last = last if last is not None else e
    try:
        import xbmcvfs
        f = xbmcvfs.File(url, 'rb')
        try:
            data = f.read()
        finally:
            f.close()
        if data:
            return data
        raise IOError('xbmcvfs empty')
    except Exception as e:
        raise last if last is not None else e


def epg_load():
    if _EPG_SESSION['data'] is not None:
        return _EPG_SESSION['data']
    path = _epg_cache_path()
    if os.path.exists(path):
        try:
            if time.time() - os.path.getmtime(path) < EPG_KEEP_HOURS * 3600:
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                _EPG_SESSION['data'] = data
                return data
        except Exception:
            pass
    if _EPG_SESSION.get('fail') and time.time() - _EPG_SESSION['fail'] < EPG_KEEP_HOURS * 3600:
        return None
    try:
        url = ADDON.getSetting('epg_url').strip() or EPG_URL_DEFAULT
        raw = _http_get_bytes(url)
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
        data = _epg_parse(raw)
        try:
            d = os.path.dirname(path)
            if not os.path.isdir(d):
                os.makedirs(d)
            with open(path, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
        _EPG_SESSION['data'] = data
        return data
    except Exception as e:
        xbmc.log('KODIAKSO epg ERR: ' + str(e), xbmc.LOGERROR)
        try:
            import traceback
            xbmc.log('KODIAKSO epg TB:\n' + traceback.format_exc(), xbmc.LOGERROR)
        except Exception:
            pass
        _EPG_SESSION['fail'] = time.time()
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                _EPG_SESSION['data'] = data
                return data
            except Exception:
                pass
        return None


def _epg_chid(cid, epg):
    if not epg:
        return None
    for c in _epg_candidates(cid):
        if c in epg['chmap']:
            return epg['chmap'][c]
    return None


def _epg_short(t, n=38):
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n - 1] + '\u2026'


def _epg_now(cid, epg=None):
    try:
        if ADDON.getSetting('epg_enabled') != 'true':
            return None, None
        if epg is None:
            epg = epg_load()
        chid = _epg_chid(cid, epg)
        if not chid:
            return None, None
        progs = epg['progs'].get(chid, [])
        if not progs:
            return None, None
        now = datetime.now()
        cur = None
        nxt = None
        for i, p in enumerate(progs):
            if p[0] <= now < p[1]:
                cur = p
                if i + 1 < len(progs):
                    nxt = progs[i + 1]
                break
        if cur is None:
            for p in progs:
                if p[0] > now:
                    nxt = p
                    break
        return cur, nxt
    except Exception as e:
        log('epg_now %s: %s' % (cid, e))
        try:
            import traceback
            log('epg_now TB: ' + traceback.format_exc())
        except Exception:
            pass
        return None, None


def sky_cat_view(cat, back=''):
    back_button(back or (BASE + '?action=sky'))
    epg = epg_load() if ADDON.getSetting('epg_enabled') == 'true' else None
    try:
        for title, cid in sky_channels().get(cat, []):
            try:
                exp = _sky_expiry(cid)
                cur, nxt = _epg_now(cid, epg)
                prog = ''
                if cur:
                    prog = _sky_epg_label(cur)
                label, l2, tname = _sky_parts(title, exp, prog)
                li = xbmcgui.ListItem(label=label)
                if l2:
                    li.setLabel2(l2)
                logo = LOGOS.get(cid, '')
                li.setArt({'thumb': (LOGO_BASE + logo) if logo else SQUARE_ICON,
                           'icon': (LOGO_BASE + logo) if logo else SQUARE_ICON,
                           'poster': (LOGO_BASE + logo) if logo else SQUARE_ICON})
                li.setProperty('isPlayable', 'true')
                lines = []
                if exp:
                    lines.append('Scadenza %s' % exp.strftime('%d/%m/%Y %H:%M'))
                if cur:
                    lines.append('Ora %02d:%02d %s' % (cur[0].hour, cur[0].minute, _epg_short(cur[2], 60)))
                if nxt:
                    lines.append('%02d:%02d %s' % (nxt[0].hour, nxt[0].minute, _epg_short(nxt[2], 60)))
                li.setInfo('video', {'title': tname, 'plot': ' | '.join(lines)})
                cur_p = (cur[2].strip() if cur and cur[2] else '')
                url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(title) + '&p=' + urllib.parse.quote(cur_p)
                xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
            except Exception as e:
                log('sky_cat item %s: %s' % (cid, e))
                try:
                    import traceback
                    log('sky_cat TB: ' + traceback.format_exc())
                except Exception:
                    pass
    except Exception as e:
        log('sky_cat vista %s: %s' % (cat, e))
        try:
            import traceback
            log('sky_cat TB: ' + traceback.format_exc())
        except Exception:
            pass
    xbmcplugin.endOfDirectory(HANDLE)


def tv_view():
    home_button()
    # SKY Intrattenimento spostato da SPORT -> TV (identica lista sky_cat_view)
    try:
        c = _sky_counts(CAT_INT)
        label_int = lbl(CAT_INT) + ' | CANALI ATTIVI: %d \u2022 CANALI IN SCADENZA: %d \u2022 CANALI SCADUTI: %d' % (c.get('ok', 0), c.get('soon', 0), c.get('exp', 0))
    except Exception:
        label_int = lbl(CAT_INT)
    li_int = xbmcgui.ListItem(label=label_int)
    li_int.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
    li_int.setInfo('video', {'title': CAT_INT, 'plot': 'Canali Sky Intrattenimento (Server 1 - API Heroku)'})
    url_int = BASE + '?action=skycat&cat=' + urllib.parse.quote(CAT_INT) + '&back=' + urllib.parse.quote(BASE + '?action=tv')
    xbmcplugin.addDirectoryItem(HANDLE, url_int, li_int, isFolder=True)

    channels = fetch_channels()
    groups = {}
    for ch in channels:
        if ch['group'].lower() in ('dazn', 'eventi'):
            continue
        groups.setdefault(ch['group'], []).append(ch)
    TV_ICONS = {
        'digitale terrestre': 'tv_icon.png',
        'eurosport': 'eurosport.png',
        'supertennis': 'supertennis.png',
        'eventi': 'eventi_icon.png',
        'dazn': 'dazn.png',
    }
    for group in sorted(groups):
        li = xbmcgui.ListItem(label=lbl(group))
        icon = TV_ICONS.get(group.lower(), 'tv_icon.png')
        li.setArt({'thumb': LOGO_BASE + icon, 'icon': LOGO_BASE + icon})
        li.setInfo('video', {'title': group})
        url = BASE + '?group=' + urllib.parse.quote(group) + '&deep=1&back=' + urllib.parse.quote(BASE + '?action=tv')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


TMDB_KEY = ADDON.getSetting('tmdb_key').strip() or '2e0b38cfb2936cec8ab1ce48e4335ac3'
TMDB_LANG = ADDON.getSetting('tmdb_language').strip() or 'it-IT'
TMDB_ADULT = ADDON.getSetting('tmdb_adult') == 'true'
TMDB_URL = 'https://api.themoviedb.org/3'
TMDB_IMG = 'https://image.tmdb.org/t/p/'

HOME_SECTIONS = [('Film', 'movie'), ('Serie TV', 'tv')]

FILM_CATS = [
    ('Popolari', 'popular'),
    ('In sala', 'now_playing'),
    ('Prossimamente', 'upcoming'),
    ('Più votati', 'top_rated'),
    ('Trending oggi', 'trending_day'),
    ('Trending settimana', 'trending_week'),
    ('Per genere', 'genres'),
    ('Per decennio', 'decades'),
    ('Tutto il catalogo', 'all'),
    ('Ricerca', 'search'),
]

TV_CATS = [
    ('Popolari', 'popular'),
    ('In onda oggi', 'airing_today'),
    ('In TV', 'on_the_air'),
    ('Più votate', 'top_rated'),
    ('Trending oggi', 'trending_day'),
    ('Trending settimana', 'trending_week'),
    ('Per genere', 'genres'),
    ('Per decennio', 'decades'),
    ('Tutto il catalogo', 'all'),
    ('Ricerca', 'search'),
]

ALL_SORTS = {
    'movie': [
        ('Popolarità', 'popularity.desc'),
        ('Voto medio', 'vote_average.desc'),
        ('Uscita più recente', 'primary_release_date.desc'),
        ('Più vecchi', 'primary_release_date.asc'),
        ('Titolo A-Z', 'original_title.asc'),
    ],
    'tv': [
        ('Popolarità', 'popularity.desc'),
        ('Voto medio', 'vote_average.desc'),
        ('Prima messa in onda', 'first_air_date.desc'),
        ('Più vecchie', 'first_air_date.asc'),
        ('Titolo A-Z', 'name.asc'),
    ],
}

DECADES = [str(y) for y in range(2020, 1880, -10)]


def tmdb_get(path, **params):
    params['api_key'] = TMDB_KEY
    params.setdefault('language', TMDB_LANG)
    r = requests.get(TMDB_URL + path, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def _tmdb_url(action, **params):
    if _VOD_SRC:
        params.setdefault('src', _VOD_SRC)
    return BASE + '?action=' + action + '&' + urllib.parse.urlencode(params)


def v2_get(url, base):
    try:
        r = requests.get(url, timeout=15, headers={
            'User-Agent': VIXSRC_UA,
            'Accept': 'text/html,application/xhtml+xml,application/json,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': base + '/',
            'Origin': base,
        })
        if r.status_code == 200 and r.text:
            return r.text
    except Exception:
        pass
    return ''


def resolve_v2(id_, mtype='movie', season='0', episode='0', title='', eptitle=''):
    base = 'https://videm.xyz'
    season_str = str(season or '0')
    episode_str = str(episode or '0')
    if mtype == 'tv':
        embed = base + '/embed/tv/%s/%s/%s' % (id_, season_str, episode_str)
    else:
        embed = base + '/embed/movie/%s' % id_
    html = v2_get(embed, base)
    m = re.search(r'var Q\s*=\s*(\{.*?\});', html, re.S)
    if not m:
        return None
    try:
        q = json.loads(m.group(1))
    except Exception:
        return None
    qid = urllib.parse.quote(str(q.get('id', id_)))
    qs = 'type=%s&id=%s&s=%s&e=%s' % (q.get('type', mtype), qid,
                                      q.get('s') or season_str, q.get('e') or episode_str)
    qt = urllib.parse.quote(str(q.get('t', '')))
    src = v2_get(base + '/api.php?a=sources&' + qs + '&t=' + qt, embed)
    try:
        j = json.loads(src)
    except Exception:
        j = None
    servers = [s for s in (j or {}).get('servers', []) if s.get('rm')] or (j or {}).get('servers', [])
    pick = None
    for s in servers:
        if 'ita' in (s.get('name') or '').lower():
            pick = s
            break
    if pick is None and servers:
        pick = servers[0]
    if not pick:
        return None
    play = v2_get(base + '/api.php?a=play&ref=' + urllib.parse.quote(str(pick.get('ref', ''))) + '&t=' + qt, embed)
    try:
        pj = json.loads(play)
    except Exception:
        pj = None
    purl = pj.get('url') if isinstance(pj, dict) else None
    ptype = pj.get('type', 'hls') if isinstance(pj, dict) else 'hls'
    if not purl:
        return None
    if purl.startswith('/'):
        purl = base + purl

    try:
        s_num = int(season or 0)
        e_num = int(episode or 0)
    except (TypeError, ValueError):
        s_num = 0
        e_num = 0

    if mtype == 'tv' and s_num > 0 and e_num > 0:
        if eptitle:
            player_title = '%s - S%d:E%d - %s' % (title, s_num, e_num, eptitle)
        else:
            player_title = '%s - S%d:E%d' % (title, s_num, e_num)
    else:
        player_title = title or pick.get('name') or 'VidAPI'

    li = xbmcgui.ListItem(label=lbl(player_title))
    li.setPath(purl)
    li.setInfo('video', {'title': player_title, 'tvshowtitle': '', 'season': 0, 'episode': 0, 'mediatype': 'video'})
    if ptype == 'hls' or purl.endswith('.m3u8'):
        headers = urllib.parse.urlencode({'User-Agent': VIXSRC_UA, 'Referer': embed, 'Origin': base})
        li.setProperty('inputstream', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', 'hls')
        li.setProperty('inputstream.adaptive.stream_headers', headers)
        li.setProperty('inputstream.adaptive.manifest_headers', headers)
        li.setProperty('inputstream.adaptive.license_key', '|' + headers)
    li.setProperty('isPlayable', 'true')
    return li


def v2_seasons_view(id_, back=''):
    back_button(back or (BASE + '?action=films'))
    try:
        j = tmdb_get('/tv/%s' % id_)
    except Exception:
        j = {}
    tname = html.unescape(j.get('name') or 'Sconosciuto')
    poster = j.get('poster_path')
    for s in j.get('seasons', []):
        n = s.get('season_number') or 0
        if n <= 0:
            continue
        label = 'Stagione %d' % n
        if s.get('air_date'):
            label += '  (%s)' % str(s['air_date'])[:4]
        if s.get('episode_count'):
            label += '  - %d ep.' % s['episode_count']
        li = xbmcgui.ListItem(label=lbl(label))
        if poster:
            li.setArt({'thumb': TMDB_IMG + 'w1280' + poster})
        li.setInfo('video', {'title': '%s - Stagione %d' % (tname, n), 'mediatype': 'season'})
        url = _tmdb_url('v2episodes', id=id_, s=str(n))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def v2_episodes_view(id_, s, back=''):
    back_button(back or (BASE + '?action=films'))
    try:
        j = tmdb_get('/tv/%s/season/%s' % (id_, s))
    except Exception:
        j = {}
    tname = html.unescape(j.get('name') or 'Sconosciuto')
    for ep in j.get('episodes', []):
        n = ep.get('episode_number') or 0
        ename = html.unescape(ep.get('name') or '')
        label = ('Ep. %02d  %s' % (n, ename)) if ename else ('Episodio %02d' % n)
        li = xbmcgui.ListItem(label=lbl(label))
        still = ep.get('still_path')
        if still:
            li.setArt({'thumb': TMDB_IMG + 'w1280' + still})
        etitle = '%s S%sE%s' % (tname, s, n)
        li.setInfo('video', {'title': etitle, 'plot': ep.get('overview') or '', 'mediatype': 'episode'})
        url = _tmdb_url('v2play', id=id_, mtype='tv', s=str(s), e=str(n), t=tname, ept=ename)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_add_item(it, mtype, back=''):
    title = html.unescape(it.get('title') or it.get('name') or '')
    date = it.get('release_date') or it.get('first_air_date') or ''
    label = title + ('  (' + date[:4] + ')' if len(date) >= 4 else '')
    li = xbmcgui.ListItem(label=lbl(label))
    poster = it.get('poster_path')
    li.setArt({'thumb': TMDB_IMG + 'w1280' + poster if poster else SQUARE_ICON})
    fan = it.get('backdrop_path')
    if fan:
        li.setArt({'fanart': TMDB_IMG + 'w1280' + fan})
    info = {'title': title, 'mediatype': 'movie' if mtype == 'movie' else 'tv',
            'plot': it.get('overview') or ''}
    if len(date) >= 4:
        try:
            info['year'] = int(date[:4])
        except ValueError:
            pass
    try:
        info['rating'] = float(it.get('vote_average') or 0)
    except (TypeError, ValueError):
        pass
    li.setInfo('video', info)
    if mtype == 'movie':
        li.setProperty('isPlayable', 'true')
        if _VOD_SRC == '2':
            url = _tmdb_url('v2play', id=it.get('id'), mtype='movie')
        else:
            url = _tmdb_url('mplayauto', q=title, back=back)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    else:
        if _VOD_SRC == '2':
            url = _tmdb_url('v2seasons', id=it.get('id'))
        else:
            url = _tmdb_url('mseasonsauto', q=title, back=back)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)


def tmdb_list(mtype, kind='', genre='', page=1, sort_by='', year='', back=''):
    if not back:
        if genre:
            back = BASE + '?action=genres&mt=' + urllib.parse.quote(mtype)
        elif year:
            back = BASE + '?action=decades&mt=' + urllib.parse.quote(mtype)
        elif kind:
            back = BASE + '?action=films' if kind.startswith('trending') else (BASE + '?action=allsorts&mt=' + urllib.parse.quote(mtype) if kind == 'all' else BASE + '?action=cats&mt=' + urllib.parse.quote(mtype))
        else:
            back = BASE + '?action=films'
    back_button(back)
    page = int(page)
    if kind == 'trending_day':
        path = '/trending/%s/day' % mtype
        params = {'page': page}
    elif kind == 'trending_week':
        path = '/trending/%s/week' % mtype
        params = {'page': page}
    elif genre:
        path = '/discover/' + mtype
        params = {'with_genres': genre, 'sort_by': 'popularity.desc', 'page': page}
    elif kind == 'all':
        path = '/discover/' + mtype
        params = {'sort_by': sort_by or 'popularity.desc', 'page': page}
        if sort_by == 'vote_average.desc':
            params['vote_count.gte'] = 100
        if year:
            if mtype == 'movie':
                params['primary_release_date.gte'] = '%s-01-01' % year
                params['primary_release_date.lte'] = '%d-12-31' % (int(year) + 9)
            else:
                params['first_air_date.gte'] = '%s-01-01' % year
                params['first_air_date.lte'] = '%d-12-31' % (int(year) + 9)
    else:
        path = '/%s/%s' % (mtype, kind)
        params = {'page': page}
    j = tmdb_get(path, **params)
    if mtype == 'all':
        xbmcplugin.setContent(HANDLE, 'movies')
    else:
        xbmcplugin.setContent(HANDLE, 'movies' if mtype == 'movie' else 'tvshows')
    cur = _tmdb_url('list', mt=mtype, kind=kind, genre=genre, page=str(page), sort_by=sort_by, year=year)
    for it in j.get('results', []):
        tmdb_add_item(it, it.get('media_type') or mtype, back=cur)
    if page < (j.get('total_pages') or 1) and j.get('results'):
        li = xbmcgui.ListItem(label=lbl('Prossima pagina  ►'))
        
        url = _tmdb_url('list', mt=mtype, kind=kind, genre=genre, page=str(page + 1), sort_by=sort_by, year=year, back=back)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_allsorts(mtype, back=''):
    back_button(back or (BASE + '?action=cats&mt=' + urllib.parse.quote(mtype)))
    allsorts_url = BASE + '?action=allsorts&mt=' + urllib.parse.quote(mtype)
    for label, sort_by in ALL_SORTS.get(mtype, ALL_SORTS['movie']):
        li = xbmcgui.ListItem(label=lbl(label))
        
        url = _tmdb_url('list', mt=mtype, kind='all', sort_by=sort_by, page='1', back=allsorts_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_decades(mtype, back=''):
    back_button(back or (BASE + '?action=cats&mt=' + urllib.parse.quote(mtype)))
    decades_url = BASE + '?action=decades&mt=' + urllib.parse.quote(mtype)
    for d in DECADES:
        li = xbmcgui.ListItem(label=lbl(d + 's'))
        
        url = _tmdb_url('list', mt=mtype, kind='all', sort_by='popularity.desc', year=d, page='1', back=decades_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_cats(mtype, back=''):
    back_button(back or (BASE + '?action=films'))
    cats = FILM_CATS if mtype == 'movie' else TV_CATS
    cats_url = BASE + '?action=cats&mt=' + urllib.parse.quote(mtype)
    for label, kind in cats:
        li = xbmcgui.ListItem(label=lbl(label))
        
        if kind == 'genres':
            url = _tmdb_url('genres', mt=mtype, back=cats_url)
        elif kind == 'decades':
            url = _tmdb_url('decades', mt=mtype, back=cats_url)
        elif kind == 'all':
            url = _tmdb_url('allsorts', mt=mtype, back=cats_url)
        elif kind == 'search':
            url = _tmdb_url('search', back=cats_url)
        else:
            url = _tmdb_url('list', mt=mtype, kind=kind, page='1', back=cats_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_genres(mtype, back=''):
    back_button(back or (BASE + '?action=cats&mt=' + urllib.parse.quote(mtype)))
    j = tmdb_get('/genre/%s/list' % mtype)
    genres_url = BASE + '?action=genres&mt=' + urllib.parse.quote(mtype)
    for g in sorted(j.get('genres', []), key=lambda x: x['name']):
        li = xbmcgui.ListItem(label=lbl(g['name']))
        
        url = _tmdb_url('list', mt=mtype, genre=str(g['id']), page='1', back=genres_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_details(mtype, id_, back=''):
    back_button(back or (BASE + '?action=films'))
    j = tmdb_get('/%s/%s' % (mtype, id_), append_to_response='credits,similar')
    title = html.unescape(j.get('title') or j.get('name') or '')
    li = xbmcgui.ListItem(label=lbl(title))
    info = {'title': title, 'plot': j.get('overview') or ''}
    date = j.get('release_date') or j.get('first_air_date') or ''
    if len(date) >= 4:
        try:
            info['year'] = int(date[:4])
        except ValueError:
            pass
    try:
        info['rating'] = float(j.get('vote_average') or 0)
    except (TypeError, ValueError):
        pass
    genres = [g.get('name', '') for g in j.get('genres', [])]
    if genres:
        info['genre'] = genres
    credits = j.get('credits', {})
    info['cast'] = [c.get('name', '') for c in credits.get('cast', [])[:10]]
    info['director'] = [c.get('name', '') for c in credits.get('crew', [])
                        if c.get('job') == 'Director'][:5]
    li.setInfo('video', info)
    poster = j.get('poster_path')
    if poster:
        li.setArt({'thumb': TMDB_IMG + 'w500' + poster})
    fan = j.get('backdrop_path')
    if fan:
        li.setArt({'fanart': TMDB_IMG + 'w1280' + fan})
    xbmcgui.Dialog().info(li)

    play = xbmcgui.ListItem(label=lbl('▶  Riproduci con VixSrc' if _VOD_SRC == '2' else '▶  Riproduci con Mandrakodi'))
    play.setArt({'thumb': SQUARE_ICON})
    details_url = BASE + '?action=details&mt=' + urllib.parse.quote(mtype) + '&id=' + urllib.parse.quote(id_)
    if _VOD_SRC == '2':
        if mtype == 'movie':
            url = _tmdb_url('v2play', id=id_, mtype='movie')
        else:
            url = _tmdb_url('v2seasons', id=id_)
    else:
        url = _tmdb_url('msearch', q=title, mt=mtype, back=details_url)
    xbmcplugin.addDirectoryItem(HANDLE, url, play, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_search(query='', page=1, back=''):
    back_button(back or (BASE + '?action=films'))
    page = int(page)
    did_kbd = False
    if not query:
        kb = xbmc.Keyboard('', 'Cerca in TMDB')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            xbmcplugin.endOfDirectory(HANDLE)
            return
        query = kb.getText().strip()
        did_kbd = True
    j = tmdb_get('/search/multi', query=query, include_adult='true' if TMDB_ADULT else 'false', page=page)
    xbmcplugin.setContent(HANDLE, 'movies')
    search_url = BASE + '?action=search&q=' + urllib.parse.quote(query) + '&page=' + str(page)
    for it in j.get('results', []):
        if it.get('media_type') in ('movie', 'tv'):
            tmdb_add_item(it, it.get('media_type'), back=search_url)
    if page < (j.get('total_pages') or 1) and j.get('results'):
        li = xbmcgui.ListItem(label=lbl('Prossima pagina  ►'))
        
        url = _tmdb_url('search', q=query, page=str(page + 1), back=back)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)
    if did_kbd:
        xbmc.executebuiltin('Container.Update("%s", replace)' % _tmdb_url('search', q=query, page='1'))


CS_URL_FILE = 'https://raw.githubusercontent.com/mandrakodi/mandrakodi.github.io/main/data/cs_url.txt'
SC_DEFAULT = 'https://streamingunity.vip/'


def mandra_cs():
    try:
        return requests.get(CS_URL_FILE, timeout=10).text.strip()
    except Exception:
        return SC_DEFAULT


def man_title(it):
    t = clean_title(it.get('title', ''))
    t = re.sub(r'^SL\s*\d+\s*\*+\s*', '', t)
    return t.strip()


def resolve_scws(parIn, title, eptitle='', season=0, episode=0):
    try:
        s = int(season) or None
    except (TypeError, ValueError):
        s = None
    try:
        e = int(episode) or None
    except (TypeError, ValueError):
        e = None
    cs = SC_DEFAULT
    try:
        cs = mandra_cs()
        base = cs + 'it/iframe/' + parIn
        rnd = UA
        r = requests.get(base, headers={'user-agent': rnd}, timeout=25)
        r.raise_for_status()
        page = r.text.replace('\n', '').replace('\r', '').replace('\t', '')
        m3u8Url = ''
        for src in re.findall(r'src="(.*?)"', page):
            if 'vixcloud.co' in src:
                m3u8Url = src
        if not m3u8Url:
            raise Exception('embed vixcloud non trovato')
        full_embed = m3u8Url.replace('&amp;', '&')
        r2 = requests.get(full_embed, headers={'user-agent': rnd}, timeout=25)
        r2.raise_for_status()
        page2 = r2.text.replace('\n', '').replace('\r', '').replace('\t', '')
        mp = page2[page2.find('masterPlaylist') if page2.find('masterPlaylist') >= 0 else 0:]
        mtok = re.search(r"'token':\s*'([^']+)'", mp)
        mexp = re.search(r"'expires':\s*'([^']+)'", mp)
        murl = re.search(r"url:\s*'([^']+)'", mp)
        if not (mtok and mexp and murl):
            raise Exception('masterPlaylist non trovato')
        urlSc = murl.group(1)
        sep = '&' if '?' in urlSc else '?'
        urlSc = urlSc + sep + 'token=' + mtok.group(1) + '&expires=' + mexp.group(1) + '&n=1'
        if 'canPlayFHD=1' in full_embed:
            urlSc += '&h=1'
        if 'b=1' in full_embed:
            urlSc += '&b=1'
    except Exception as e:
        xbmc.log('KODIAKSO scws resolve ERR: ' + str(e), xbmc.LOGERROR)
        notify(title or parIn, 'Impossibile riprodurre il contenuto', True)
        return xbmcgui.ListItem()

    hdrs = 'User-Agent=' + UA + '&Referer=' + cs + '&Origin=' + cs + '&verifypeer=false'
    if s and e:
        if eptitle:
            player_title = '%s - S%d:E%d - %s' % (title, s, e, eptitle)
        else:
            player_title = '%s - S%d:E%d' % (title, s, e)
    else:
        player_title = title or ''

    li = xbmcgui.ListItem(path=urlSc, label=lbl(player_title), offscreen=True)
    li.setInfo('video', {'title': player_title, 'tvshowtitle': '', 'season': 0, 'episode': 0, 'mediatype': 'video'})
    li.setContentLookup(False)
    li.setMimeType('application/x-mpegURL')
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'hls')
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    li.setProperty('inputstream.adaptive.license_key', '|' + hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    return li


def mandra_auto_movie(query):
    try:
        data = requests.get(API + '?numTest=A1A332A&search=' + urllib.parse.quote(query),
                            headers={'User-Agent': API_UA}, timeout=25).json()
    except Exception as e:
        xbmc.log('KODIAKSO mandra auto ERR: ' + str(e), xbmc.LOGERROR)
        notify(query or 'Film', 'Errore ricerca', True)
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return
    for it in data.get('items', []):
        mr = it.get('myresolve', '') or ''
        if mr.startswith('scws2@@'):
            par = mr.split('@@', 1)[1]
            title = man_title(it) or query
            li = resolve_scws(par, title)
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
            return
    notify(query or 'Film', 'Impossibile riprodurre il contenuto', True)
    xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())


def mandra_auto_series(query, back=''):
    try:
        data = requests.get(API + '?numTest=A1A332A&mode=1&search=' + urllib.parse.quote(query),
                            headers={'User-Agent': API_UA}, timeout=25).json()
    except Exception as e:
        xbmc.log('KODIAKSO mandra series ERR: ' + str(e), xbmc.LOGERROR)
        notify(query or 'Serie', 'Errore ricerca', True)
        back_button(back)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for it in data.get('items', []):
        ext = it.get('externallink', '') or ''
        m = re.search(r'code=([^&]+)', ext)
        if m:
            mandra_season_view(m.group(1), back)
            return
    notify(query or 'Serie', 'Impossibile riprodurre il contenuto', True)
    back_button(back)
    xbmcplugin.endOfDirectory(HANDLE)


def mandra_search_view(query, mtype='', back=''):
    back_button(back or (BASE + '?action=films'))
    if not query:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    data = requests.get(API + '?numTest=A1A332A' + ('&mode=1' if mtype == 'tv' else '') + '&search=' + urllib.parse.quote(query),
                        headers={'User-Agent': API_UA}, timeout=25).json()
    xbmcplugin.setContent(HANDLE, 'movies' if mtype == 'movie' else 'tvshows')
    msearch_url = BASE + '?action=msearch&q=' + urllib.parse.quote(query) + '&mt=' + urllib.parse.quote(mtype)
    added = 0
    for it in data.get('items', []):
        title = man_title(it)
        thumb = it.get('thumbnail') or SQUARE_ICON
        fan = it.get('fanart') or ''
        info = it.get('info') or ''
        li = xbmcgui.ListItem(label=lbl(title))
        li.setArt({'thumb': thumb})
        if fan:
            li.setArt({'fanart': fan})
        li.setInfo('video', {'title': title, 'plot': info})
        mr = it.get('myresolve', '') or ''
        ext = it.get('externallink', '') or ''
        if mr.startswith('scws2@@'):
            par = mr.split('@@', 1)[1]
            li.setProperty('isPlayable', 'true')
            url = _tmdb_url('mplay', p=par, t=title)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
            added += 1
        elif ext and 'mode=2&code=' in ext:
            m = re.search(r'code=([^&]+)', ext)
            if m:
                li.setProperty('isPlayable', 'false')
                url = _tmdb_url('mseason', code=m.group(1), back=msearch_url)
                xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
                added += 1
    if not added:
        li = xbmcgui.ListItem(label=lbl('Nessun risultato'))
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('msearch', q=query), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def _tmdb_season_posters(show_title):
    try:
        j_search = tmdb_get('/search/tv', query=show_title)
        results = j_search.get('results', [])
        if not results:
            return {}, None
        show_id = results[0]['id']
        tv_data = tmdb_get('/tv/%s' % show_id)
        fanart = tv_data.get('backdrop_path')
        fanart_url = (TMDB_IMG + 'w1280' + fanart) if fanart else None
        
        posters = {}
        for s in tv_data.get('seasons', []):
            sn = s.get('season_number')
            sp = s.get('poster_path') or tv_data.get('poster_path')
            if sn and sp:
                posters[str(sn)] = TMDB_IMG + 'w1280' + sp
        return posters, fanart_url
    except Exception as e:
        xbmc.log('KODIAKSO season posters ERR: ' + str(e), xbmc.LOGERROR)
        return {}, None


def mandra_season_view(code, back=''):
    back_button(back or (BASE + '?action=films'))
    xbmcplugin.setContent(HANDLE, 'tvshows')
    season_url = BASE + '?action=mseason&code=' + urllib.parse.quote(code)
    added = False
    try:
        cs = mandra_cs()
        url = cs + 'it/titles/' + urllib.parse.quote(code)
        r = requests.get(url, headers={'user-agent': UA}, timeout=15)
        if r.status_code == 200:
            m = re.search(r'<div id="app" data-page="(.*?)"', r.text)
            if m:
                props = json.loads(m.group(1).replace('&quot;', '"'))['props']
                title_obj = props.get('title', {})
                show_name = html.unescape(title_obj.get('name') or '')
                
                # Fetch HD season-specific posters from TMDB
                tmdb_posters, tmdb_fanart = _tmdb_season_posters(show_name or code.replace('-', ' '))
                
                su_poster = SQUARE_ICON
                su_fanart = tmdb_fanart
                for im in title_obj.get('images', []):
                    if im.get('type') == 'poster' and im.get('filename') and su_poster == SQUARE_ICON:
                        su_poster = 'https://cdn.streamingunity.vip/images/' + im['filename']
                    elif im.get('type') == 'background' and im.get('filename') and not su_fanart:
                        su_fanart = 'https://cdn.streamingunity.vip/images/' + im['filename']
                
                seasons = title_obj.get('seasons', [])
                for s in seasons:
                    n = s.get('number')
                    if n and n > 0:
                        s_num = str(n)
                        par = f"{code}---{s_num}"
                        stitle = f"Stagione {s_num}"
                        li = xbmcgui.ListItem(label=lbl(stitle))
                        
                        # Season-specific poster from TMDB if available
                        p_url = tmdb_posters.get(s_num) or su_poster
                        art = {'thumb': p_url, 'poster': p_url, 'icon': p_url}
                        if su_fanart:
                            art['fanart'] = su_fanart
                        li.setArt(art)
                        li.setInfo('video', {'title': stitle})
                        url_item = _tmdb_url('mepisodes', par=par, back=season_url)
                        xbmcplugin.addDirectoryItem(HANDLE, url_item, li, isFolder=True)
                        added = True
    except Exception as e:
        xbmc.log('KODIAKSO su seasons ERR: ' + str(e), xbmc.LOGERROR)

    if not added:
        try:
            data = requests.get(API + '?numTest=A1A356&mode=2&code=' + urllib.parse.quote(code),
                                headers={'User-Agent': API_UA}, timeout=25).json()
            for it in data.get('items', []):
                mr = it.get('myresolve', '') or ''
                if not mr.startswith('seriesc@@'):
                    continue
                par = mr.split('@@', 1)[1]
                title = man_title(it) or ('Stagione ' + par.split('---')[-1])
                li = xbmcgui.ListItem(label=lbl(title))
                li.setArt({'thumb': it.get('thumbnail') or SQUARE_ICON})
                if it.get('fanart'):
                    li.setArt({'fanart': it['fanart']})
                li.setInfo('video', {'title': title, 'plot': it.get('info') or ''})
                url = _tmdb_url('mepisodes', par=par, back=season_url)
                xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
        except Exception as e:
            xbmc.log('KODIAKSO api seasons ERR: ' + str(e), xbmc.LOGERROR)

    xbmcplugin.endOfDirectory(HANDLE)


def mandra_episodes_view(par, back=''):
    back_button(back or (BASE + '?action=films'))
    idSea, numSea = par.split('---')
    cs = mandra_cs()
    url = cs + 'it/titles/' + idSea + '/season-' + numSea
    r = requests.get(url, headers={'user-agent': UA}, timeout=30)
    r.raise_for_status()
    m = re.search(r'<div id="app" data-page="(.*?)"', r.text)
    if not m:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    props = json.loads(m.group(1).replace('&quot;', '"'))['props']
    show_name = html.unescape(props['title']['name'])
    cover = SQUARE_ICON
    for im in props['title'].get('images', []):
        if im.get('type') == 'cover':
            cover = 'https://cdn.streamingunity.vip/images/' + im['filename']
            break
    xbmcplugin.setContent(HANDLE, 'episodes')
    for ep in props['loadedSeason'].get('episodes', []):
        n = ep.get('number', '')
        try:
            numep = int(n)
            label = '%sx%02d %s' % (numSea, numep, (ep.get('name') or ('Episodio ' + str(numep))))
        except (TypeError, ValueError):
            label = ep.get('name') or ('Episodio ' + str(n))
        name = html.unescape(ep.get('name') or label)
        li = xbmcgui.ListItem(label=lbl(label))
        plot = html.unescape(ep.get('plot') or '')
        try:
            s_int = int(numSea)
        except (TypeError, ValueError):
            s_int = 0
        try:
            e_int = int(ep.get('number') or 0)
        except (TypeError, ValueError):
            e_int = 0
        info = {'title': name, 'plot': plot, 'mediatype': 'episode',
                'tvshowtitle': show_name, 'season': s_int, 'episode': e_int}
        li.setInfo('video', info)
        thumb = cover
        if ep.get('images'):
            try:
                thumb = 'https://cdn.streamingunity.vip/images/' + ep['images'][0]['filename']
            except Exception:
                pass
        li.setArt({'thumb': thumb})
        li.setProperty('isPlayable', 'true')
        parIn = idSea + '?episode_id=' + str(ep['id'])
        url = _tmdb_url('mplay', p=parIn, t=show_name, ept=name, s=numSea, e=numep)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def vod_view():
    home_button()
    vod1_url = BASE + '?action=films'
    vod2_url = BASE + '?action=films&src=2'

    li1 = xbmcgui.ListItem(label=lbl('VOD 1'))
    li1.setArt({'thumb': LOGO_BASE + 'netflix.png', 'icon': LOGO_BASE + 'netflix.png'})
    li1.setInfo('video', {'title': 'VOD 1', 'plot': 'Catalogo VOD 1 (StreamingUnity / VixCloud)'})
    xbmcplugin.addDirectoryItem(HANDLE, vod1_url, li1, isFolder=True)

    li2 = xbmcgui.ListItem(label=lbl('VOD 2'))
    li2.setArt({'thumb': LOGO_BASE + 'netflix.png', 'icon': LOGO_BASE + 'netflix.png'})
    li2.setInfo('video', {'title': 'VOD 2', 'plot': 'Catalogo VOD 2 (VidAPI / Videm)'})
    xbmcplugin.addDirectoryItem(HANDLE, vod2_url, li2, isFolder=True)

    xbmcplugin.endOfDirectory(HANDLE)


def films_view():
    back_button(BASE + '?action=vod')
    films_url = BASE + '?action=films'
    li = xbmcgui.ListItem(label=lbl('Ricerca'))
    
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('search', back=films_url), li, isFolder=True)
    for label, window in (('Trending oggi', 'day'), ('Trending settimana', 'week')):
        li = xbmcgui.ListItem(label=lbl(label))
        
        url = _tmdb_url('list', mt='all', kind='trending_' + window, page='1', back=films_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    for label, mtype in HOME_SECTIONS:
        li = xbmcgui.ListItem(label=lbl(label))
        
        url = _tmdb_url('cats', mt=mtype, back=films_url)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


AK47_BASE = 'https://zerohazaarop.store/'
AK47_SALT = b'ak47/v2/prk'
AK47_UA = 'Dalvik/2.1.0 (Linux; Android 13)'
SZX_BASE = 'https://cdn-stream.top/'
SZX_DIGEST = bytes.fromhex('1676ec7db4771b0d826d70369b579684b182d2c0133be041bdd55f5d6d79a98b')
SZX_SALT = b'sportzx/v2/prk'
SZX_UA = 'Dalvik/2.1.0 (Linux; Android 13)'
_SZX = {'events': None, 'cats': None, 'channels': {}}
_SZX_TS = {}
_SZX_TTL = {'events': 600, 'cats': 1800, 'channels': 1200}
_SZX_API_URL = ''
_SZX_API_TS = 0
# SportzX v3 (reverse-engineered client): la chiave di decrittazione non e' piu
# nel payload (versione 3) ma derivata da una password. La password puo' essere
# aggiornata dalle impostazioni (szx_password) senza toccare il codice.
SZX_APP_PASSWORD = 'oAR80SGuX3EEjUGFRwLFKBTiris='
SZX_PW_CHARSET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+!@#$%&='
SZX_FIREBASE_API_KEY = 'AIzaSyCTIFo_vw_-XrjzDeE1yG4KuAqGLchzZ0M'
SZX_FIREBASE_PROJECT = 'sportzx-afe67'
SZX_FIREBASE_APP_ID = '1:234785582029:android:f5f9299eaa7a0d73'
SZX_FIREBASE_CERT = 'A0047CD121AE5F71048D41854702C52814E2AE2B'
SZX_FIREBASE_NUM = '234785582029'
SZX6_MIRROR = 'https://raw.githubusercontent.com/mdjamsad9/dudetvapi/main/public_decrypted/'
_SZ6 = {}
_SZ6_TS = {}
_SZ6_TTL = {'events': 900, 'channels': 1800}
_DDY = {'data': None, 'ts': 0}
_DDY_TTL = 1800

_SZX_SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]
_SZX_RSBOX = [0] * 256
for _szx_i, _szx_v in enumerate(_SZX_SBOX):
    _SZX_RSBOX[_szx_v] = _szx_i
_SZX_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d]


def _szx_xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11b
    return a & 0xff


def _szx_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _szx_xtime(a)
        b >>= 1
    return r


def _szx_expand_key(key):
    nk = len(key) // 4
    nr = nk + 6
    w = [list(key[4 * i:4 * i + 4]) for i in range(nk)]
    for i in range(nk, 4 * (nr + 1)):
        t = list(w[i - 1])
        if i % nk == 0:
            t = t[1:] + t[:1]
            t = [_SZX_SBOX[b] for b in t]
            t[0] ^= _SZX_RCON[i // nk - 1]
        elif nk > 6 and i % nk == 4:
            t = [_SZX_SBOX[b] for b in t]
        w.append([w[i - nk][j] ^ t[j] for j in range(4)])
    return w, nr


def _szx_round_key(s, w, rnd):
    for j in range(4):
        for k in range(4):
            s[4 * j + k] ^= w[4 * rnd + j][k]


def _szx_inv_shift_rows(s):
    for r in range(1, 4):
        row = [s[4 * c + r] for c in range(4)]
        row = row[-r:] + row[:-r]
        for c in range(4):
            s[4 * c + r] = row[c]
    return s


def _szx_inv_sub_bytes(s):
    return [_SZX_RSBOX[b] for b in s]


def _szx_inv_mix_columns(s):
    for c in range(4):
        o = 4 * c
        a0, a1, a2, a3 = s[o], s[o + 1], s[o + 2], s[o + 3]
        s[o] = _szx_mul(a0, 14) ^ _szx_mul(a1, 11) ^ _szx_mul(a2, 13) ^ _szx_mul(a3, 9)
        s[o + 1] = _szx_mul(a0, 9) ^ _szx_mul(a1, 14) ^ _szx_mul(a2, 11) ^ _szx_mul(a3, 13)
        s[o + 2] = _szx_mul(a0, 13) ^ _szx_mul(a1, 9) ^ _szx_mul(a2, 14) ^ _szx_mul(a3, 11)
        s[o + 3] = _szx_mul(a0, 11) ^ _szx_mul(a1, 13) ^ _szx_mul(a2, 9) ^ _szx_mul(a3, 14)
    return s


def _szx_decrypt_block(key, ct):
    w, nr = _szx_expand_key(key)
    s = list(ct)
    _szx_round_key(s, w, nr)
    for rnd in range(nr - 1, 0, -1):
        _szx_inv_shift_rows(s)
        s = _szx_inv_sub_bytes(s)
        _szx_round_key(s, w, rnd)
        _szx_inv_mix_columns(s)
    _szx_inv_shift_rows(s)
    s = _szx_inv_sub_bytes(s)
    _szx_round_key(s, w, 0)
    return bytes(s)


def _szx_aes_cbc_decrypt(key, iv, ct):
    pt = bytearray()
    prev = iv
    for off in range(0, len(ct), 16):
        blk = _szx_decrypt_block(key, ct[off:off + 16])
        pt += bytes(a ^ b for a, b in zip(blk, prev))
        prev = ct[off:off + 16]
    return bytes(pt)


def _szx_new_derive(s):
    data = s.encode('utf-8', 'replace')
    n = len(data)
    if n == 0:
        return b'', b''
    u = 0x811c9dc5
    for ch in data:
        u = ((u ^ ch) * 0x1000193) & 0xFFFFFFFF
    key = bytearray()
    for i in range(16):
        b = data[i % n]
        u = ((u * 0x1f) + (i ^ b)) & 0xFFFFFFFF
        key.append(SZX_PW_CHARSET[u % len(SZX_PW_CHARSET)])
    u = 0x811c832a
    for ch in data:
        u = ((u ^ ch) * 0x1000193) & 0xFFFFFFFF
    iv = bytearray()
    idx = acc = 0
    while len(iv) < 16:
        b = data[idx % n]
        u = ((u * 0x1d) + (acc ^ b)) & 0xFFFFFFFF
        iv.append(SZX_PW_CHARSET[u % len(SZX_PW_CHARSET)])
        idx += 3
        acc = (acc + 7) & 0xFFFFFFFF
    return bytes(key), bytes(iv)


def _szx_new_decrypt(data, password):
    try:
        b = data.strip()
        b += '=' * (-len(b) % 4)
        blob = base64.urlsafe_b64decode(b)
        if not blob or blob[0] not in (2, 3):
            return None
        ct = blob[1:]
        if len(ct) % 16 != 0:
            ct = blob
        if len(ct) == 0 or len(ct) % 16 != 0:
            return None
        key, iv = _szx_new_derive(password)
        pt = _szx_aes_cbc_decrypt(key, iv, ct)
        pad = pt[-1] if pt else 0
        if 1 <= pad <= 16:
            pt = pt[:-pad]
        if not pt:
            return None
        return pt
    except Exception:
        return None


def _szx_firebase_api_url():
    try:
        import base64 as _b64
        import os as _os
        raw = bytearray(_os.urandom(17))
        raw[0] = (raw[0] & 0x0F) | 0x70
        fid = _b64.urlsafe_b64encode(raw).decode().rstrip('=')[:22]
        ih = {'Accept': 'application/json', 'Content-Type': 'application/json',
              'User-Agent': SZX_UA, 'X-Android-Cert': SZX_FIREBASE_CERT,
              'X-Android-Package': 'com.sportzx.live',
              'x-goog-api-key': SZX_FIREBASE_API_KEY}
        ib = {'fid': fid, 'appId': SZX_FIREBASE_APP_ID, 'authVersion': 'FIS_v2',
              'sdkVersion': 'a:18.0.0'}
        r = requests.post('https://firebaseinstallations.googleapis.com/v1/projects/%s/installations' % SZX_FIREBASE_PROJECT,
                          json=ib, headers=ih, timeout=20)
        r.raise_for_status()
        tok = r.json().get('authToken', {}).get('token')
        if not tok:
            return ''
        ch = {'Content-Type': 'application/json', 'User-Agent': SZX_UA,
              'X-Android-Cert': SZX_FIREBASE_CERT,
              'X-Android-Package': 'com.sportzx.live', 'X-Firebase-RC-Fetch-Type': 'BASE/1',
              'X-Goog-Api-Key': SZX_FIREBASE_API_KEY,
              'X-Goog-Firebase-Installations-Auth': tok}
        cb = {'appVersion': '2.1', 'firstOpenTime': '2025-11-10T16:00:00.000Z',
              'timeZone': 'Europe/Rome', 'appInstanceIdToken': tok, 'languageCode': 'it-IT',
              'appBuild': '12', 'appInstanceId': fid, 'countryCode': 'IT',
              'appId': SZX_FIREBASE_APP_ID, 'platformVersion': '33', 'sdkVersion': '22.1.2',
              'packageName': 'com.sportzx.live'}
        r = requests.post('https://firebaseremoteconfig.googleapis.com/v1/projects/%s/namespaces/firebase:fetch' % SZX_FIREBASE_NUM,
                          json=cb, headers=ch, timeout=20)
        r.raise_for_status()
        return r.json().get('entries', {}).get('api_url') or ''
    except Exception as e:
        log('szx firebase api url: %s' % e)
        return ''


def szx_base():
    global _SZX_API_URL, _SZX_API_TS
    cfg = ADDON.getSetting('szx_base').strip()
    if cfg:
        return cfg if cfg.endswith('/') else cfg + '/'
    now = time.time()
    if _SZX_API_URL and (now - _SZX_API_TS) < 21600:
        return _SZX_API_URL
    url = _szx_firebase_api_url()
    if url:
        _SZX_API_URL = url if url.endswith('/') else url + '/'
        _SZX_API_TS = now
    return _SZX_API_URL or SZX_BASE


def _szx_raw_key_iv():
    k = ADDON.getSetting('szx_key').strip()
    v = ADDON.getSetting('szx_iv').strip()
    if not k or not v:
        return None, None

    def _dec(s):
        s = s.strip()
        try:
            return bytes.fromhex(s)
        except Exception:
            pass
        try:
            return base64.b64decode(s + '=' * (-len(s) % 4))
        except Exception:
            pass
        return None

    kb, vb = _dec(k), _dec(v)
    if kb and vb:
        return kb, vb
    return None, None


def _szx_aes_cbc_try(blob, key, iv):
    cands = [
        (blob[1:], iv),
        (blob[17:], blob[1:17]),
        (blob[17:-32], blob[1:17]),
    ]
    for ct, use_iv in cands:
        if len(ct) == 0 or len(ct) % 16 != 0:
            continue
        try:
            pt = _szx_aes_cbc_decrypt(key, use_iv, ct)
            pad = pt[-1] if pt else 0
            if 1 <= pad <= 16:
                pt = pt[:-pad]
            if pt:
                return pt
        except Exception:
            continue
    return None


def _szx_decrypt(data):
    try:
        b = data.strip()
        b += '=' * (-len(b) % 4)
        blob = base64.urlsafe_b64decode(b)
    except Exception:
        return None
    if not blob or blob[0] not in (2, 3):
        return None
    rk, rv = _szx_raw_key_iv()
    if rk and rv:
        d = _szx_aes_cbc_try(blob, rk, rv)
        if d:
            return d
    pw = ADDON.getSetting('szx_password').strip() or SZX_APP_PASSWORD
    d = _szx_new_decrypt(data, pw)
    if d:
        return d
    return _szx_legacy_decrypt(data)


def _szx_legacy_decrypt(data):
    try:
        b = data.rstrip('=')
        blob = base64.urlsafe_b64decode(b + '=' * (-len(b) % 4))
        if len(blob) < 49 or blob[0] != 2:
            return None
        iv = blob[1:17]
        tag = blob[-32:]
        ct = blob[17:-32]
        kd = hmac.new(SZX_SALT, SZX_DIGEST, hashlib.sha256).digest()
        enc = hmac.new(kd, b'enc', hashlib.sha256).digest()
        mac = hmac.new(kd, b'mac', hashlib.sha256).digest()
        if not hmac.compare_digest(hmac.new(mac, blob[:-32], hashlib.sha256).digest(), tag):
            return None
        pt = _szx_aes_cbc_decrypt(enc, iv, ct)
        pad = pt[-1] if pt else 0
        if 1 <= pad <= 16:
            pt = pt[:-pad]
        return bytes((((b << 5) | (b >> 3)) & 255) ^ SZX_DIGEST[i % 32] for i, b in enumerate(pt))
    except Exception:
        return None


def _szx_fetch(name):
    last = None
    base = szx_base()
    for attempt in range(2):
        try:
            r = requests.get(base + name, timeout=20,
                             headers={'User-Agent': SZX_UA})
            r.raise_for_status()
            return r.json().get('data', '')
        except Exception as e:
            last = e
            time.sleep(1)
    log('szx fetch %s: %s' % (name, last))
    return ''


def _szx_load(key, name, eid=''):
    now = time.time()
    if _SZX.get(key) is not None and (now - _SZX_TS.get(key, 0)) < _SZX_TTL.get(key, 600):
        return _SZX[key]
    raw = _szx_fetch(name)
    d = _szx_decrypt(raw) if raw else None
    try:
        val = json.loads(d.decode('utf-8', 'replace')) if d else []
    except Exception:
        val = []
    _SZX[key] = val
    _SZX_TS[key] = now
    return val


def _sz6_fetch(name):
    last = None
    for attempt in range(2):
        try:
            r = requests.get(SZX6_MIRROR + name, timeout=20, headers={'User-Agent': UA})
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            time.sleep(1)
    log('sz6 fetch %s: %s' % (name, last))
    return None


def _sz6_events(force=False):
    if not force and _SZ6.get('events') is not None and (time.time() - _SZ6_TS.get('events', 0)) < _SZ6_TTL['events']:
        return _SZ6['events']
    data = _sz6_fetch('events.json')
    val = data if isinstance(data, list) else []
    _SZ6['events'] = val
    _SZ6_TS['events'] = time.time()
    return val


def _sz6_channels(eid, force=False):
    key = 'ch_%s' % eid
    if not force and key in _SZ6 and (time.time() - _SZ6_TS.get(key, 0)) < _SZ6_TTL['channels']:
        return _SZ6[key]
    data = _sz6_fetch('channels/%s.json' % eid)
    val = data if isinstance(data, list) else []
    _SZ6[key] = val
    _SZ6_TS[key] = time.time()
    return val


def _sz6_sortkey(c):
    try:
        t = int(c.get('type') or '0')
    except Exception:
        t = 0
    return (1 if t == 1 else 0, (c.get('title') or '').lower())


def _sz6_ordered(chs):
    out = []
    for c in sorted(chs, key=_sz6_sortkey):
        try:
            t = int(c.get('type') or '0')
        except Exception:
            t = 0
        if t == 2:
            continue
        out.append(c)
    return out


def _sz6_thumb(url):
    if not isinstance(url, str) or not url.startswith('http'):
        return ''
    u = url.lower().split('?')[0]
    if 'enc_avif' in url.lower() or '.svg' in u:
        return ''
    if re.search(r'\.(png|jpe?g|webp|gif)$', u):
        return url
    for dom in ('play-lh.googleusercontent.com', 'encrypted-tbn0.gstatic.com',
                'lh3.googleusercontent.com', 'yt3.ggpht.com'):
        if dom in u:
            return url
    return ''


def _sz6_parse_start(st):
    """'YYYY/MM/DD HH:MM:SS +ZZZZ' (UTC) -> (sort_key, local '%d/%m %H:%M').
    Ritorna (None, '') se non parsabile."""
    try:
        m = re.match(r'^(\d{4})/(\d{2})/(\d{2})[ T](\d{2}):(\d{2}):(\d{2})\s*([+-]\d{4})?$', (st or '').strip())
        if not m:
            return None, ''
        y, mo, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
        h, mi, se = int(m.group(4)), int(m.group(5)), int(m.group(6))
        dt = datetime(y, mo, dd, h, mi, se, tzinfo=timezone.utc)
        local = dt.astimezone()
        return dt.timestamp(), local.strftime('%d/%m %H:%M')
    except Exception:
        return None, ''


def sz6_view():
    back_button(BASE + '?action=events')
    xbmcplugin.setContent(HANDLE, 'videos')
    events = _sz6_events()
    li = xbmcgui.ListItem(label=lbl('Aggiorna eventi'))
    li.setInfo('video', {'title': 'Aggiorna eventi', 'plot': 'Ricarica gli eventi SportzX dal mirror'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sz6_refresh'), li, isFolder=True)
    if not events:
        li = xbmcgui.ListItem(label=lbl('Nessun evento (mirror non raggiungibile)'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    sortable = []
    for ev in events:
        ei = ev.get('eventInfo') or {}
        ts, tstr = _sz6_parse_start(ei.get('startTime') or '')
        if ts is None:
            ts = float('inf')
        sortable.append((ts, ev, tstr))
    sortable.sort(key=lambda x: (x[0], (x[1].get('title') or '').lower()))
    for ts, ev, time_str in sortable:
        eid = str(ev.get('id') or '')
        title = ev.get('title') or ''
        cat = ev.get('cat') or ''
        ei = ev.get('eventInfo') or {}
        label = ('%s  [%s - %s]' % (title, time_str, cat)) if time_str else ('%s  [%s]' % (title, cat))
        li = xbmcgui.ListItem(label=lbl(label))
        thumb = _sz6_thumb(ei.get('teamAFlag') or ei.get('teamBFlag') or '')
        if thumb:
            li.setArt({'thumb': thumb})
        li.setInfo('video', {'title': title, 'plot': '%s%s' % (cat, ('  %s' % time_str) if time_str else '')})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sz6_ev', e=eid), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sz6_refresh():
    _sz6_events(force=True)
    xbmc.executebuiltin('Container.Refresh()')


def sz6_ev_view(e):
    back_button(BASE + '?action=sz6')
    xbmcplugin.setContent(HANDLE, 'videos')
    chs = _sz6_ordered(_sz6_channels(e))
    if not chs:
        li = xbmcgui.ListItem(label=lbl('Nessun flusso per questo evento'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sz6', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for idx, ch in enumerate(chs):
        try:
            t = int(ch.get('type') or '0')
        except Exception:
            t = 0
        title = ch.get('title') or ('Canale %d' % idx)
        if t == 1:
            title += '  (MPD)'
        li = xbmcgui.ListItem(label=lbl(title))
        thumb = _sz6_thumb(ch.get('logo') or '')
        if thumb:
            li.setArt({'thumb': thumb})
        li.setProperty('isPlayable', 'true')
        li.setInfo('video', {'title': title})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sz6_play', e=e, i=str(idx)), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def _resolve_channel_list(chs, idx, name):
    try:
        ch = chs[int(idx)]
    except Exception:
        notify(name, 'Canale non disponibile', True)
        return xbmcgui.ListItem()
    link = ch.get('link') or ''
    if not link:
        notify(name, 'Nessun link per questo canale', True)
        return xbmcgui.ListItem()
    url = link
    hdrstr = ''
    if '|' in link:
        url, _, hdrstr = link.partition('|')
    hdrs = ''
    if hdrstr:
        parts = []
        for kv in hdrstr.split('&'):
            k, _, v = kv.partition('=')
            if not k:
                continue
            k = '-'.join(p.capitalize() for p in k.replace('_', '-').split('-'))
            parts.append(k + '=' + v)
        hdrs = '&'.join(parts)
    is_mpd = str(ch.get('type', '0')) == '1' or url.lower().endswith('.mpd')
    li = xbmcgui.ListItem(path=url, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'mpd' if is_mpd else 'hls')
    api = ch.get('api') or ''
    if api:
        li.setProperty('inputstream.adaptive.drm_legacy', 'org.w3.clearkey|' + api)
    if hdrs:
        li.setProperty('inputstream.adaptive.stream_headers', hdrs)
        li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
        if not is_mpd:
            li.setProperty('inputstream.adaptive.license_key', '|' + hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    if ADDON.getSetting('live_async') == 'true':
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    if ADDON.getSetting('manifest_upd') == 'true':
        li.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    return li


def play_sz6(e, i):
    li = _resolve_channel_list(_sz6_ordered(_sz6_channels(e)), i, 'Eventi 6 (SportzX)')
    xbmcplugin.setResolvedUrl(HANDLE, True, li)


def events_view():
    home_button()
    li = xbmcgui.ListItem(label=lbl('Eventi 1'))
    li.setArt({'thumb': LOGO_BASE + 'eventi_icon.png'})
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=eventi1', li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 2 (AK47 Sports)'))
    li.setArt({'thumb': LOGO_BASE + 'sportzx.png'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sportzx'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 3 (Daddy)'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 4 (HTSport)'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('htsport'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 5 (Canali Sport)'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sports'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 6 (SportzX)'))
    li.setArt({'thumb': LOGO_BASE + 'sportzx.png'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sz6'), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def _daddy_fetch():
    if _DDY['data'] is None or (time.time() - _DDY['ts']) >= _DDY_TTL:
        last = None
        for attempt in range(2):
            try:
                r = requests.get('https://test34344.herokuapp.com/filter.php',
                                 params={'numTest': 'A1A114'},
                                 headers={'User-Agent': API_UA}, timeout=25)
                r.raise_for_status()
                _DDY['data'] = r.json().get('channels', [])
                _DDY['ts'] = time.time()
                break
            except Exception as e:
                last = e
                time.sleep(1)
        if _DDY['data'] is None:
            log('daddy fetch: %s' % last)
            _DDY['data'] = []
            _DDY['ts'] = time.time()
    return _DDY['data']


def daddy_view():
    back_button(BASE + '?action=events')
    cats = _daddy_fetch()
    if not cats:
        li = xbmcgui.ListItem(label=lbl('Nessuna categoria'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for idx, c in enumerate(cats):
        title = strip_color(c.get('name') or '')
        if not title:
            continue
        li = xbmcgui.ListItem(label=lbl(title))
        thumb = c.get('thumbnail') or ''
        if isinstance(thumb, str) and thumb.startswith('http'):
            li.setArt({'thumb': thumb})
        n = len(c.get('items') or [])
        li.setInfo('video', {'title': title, 'plot': ('%d eventi' % n) if n else 'Nessun evento'})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy_cat', i=str(idx)), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def daddy_cat_view(i):
    back_button(BASE + '?action=ddy')
    cats = _daddy_fetch()
    try:
        cat = cats[int(i)]
    except Exception:
        cat = None
    items = (cat or {}).get('items') or []
    if not items:
        li = xbmcgui.ListItem(label=lbl('Nessun canale'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=ddy', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for it in items:
        title = strip_color(it.get('title') or '')
        mr = it.get('myresolve') or ''
        code = mr.split('@@', 1)[1] if '@@' in mr else ''
        if not title or not code:
            continue
        li = xbmcgui.ListItem(label=lbl(title))
        li.setInfo('video', {'title': title, 'plot': it.get('info') or ''})
        li.setProperty('isPlayable', 'true')
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy_play', c=code), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def resolve_daddy(code):
    try:
        hdrs0 = {'user-agent': 'Mozilla/5.0', 'accept': '*/*', 'Referer': 'https://dlhd.st/'}
        page1 = requests.get('https://dlhd.st/stream/stream-%s.php' % code,
                             headers=hdrs0, timeout=25).text
        m = re.search(r'<iframe src="(.*?)"', page1)
        if not m:
            raise ValueError('iframe non trovato')
        dadUrl = m.group(1)
        page2 = requests.get(dadUrl, headers=hdrs0, timeout=25).text
        m2 = re.search(r"window\.atob\('(.*?)'\)", page2)
        if not m2:
            raise ValueError('token non trovato')
        link = base64.b64decode(m2.group(1)).decode('utf-8', 'replace')
        arr = dadUrl.split('/')
        refe = arr[0] + '//' + arr[2] + '/'
        origin = arr[0] + '//' + arr[2]
        hdrs = 'Referer=%s&Origin=%s&User-Agent=%s' % (refe, origin, UA)
    except Exception as e:
        log('daddy resolve %s: %s' % (code, e))
        notify('Eventi 3', 'Errore risoluzione link', True)
        return xbmcgui.ListItem()
    li = xbmcgui.ListItem(path=link, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    is_mpd = '.mpd' in link.lower()
    li.setProperty('inputstream.adaptive.manifest_type', 'mpd' if is_mpd else 'hls')
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    if not is_mpd:
        li.setProperty('inputstream.adaptive.license_key', '|' + hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    if ADDON.getSetting('live_async') == 'true':
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    if ADDON.getSetting('manifest_upd') == 'true':
        li.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    return li


def _ht_clean(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def _ht_fetch(force=False):
    if not force and _HT['data'] is not None and (time.time() - _HT['ts']) < HTSPORT_TTL:
        return _HT['data']
    days = []
    try:
        r = requests.get(HTSPORT_INDEX, timeout=25, headers={'User-Agent': UA})
        r.raise_for_status()
        text = r.text
        day_re = re.compile(r'<div class="date-header"><span[^>]*>(.*?)</span>\s*(.*?)</div>', re.S)
        lab_re = re.compile(r'<span class="category-label">(.*?)</span>', re.S)
        card_re = re.compile(r'<div class="match-card\b.*?</div>\s*</div>', re.S)
        tokens = []
        for m in day_re.finditer(text):
            tokens.append((m.start(), 'day', m))
        for m in lab_re.finditer(text):
            tokens.append((m.start(), 'lab', m))
        for m in card_re.finditer(text):
            tokens.append((m.start(), 'card', m))
        tokens.sort(key=lambda x: x[0])
        cur_day = None
        cur_comp = None
        for _pos, kind, m in tokens:
            if kind == 'day':
                name = _ht_clean(m.group(1))
                date = _ht_clean(m.group(2))
                cur_day = {'label': (name + ' ' + date).strip(), 'comps': []}
                cur_comp = None
                days.append(cur_day)
            elif kind == 'lab':
                if cur_day is None:
                    continue
                cur_comp = _ht_clean(m.group(1))
                cur_day['comps'].append({'comp': cur_comp, 'matches': []})
            elif kind == 'card':
                if cur_day is None or cur_comp is None or not cur_day['comps']:
                    continue
                content = m.group(0)
                tm = re.search(r'<strong>([^<]+)</strong>', content)
                mtime = _ht_clean(tm.group(1)) if tm else ''
                tbox = re.search(r'class="teams-box"[^>]*>(.*?)</div>', content, re.S)
                teams = re.sub(r'<[^>]+>', '', tbox.group(1)).strip() if tbox else ''
                teams = html.unescape(teams).strip()
                chs = []
                for a in re.finditer(r'<a href="([^"]+)"[^>]*class="btn[^"]*"[^>]*>(.*?)</a>', content, re.S):
                    href = a.group(1)
                    name = _ht_clean(a.group(2))
                    if href and name:
                        chs.append({'name': name, 'page': href})
                cur_day['comps'][-1]['matches'].append(
                    {'time': mtime, 'teams': teams, 'channels': chs})
        days = [d for d in days if d['comps']]
    except Exception as e:
        log('htsport fetch: %s' % e)
        days = []
    _HT['data'] = days
    _HT['ts'] = time.time()
    return days


def _ht_decode_obf(page):
    m = re.search(r'var ([A-Za-z0-9_]+)=\[([0-9,]+)\],([A-Za-z0-9_]+)=(\d+),([A-Za-z0-9_]+)=(\d+),[A-Za-z0-9_]+=""', page)
    if not m:
        return ''
    try:
        nums = [int(x) for x in m.group(2).split(',')]
        k1 = int(m.group(4))
        k2 = int(m.group(6))
        out = ''
        for v in nums:
            out += chr(((v ^ k1) - k2 + 256) % 256)
        m3 = re.search(r'https?://[^\s"\\]+\.m3u8', out)
        return m3.group(0) if m3 else ''
    except Exception:
        return ''


def resolve_htsport(page):
    now = time.time()
    if page in _HT_RES['data'] and (now - _HT_RES['ts'].get(page, 0)) < _HT_RES_TTL:
        return _HT_RES['data'][page]
    url = ''
    try:
        page_url = urllib.parse.urljoin(HTSPORT_BASE, page) if not page.startswith('http') else page
        p = requests.get(page_url, timeout=25, headers={'User-Agent': UA})
        p.raise_for_status()
        m = re.search(r'<iframe[^>]+src="([^"]+)"', p.text)
        if m:
            fr = m.group(1)
            po = requests.get(fr, timeout=25, headers={'User-Agent': UA, 'Referer': HTSPORT_BASE + '/'})
            po.raise_for_status()
            url = _ht_decode_obf(po.text)
    except Exception as e:
        log('htsport resolve %s: %s' % (page, e))
        url = ''
    _HT_RES['data'][page] = url
    _HT_RES['ts'][page] = now
    return url


def htsport_view():
    back_button(BASE + '?action=events')
    days = _ht_fetch()
    if not days:
        li = xbmcgui.ListItem(label=lbl('Nessuna lista eventi (sito non raggiungibile)'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    li = xbmcgui.ListItem(label=lbl('Aggiorna eventi'))
    li.setInfo('video', {'title': 'Aggiorna eventi', 'plot': 'Scarica di nuovo gli eventi dal sito'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('htsport_refresh'), li, isFolder=True)
    for di, d in enumerate(days):
        n = sum(len(c['matches']) for c in d['comps'])
        li = xbmcgui.ListItem(label=lbl(d['label']))
        li.setInfo('video', {'title': d['label'], 'plot': '%d eventi' % n})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('htsport_day', di=str(di)), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def htsport_refresh():
    _ht_fetch(force=True)
    xbmc.executebuiltin('Container.Refresh()')


def htsport_day_view(di):
    back_button(BASE + '?action=htsport')
    days = _ht_fetch()
    try:
        day = days[int(di)]
    except Exception:
        days = _ht_fetch(force=True)
        try:
            day = days[int(di)]
        except Exception:
            day = None
    if not day:
        li = xbmcgui.ListItem(label=lbl('Lista eventi non disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=htsport', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for ci, c in enumerate(day['comps']):
        title = c['comp']
        n = len(c['matches'])
        li = xbmcgui.ListItem(label=lbl(title))
        li.setInfo('video', {'title': title, 'plot': '%d eventi' % n})
        url = _tmdb_url('htsport_comp', di=str(di), ci=str(ci))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def htsport_comp_view(di, ci):
    back_button(BASE + '?action=htsport_day&di=' + str(di))
    days = _ht_fetch()
    try:
        comp = days[int(di)]['comps'][int(ci)]
    except Exception:
        comp = None
    if not comp:
        li = xbmcgui.ListItem(label=lbl('Nessun evento disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=htsport_day&di=' + str(di), li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for mi, mt in enumerate(comp['matches']):
        nch = len(mt['channels'])
        label = ('[%s]  %s' % (mt['time'], mt['teams'])) if mt['time'] else mt['teams']
        plot = mt['teams']
        if nch:
            plot += ' | Canali: ' + ', '.join(c['name'] for c in mt['channels'])
        li = xbmcgui.ListItem(label=lbl(label))
        li.setInfo('video', {'title': mt['teams'], 'plot': plot})
        url = _tmdb_url('htsport_match', di=str(di), ci=str(ci), mi=str(mi))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def htsport_match_view(di, ci, mi):
    back_button(BASE + '?action=htsport_comp&di=' + str(di) + '&ci=' + str(ci))
    xbmcplugin.setContent(HANDLE, 'videos')
    days = _ht_fetch()
    try:
        match = days[int(di)]['comps'][int(ci)]['matches'][int(mi)]
    except Exception:
        match = None
    if not match or not match['channels']:
        li = xbmcgui.ListItem(label=lbl('Nessun canale disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=htsport_comp&di=' + str(di) + '&ci=' + str(ci), li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    title = match['teams']
    if match['time']:
        title = '%s  [%s]' % (match['teams'], match['time'])
    for ch in match['channels']:
        name = ch['name'] or 'Canale'
        li = xbmcgui.ListItem(label=lbl(name))
        li.setInfo('video', {'title': name, 'plot': title})
        li.setProperty('isPlayable', 'true')
        url = _tmdb_url('htsport_play', page=ch['page'])
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def play_htsport(page):
    url = resolve_htsport(page)
    if not url:
        notify('HTSport', 'Risoluzione link non riuscita', True)
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return
    li = xbmcgui.ListItem(path=url, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'hls')
    try:
        host = 'https://' + url.split('/')[2]
    except Exception:
        host = url
    hdrs = 'User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (UA, host, host)
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    if ADDON.getSetting('live_async') == 'true':
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    if ADDON.getSetting('manifest_upd') == 'true':
        li.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    li.setProperty('inputstream.adaptive.license_key', '|User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (UA, host, host))
    xbmcplugin.setResolvedUrl(HANDLE, True, li)


def _sports_fetch(force=False):
    if not force and _SPORTS['data'] is not None and (time.time() - _SPORTS['ts']) < SPORTS_TTL:
        return _SPORTS['data']
    chans = []
    try:
        r = requests.get(SPORTS_PLAYLIST_URL, timeout=30, headers={'User-Agent': UA})
        r.raise_for_status()
        name = None
        for ln in r.text.splitlines():
            ln = ln.strip()
            if ln.startswith('#EXTINF'):
                if 'group-title' in ln:
                    m = ln.rsplit('",', 1)
                    name = m[-1].strip() if len(m) == 2 else ln.split(',', 1)[-1].strip()
                else:
                    name = ln.split(',', 1)[-1].strip()
                name = re.sub(r'[\[\]\(\)]', '', name).strip()
            elif ln.startswith('http') and name:
                chans.append({'name': name, 'url': ln})
                name = None
    except Exception as e:
        log('sports fetch: %s' % e)
        chans = []
    _SPORTS['data'] = chans
    _SPORTS['ts'] = time.time()
    return chans


def sports_view():
    back_button(BASE + '?action=events')
    chans = _sports_fetch()
    if not chans:
        li = xbmcgui.ListItem(label=lbl('Nessun canale (playlist non raggiungibile)'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    li = xbmcgui.ListItem(label=lbl('Aggiorna canali'))
    li.setInfo('video', {'title': 'Aggiorna canali', 'plot': 'Scarica di nuovo la playlist dei canali'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sports_refresh'), li, isFolder=True)
    xbmcplugin.setContent(HANDLE, 'videos')
    for ch in sorted(chans, key=lambda c: c['name'].lower()):
        title = ch['name'] or 'Canale'
        li = xbmcgui.ListItem(label=lbl(title))
        li.setInfo('video', {'title': title, 'plot': 'Canale sportivo'})
        li.setProperty('isPlayable', 'true')
        url = _tmdb_url('sports_play', u=ch['url'])
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sports_refresh():
    _sports_fetch(force=True)
    xbmc.executebuiltin('Container.Refresh()')


def play_sports(u):
    url = u or ''
    if not url:
        notify('Canali Sport', 'Nessun flusso disponibile', True)
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return
    li = xbmcgui.ListItem(path=url, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'hls')
    try:
        host = ('https://' if not url.startswith('http://') else 'http://') + url.split('/')[2]
    except Exception:
        host = url
    hdrs = 'User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (UA, host, host)
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    if ADDON.getSetting('buffer_enabled') == 'true':
        li.setProperty('inputstream.adaptive.buffer_size', ADDON.getSetting('buffer_size') + 'MiB')
    if ADDON.getSetting('live_async') == 'true':
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    if ADDON.getSetting('manifest_upd') == 'true':
        li.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    li.setProperty('inputstream.adaptive.license_key', '|User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (UA, host, host))
    xbmcplugin.setResolvedUrl(HANDLE, True, li)


def sportzx_view():
    # AK47 Sports - MPD giornalieri (ex SportzX)
    back_button(BASE + '?action=events')
    li = xbmcgui.ListItem(label=lbl('Eventi live MPD'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ak47_events'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('AK47 TV (MPD)'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ak47_cats'), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def ak47_events_view():
    back_button(BASE + '?action=sportzx')
    xbmcplugin.setContent(HANDLE, 'videos')
    from collections import defaultdict
    nations = defaultdict(list)
    for ch in _AK47_MPD:
        nations[ch['nation']].append(ch)
    for nation in sorted(nations):
        cnt = len(nations[nation])
        flag = _FLAGS.get(nation, LOGO_BASE + 'skyhd.png')
        li = xbmcgui.ListItem(label=lbl('%s (%d) [MPD]' % (nation, cnt)))
        li.setArt({'thumb': flag, 'icon': flag})
        li.setInfo('video', {'title': nation, 'plot': ''})
        url = BASE + '?action=ak47_nation&nation=' + urllib.parse.quote(nation)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def ak47_nation_view(nation):
    back_button(BASE + '?action=ak47_events')
    xbmcplugin.setContent(HANDLE, 'videos')
    for ch in [c for c in _AK47_MPD if c['nation'] == nation]:
        mpd = ch['mpd']
        keys = ch.get('keys') or ''
        li = xbmcgui.ListItem(label=lbl(ch['title']), path=mpd)
        flag = _FLAGS.get(nation, LOGO_BASE + 'skyhd.png')
        li.setArt({'thumb': flag})
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
        try:
            host = 'https://' + mpd.split('/')[2]
        except:
            host = mpd
        hdrs = 'User-Agent=%s&Referer=%s/&Origin=%s&verifypeer=false' % (UA, host, host)
        li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
        li.setProperty('inputstream.adaptive.stream_headers', hdrs)
        if keys:
            li.setProperty('inputstream.adaptive.license_type', 'org.w3.clearkey')
            li.setProperty('inputstream.adaptive.license_key', keys)
            li.setProperty('inputstream.adaptive.drm_legacy', 'org.w3.clearkey|' + keys)
        li.setInfo('video', {'title': ch['title'], 'plot': ''})
        xbmcplugin.addDirectoryItem(HANDLE, mpd, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def ak47_cats_view():
    back_button(BASE + '?action=sportzx')
    ak47_events_view()


def sportzx_events_view():
    back_button(BASE + '?action=sportzx')
    evs = _szx_load('events', 'events.json')
    if not evs:
        li = xbmcgui.ListItem(label=lbl('Nessun evento live'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sportzx', li, isFolder=False)
        li = xbmcgui.ListItem(label=lbl('Se gli eventi non compaiono: imposta la password SportzX nelle Impostazioni'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sportzx', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for ev in evs:
        title = ev.get('title') or ''
        if not title:
            continue
        info = ev.get('eventInfo') or {}
        label = '[COLOR snow]%s[/COLOR]' % title
        stime = info.get('startTime', '') or ''
        ds = stime.split(' ')[0].split('/')
        if len(ds) == 3:
            label += '   [COLOR %s]%s%s%s[/COLOR]' % (EXP_OK_COLOR, ds[2], ds[1], ds[0])
        li = xbmcgui.ListItem(label=label)
        plot = title
        if info.get('teamA') or info.get('teamB'):
            plot = '%s vs %s' % (info.get('teamA', ''), info.get('teamB', ''))
        if info.get('eventName'):
            plot += ' | ' + str(info['eventName'])
        if stime:
            plot += ' | Inizio ' + stime
        li.setInfo('video', {'title': title, 'plot': plot})
        li.setProperty('isPlayable', 'false')
        url = _tmdb_url('szx_event', id=str(ev.get('id', '')))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sportzx_event_view(eid, back=''):
    back_button(back or (BASE + '?action=szx_events'))
    chs = _szx_channels(eid)
    if not chs:
        li = xbmcgui.ListItem(label=lbl('Nessun canale disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=szx_events', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for idx, ch in enumerate(chs):
        title = (ch.get('title') or ('Canale %d' % (idx + 1))).strip()
        li = xbmcgui.ListItem(label=lbl(title))
        li.setInfo('video', {'title': title})
        li.setProperty('isPlayable', 'true')
        url = _tmdb_url('szx_play', id=eid, i=str(idx))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sportzx_cat_view():
    back_button(BASE + '?action=sportzx')
    cats = _szx_load('cats', 'cats.json')
    added = 0
    for c in cats:
        title = c.get('title') or ''
        link = c.get('catLink') or ''
        if not isinstance(link, str) or not link.startswith('http'):
            continue
        li = xbmcgui.ListItem(label=lbl(title))
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('szx_catplay', link=link), li, isFolder=True)
        added += 1
    if not added:
        li = xbmcgui.ListItem(label=lbl('Nessuna categoria disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sportzx', li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sportzx_catplay_view(link=''):
    back_button(BASE + '?action=szx_cats')
    try:
        r = requests.get(link, timeout=20, headers={'User-Agent': UA})
        r.raise_for_status()
        text = r.text
    except Exception as e:
        log('sportzx cat playlist: %s' % e)
        li = xbmcgui.ListItem(label=lbl('Playlist non disponibile'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=szx_cats', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for ch in parse_m3u(text):
        li = xbmcgui.ListItem(label=lbl(ch['label']), path=ch['url'])
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        for k, v in ch['props'].items():
            if k == 'inputstream' and not v:
                continue
            li.setProperty(k, v)
        xbmcplugin.addDirectoryItem(HANDLE, ch['url'], li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def _szx_channels(eid):
    if eid not in _SZX['channels']:
        _SZX['channels'][eid] = _szx_load(eid, 'channels/%s.json' % eid)
    return _SZX['channels'][eid]


def resolve_sportzx(eid, idx):
    return _resolve_channel_list(_szx_channels(eid), idx, 'Sportzx')


def guida_view():
    home_button()
    xbmcplugin.setContent(HANDLE, 'videos')
    for name, cid, flag, broad in _GUIDA:
        li = xbmcgui.ListItem(label=lbl(name))
        li.setArt({'thumb': LOGO_BASE + 'tv_icon.png'})
        li.setInfo('video', {'title': name, 'plot': ''})
        li.setProperty('IsPlayable', 'false')
        url = BASE + '?action=guidacomp&comp=' + urllib.parse.quote(cid) + '&name=' + urllib.parse.quote(name)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def guida_comp_view(comp, name=''):
    back_button(BASE + '?action=guida')
    xbmcplugin.setContent(HANDLE, 'videos')

    # Mappa comp -> DaddyLive categoria
    comp_to_daddy = {
        'italy/serie-a': 'Serie A',
        'italy/serie-b': 'Serie B',
        'italy/coppa-italia': None,
        'england/premier-league': 'Premier League',
        'spain/primera-division': 'LaLiga',
        'germany/bundesliga': 'Bundesliga',
        'france/ligue-1': 'Ligue 1',
        'international/uefa-champions-league': None,
        'international/uefa-europa-league': None,
    }

    # estrai nome competizione per filtro
    filter_kw = None
    for k, v in comp_to_daddy.items():
        if comp == k:
            filter_kw = v
            break

    # raccogli eventi da DaddyLive
    events = {}
    try:
        cats = _daddy_fetch()
        for cat in cats:
            cat_name = strip_color(cat.get('name','') or '')
            for it in cat.get('items', []):
                raw = it.get('title') or ''
                title = strip_color(raw)
                if not title:
                    continue
                # filtra solo Serie A se richiesta Serie A
                if filter_kw and ('%s :' % filter_kw) not in title:
                    continue
                # estrai orario + partita + canale
                m = re.match(r'^(\d+\w*\s+\w+\s+\d{4})\s+(\d{2}:\d{2})\s+(.+?)\s+([A-Za-z0-9 .\'&\-/]+?)$', title)
                if m:
                    date_str, time_str, match_name, channel = m.group(1), m.group(2), m.group(3).strip(), m.group(4).strip()
                    match_key = '%s %s' % (time_str, match_name)
                    if match_key not in events:
                        events[match_key] = {'date': date_str, 'time': time_str, 'name': match_name, 'channels': set()}
                    if channel.lower() != 'backup stream':
                        events[match_key]['channels'].add(channel)

    except Exception as e:
        log('guida daddy fetch: %s' % e)

    if not events:
        li = xbmcgui.ListItem(label=lbl('Nessun evento trovato'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=guida', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return

    # ordina per orario
    sorted_events = sorted(events.items(), key=lambda x: x[0])

    for key, ev in sorted_events:
        # header partita
        label = '[COLOR snow]%s[/COLOR] [COLOR FF99CC33]%s[/COLOR]' % (ev['time'], ev['name'])
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': LOGO_BASE + 'skyhd.png'})
        li.setProperty('IsPlayable', 'false')
        li.setInfo('video', {'title': ev['name'], 'plot': ''})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=guida', li, isFolder=False)

        # canali ordinati alfabeticamente
        chs = sorted(ev['channels'])
        for i, ch in enumerate(chs):
            prefix = '\u2514\u2500 ' if i == len(chs)-1 else '\u251c\u2500 '
            li_c = xbmcgui.ListItem(label=lbl('%s %s' % (prefix, ch)))
            li_c.setArt({'thumb': LOGO_BASE + 'tv_icon.png'})
            li_c.setProperty('IsPlayable', 'false')
            li_c.setInfo('video', {'title': ch, 'plot': ''})
            xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=guida', li_c, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE)


def html_unescape(s):
    try:
        import html as _h
        return _h.unescape(s)
    except Exception:
        return s


def empty_item():
    li = xbmcgui.ListItem(label=' ')
    li.setArt({'thumb': EMPTY_LOGO, 'icon': EMPTY_LOGO})
    xbmcplugin.addDirectoryItem(HANDLE, BASE, li, isFolder=False)


def _ver_tuple(s):
    return tuple(int(x) for x in re.findall(r'\d+', s) or ['0'])


def check_update():
    try:
        headers = {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
        r = requests.get(REPO_BASE + '/addons.xml?_=' + str(int(time.time())), headers=headers, timeout=15)
        r.raise_for_status()
        m = re.search(r'<addon id="plugin\.video\.kodiakso" name="PZ8" version="([^"]+)"', r.text)
        if not m:
            m = re.search(r'<addon id="plugin\.video\.kodiakso" version="([^"]+)"', r.text)
        if not m:
            raise Exception('versione non trovata')
        new = m.group(1)
        cur = ADDON.getAddonInfo('version')
        if _ver_tuple(new) <= _ver_tuple(cur):
            notify(NAME, 'Aggiornato: sei gia alla v' + cur)
            return
        z = requests.get(REPO_BASE + '/zips/plugin.video.kodiakso/plugin.video.kodiakso-' + new + '.zip?_=' + str(int(time.time())), headers=headers, timeout=120)
        z.raise_for_status()
        data = zipfile.ZipFile(io.BytesIO(z.content))
        dest = ADDON.getAddonInfo('path')
        count = 0
        for name in data.namelist():
            rel = name[len('plugin.video.kodiakso/'):] if name.startswith('plugin.video.kodiakso/') else name
            if not rel or not name.startswith('plugin.video.kodiakso/') or rel.endswith('/'):
                continue
            target = os.path.normpath(os.path.join(dest, rel.replace('/', os.sep)))
            if not target.startswith(os.path.normpath(dest)):
                continue
            d = os.path.dirname(target)
            if not os.path.isdir(d):
                try:
                    os.makedirs(d)
                except Exception:
                    continue
            tmp = target + '.tmp'
            try:
                with open(tmp, 'wb') as f:
                    f.write(data.read(name))
                try:
                    os.replace(tmp, target)
                except Exception:
                    if os.path.exists(target):
                        try:
                            os.remove(target)
                        except Exception:
                            try:
                                os.rename(target, target + '.' + str(int(time.time())) + '.old')
                            except Exception:
                                pass
                    os.replace(tmp, target)
                count += 1
            except Exception as e:
                xbmc.log('KODIAKSO update file ERR (' + rel + '): ' + str(e), xbmc.LOGERROR)
        xbmc.executebuiltin('UpdateLocalAddons')
        notify(NAME, 'Aggiornato alla v' + new + ' (file aggiornati: ' + str(count) + ')')
    except Exception as e:
        xbmc.log('KODIAKSO update ERR: ' + str(e), xbmc.LOGERROR)
        notify(NAME, 'Impossibile controllare gli aggiornamenti', True)


def update_view():
    # Fix Backspace -> old version (1.10.70) visual bug: don't push history, refresh in place without cache
    check_update()
    # UpdateLocalAddons already called in check_update(); force refresh of current container
    # Use Refresh (re-executes root without pushing) + cacheToDisc=False to avoid cached old ListItems
    try:
        xbmc.sleep(400)
    except Exception:
        pass
    xbmc.executebuiltin('Container.Refresh')
    xbmc.executebuiltin('Container.Update("%s?action=root",replace)' % BASE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def root_view():
    bann = xbmcgui.ListItem(label='[B][COLOR snow]PZ8[/COLOR][/B]')
    bann.setArt({'banner': BANNER_LOGO, 'clearlogo': BANNER_LOGO, 'icon': ICON_LOGO, 'thumb': ''})
    bann.setInfo('video', {'title': 'PZ8', 'plot': 'SPORT \u2219 TV \u2219 VOD'})
    bann.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(HANDLE, BASE, bann, isFolder=True)

    li = xbmcgui.ListItem(label=lbl('Ricerca globale'))
    li.setArt({'thumb': SEARCH_ICON})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('gsearch'), li, isFolder=True)

    empty_item()

    home_items = [
        ('GUIDA TV', LOGO_BASE + 'tv_icon.png', BASE + '?action=guida'),
        ('EVENTI', LOGO_BASE + 'eventi_icon.png', BASE + '?action=events'),
        ('SPORT', LOGO_BASE + 'skyhd.png', BASE + '?action=sky'),
        ('DAZN', LOGO_BASE + 'dazn.png', BASE + '?action=dazn'),
        ('TV', LOGO_BASE + 'tv_icon.png', BASE + '?action=tv'),
    ]
    if ADDON.getSetting('home_tmdb') != 'false':
        home_items.append(('VOD', LOGO_BASE + 'netflix.png', BASE + '?action=vod'))
    for label, icon, url in home_items:
        if label == 'VOD':
            empty_item()
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': icon or SQUARE_ICON})
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Aggiorna PZ8   v' + ADDON.getAddonInfo('version')))
    li.setArt({'thumb': ICON_LOGO})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('update'), li, isFolder=False)

    # --- Avvio Automatico (service.kodiakso.autostart) ---
    svc_id = 'service.kodiakso.autostart'
    has_svc = xbmc.getCondVisibility('System.HasAddon(%s)' % svc_id)
    if has_svc:
        try:
            svc_addon = xbmcaddon.Addon(svc_id)
            enabled = svc_addon.getSettingBool('enabled') if hasattr(svc_addon, 'getSettingBool') else svc_addon.getSetting('enabled') == 'true'
            delay = svc_addon.getSettingInt('delay') if hasattr(svc_addon, 'getSettingInt') else int(svc_addon.getSetting('delay') or '0')
        except Exception:
            enabled, delay = True, 2
        status = 'ON (%ds)' % delay if enabled else 'OFF'
        col = '00FF00' if enabled else 'FF0000'
        li = xbmcgui.ListItem(label=lbl('Avvio Automatico  [COLOR %s]%s[/COLOR]' % (col, status)))
        li.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('autostart'), li, isFolder=True)
    else:
        li = xbmcgui.ListItem(label=lbl('Avvio Automatico  [COLOR FF0000]non installato[/COLOR]'))
        li.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('autostart'), li, isFolder=True)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def autostart_view():
    svc_id = 'service.kodiakso.autostart'
    has_svc = xbmc.getCondVisibility('System.HasAddon(%s)' % svc_id)
    home_button()
    if not has_svc:
        li = xbmcgui.ListItem(label=lbl('[COLOR FF0000]Service non installato[/COLOR]'))
        li.setInfo('video', {'title': 'PZ8 Autostart non installato', 'plot': 'Installa il file service.kodiakso.autostart-1.0.1.zip da https://luishighnest.github.io/kodi/zips/plugin.video.kodiakso/ oppure da zips/service.kodiakso.autostart-1.0.1.zip. Dopo l\'installazione abilitalo qui.'})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)
        # bottone installazione guidata
        li2 = xbmcgui.ListItem(label=lbl('Installa PZ8 Autostart dal repository'))
        li2.setArt({'thumb': ICON_LOGO})
        # prova installazione da repo se disponibile
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=autostart_install', li2, isFolder=False)
        li3 = xbmcgui.ListItem(label=lbl('Apri Impostazioni Repository (installa da zip)'))
        li3.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=autostart_openrepo', li3, isFolder=False)
    else:
        try:
            svc_addon = xbmcaddon.Addon(svc_id)
            enabled = svc_addon.getSettingBool('enabled') if hasattr(svc_addon, 'getSettingBool') else svc_addon.getSetting('enabled') == 'true'
            delay = svc_addon.getSettingInt('delay') if hasattr(svc_addon, 'getSettingInt') else int(svc_addon.getSetting('delay') or '0')
        except Exception:
            enabled, delay = True, 2
        status = 'ATTIVO' if enabled else 'DISATTIVATO'
        col = '00FF00' if enabled else 'FF0000'
        li = xbmcgui.ListItem(label=lbl('Stato: [COLOR %s]%s[/COLOR]  (ritardo %ds)' % (col, status, delay)))
        li.setInfo('video', {'title': 'PZ8 Autostart', 'plot': 'Se ATTIVO, all\'avvio di Kodi apre automaticamente PZ8. Configura ritardo nelle impostazioni del service.'})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)

        tog = 'Disattiva avvio automatico' if enabled else 'Attiva avvio automatico'
        li2 = xbmcgui.ListItem(label=lbl('→ ' + tog))
        li2.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=autostart_toggle', li2, isFolder=False)

        li3 = xbmcgui.ListItem(label=lbl('→ Apri impostazioni PZ8 Autostart'))
        li3.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=autostart_settings', li3, isFolder=False)

        li4 = xbmcgui.ListItem(label=lbl('→ Test: apri subito PZ8 (RunAddon)'))
        li4.setArt({'thumb': ICON_LOGO})
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=autostart_test', li4, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE)


def autostart_toggle():
    svc_id = 'service.kodiakso.autostart'
    try:
        svc_addon = xbmcaddon.Addon(svc_id)
        cur = svc_addon.getSettingBool('enabled') if hasattr(svc_addon, 'getSettingBool') else svc_addon.getSetting('enabled') == 'true'
        svc_addon.setSettingBool('enabled', not cur) if hasattr(svc_addon, 'setSettingBool') else svc_addon.setSetting('enabled', 'false' if cur else 'true')
        notify(NAME, 'Avvio automatico: ' + ('DISATTIVATO' if cur else 'ATTIVATO'))
    except Exception as e:
        notify(NAME, 'Errore toggle: ' + str(e), True)
    xbmc.executebuiltin('Container.Update("%s?action=autostart", replace)' % BASE)


def autostart_install():
    # prova installazione da repository luishighnest
    svc_id = 'service.kodiakso.autostart'
    if xbmc.getCondVisibility('System.HasAddon(%s)' % svc_id):
        notify(NAME, 'PZ8 Autostart già installato')
        xbmc.executebuiltin('Container.Update("%s?action=autostart", replace)' % BASE)
        return
    # se repo installato, InstallAddon funziona
    xbmc.executebuiltin('InstallAddon(%s)' % svc_id)
    # fallback: suggerisci zip
    xbmcgui.Dialog().ok(NAME, 'Se l\'installazione automatica non parte:\n\n1) Vai su Add-on → Installa da zip\n2) Scegli https://luishighnest.github.io/kodi/zips/plugin.video.kodiakso/service.kodiakso.autostart-1.0.1.zip\n\nOppure scarica lo zip e installalo manualmente.')
    xbmc.executebuiltin('Container.Update("%s?action=autostart", replace)' % BASE)


TEST_JSON_URL = REPO_BASE + '/test.json'
_TEST_CACHE = {'data': None, 'ts': 0}


def _test_fetch():
    now = time.time()
    if _TEST_CACHE['data'] is not None and (now - _TEST_CACHE['ts'] < 120):
        return _TEST_CACHE['data']
    headers = {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
    r = requests.get(TEST_JSON_URL + '?_=' + str(int(now)), headers=headers, timeout=15)
    r.raise_for_status()
    data = json.loads(r.content.decode('utf-8-sig'))
    _TEST_CACHE['data'] = data
    _TEST_CACHE['ts'] = now
    return data


def test_view(back=''):
    back_button(BASE + '?action=root')
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        data = _test_fetch()
    except Exception as e:
        log('test fetch ERR: %s' % e)
        li = xbmcgui.ListItem(label=lbl('Impossibile scaricare test.json'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for cat in data.keys():
        items = data[cat] or []
        li = xbmcgui.ListItem(label=lbl('%s (%d)' % (cat, len(items))))
        li.setArt({'thumb': LOGO_BASE + 'eventi_icon.png'})
        li.setInfo('video', {'title': cat, 'plot': '%d eventi' % len(items)})
        url = BASE + '?action=testcat&cat=' + urllib.parse.quote(cat)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def _test_is_vod(it):
    mpd = (it.get('mpd') or '')
    return any(x in mpd for x in ('/vod', '-vod', 'dcn-ac-vod', '/SFP/', '/DM/', '/BB/', 'highlightauto')) or ('channel=' not in mpd and '/live' not in mpd)


def _test_is_channel(it):
    name = (it.get('name') or '').lower()
    mpd = (it.get('mpd') or '')
    return ('dazn-linear' in mpd) or (name == 'dazn 1') or name.startswith('dazn ') and 'channel=' not in mpd and '/vod' not in mpd


def _test_sky_logo(it):
    """Ritorna il logo (URL) del canale Sky se l'MPD contiene nel percorso 'channel(<cid>)' (es. skysport24).

    Gestisce anche i wrapper glitch con url= percent-encoded. Ritorna '' se non è un canale Sky noto.
    """
    mpd = (it.get('mpd') or it.get('url') or '')
    if not mpd:
        return ''
    try:
        mpd_raw = urllib.parse.unquote(mpd)
    except Exception:
        mpd_raw = mpd
    m = re.search(r'channel\(([a-z0-9_]+)\)', mpd_raw, re.I)
    if not m:
        return ''
    cid = m.group(1).lower()
    logo = LOGOS.get(cid, '')
    return (LOGO_BASE + logo) if logo else ''


def _test_classified():
    """Ritorna (canali, eventi, vod): liste di (cat, idx, entry) dal JSON.

    Usa il campo 'type' dichiarato da dazn2 (100% affidabile); se assente, euristica sull'URL.
    Le voci della categoria EVENTI (aggiunte dal tasto 10 di dazn2) finiscono SEMPRE in Eventi 1.
    """
    canali, eventi, vod = [], [], []
    try:
        data = _test_fetch()
    except Exception as e:
        log('test fetch ERR: %s' % e)
        return canali, eventi, vod
    for cat, items in data.items():
        cat_is_eventi = (cat or '').strip().upper() == 'EVENTI'
        for idx, it in enumerate(items or []):
            if cat_is_eventi:
                eventi.append((cat, idx, it))
                continue
            t = (it.get('type') or '').lower()
            if t == 'vod':
                vod.append((cat, idx, it))
            elif t == 'canale' or _test_is_channel(it):
                canali.append((cat, idx, it))
            elif t == 'evento':
                eventi.append((cat, idx, it))
            elif _test_is_vod(it):
                vod.append((cat, idx, it))
            else:
                eventi.append((cat, idx, it))
    return canali, eventi, vod


def _test_add_playable(cat, idx, it):
    """Aggiunge una voce riproducibile del JSON (stesso funzionamento della sezione TEST)."""
    from datetime import datetime, timezone
    name = it.get('name') or ''
    t = (it.get('type') or '').lower()
    if t == 'canale' or _test_is_channel(it) or not it.get('start'):
        label = name
    else:
        # solo l'orario di inizio convertito in ora locale
        try:
            s = (it.get('start') or '').replace('Z', '+00:00')
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            label = '%s  %s' % (name, dt.astimezone().strftime('%H:%M'))
        except Exception:
            label = name
    li = xbmcgui.ListItem(label=lbl(label))
    sky_logo = _test_sky_logo(it)
    if sky_logo:
        li.setArt({'thumb': sky_logo, 'icon': sky_logo, 'poster': sky_logo})
    elif it.get('image'):
        li.setArt({'thumb': it['image']})
    li.setProperty('isPlayable', 'true')
    li.setInfo('video', {'title': name})
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=testplay&cat=' + urllib.parse.quote(cat) + '&idx=' + str(idx), li, isFolder=False)


def dazn_json_view():
    """Sezione DAZN della home: canali dal JSON + cartella VOD DAZN (stesso funzionamento della sezione TEST)."""
    home_button()
    xbmcplugin.setContent(HANDLE, 'videos')
    canali, _, vod = _test_classified()
    li = xbmcgui.ListItem(label=lbl('VOD DAZN'))
    li.setArt({'thumb': LOGO_BASE + 'dazn.png'})
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=voddazn', li, isFolder=True)
    if not canali:
        li = xbmcgui.ListItem(label=lbl('Nessun canale DAZN nel JSON'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)
    for cat, idx, it in canali:
        _test_add_playable(cat, idx, it)
    xbmcplugin.endOfDirectory(HANDLE)


def eventi1_json_view():
    """Eventi 1: eventi dal JSON direttamente riproducibili (stesso funzionamento della sezione TEST)."""
    back_button(BASE + '?action=events')
    xbmcplugin.setContent(HANDLE, 'videos')
    _, eventi, _ = _test_classified()
    if not eventi:
        li = xbmcgui.ListItem(label=lbl('Nessun evento nel JSON'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
    for cat, idx, it in eventi:
        _test_add_playable(cat, idx, it)
    xbmcplugin.endOfDirectory(HANDLE)


def vod_json_view():
    """VOD DAZN: vod dal JSON (stesso funzionamento della sezione TEST)."""
    back_button(BASE + '?action=events')
    xbmcplugin.setContent(HANDLE, 'videos')
    _, _, vod = _test_classified()
    if not vod:
        li = xbmcgui.ListItem(label=lbl('Nessun VOD nel JSON'))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=events', li, isFolder=False)
    for cat, idx, it in vod:
        _test_add_playable(cat, idx, it)
    xbmcplugin.endOfDirectory(HANDLE)


def test_cat_view(cat):
    back_button(BASE + '?action=test')
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        data = _test_fetch()
    except Exception as e:
        log('test fetch ERR: %s' % e)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for it in (data.get(cat) or []):
        name = it.get('name') or ''
        start = (it.get('start') or '').replace('T', ' ')[:16]
        end = (it.get('end') or '').replace('T', ' ')[:16]
        label = '%s  [%s - %s]' % (name, start, end) if start else name
        li = xbmcgui.ListItem(label=lbl(label))
        sky_logo = _test_sky_logo(it)
        if sky_logo:
            li.setArt({'thumb': sky_logo, 'icon': sky_logo, 'poster': sky_logo})
        elif it.get('image'):
            li.setArt({'thumb': it['image']})
        li.setProperty('isPlayable', 'true')
        li.setInfo('video', {'title': name})
        idx = (data.get(cat) or []).index(it)
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=testplay&cat=' + urllib.parse.quote(cat) + '&idx=' + str(idx), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def test_play(cat, idx):
    try:
        data = _test_fetch()
        it = (data.get(cat) or [])[int(idx)]
    except Exception as e:
        log('test play ERR: %s' % e)
        notify(NAME, 'Errore lettura evento TEST', True)
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return
    mpd = it.get('mpd') or ''
    key = it.get('key') or ''
    name = it.get('name') or 'TEST'
    # UA: usa quello salvato nell'evento (il token e' legato all'hash dell'UA di estrazione)
    ev_ua = (it.get('ua') or '').strip()
    ua_use = ev_ua or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0'
    # estrae il dazn-token dall'URL oppure dal campo dedicato (VOD: token solo negli header)
    m = re.search(r'[?&]dazn-token=([^&]+)', mpd)
    tok = urllib.parse.unquote(m.group(1)) if m else ''
    if not tok:
        tok = (it.get('dazn_token') or '').strip()
    hdrs = 'User-Agent=' + ua_use + '&Referer=https://www.dazn.com/&Origin=https://www.dazn.com&verifypeer=false'
    if tok:
        hdrs += '&dazn-token=' + urllib.parse.quote(tok, safe='')
    li = xbmcgui.ListItem(path=mpd, offscreen=True)
    li.setContentLookup(False)
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    if ':' in key:
        li.setProperty('inputstream.adaptive.drm_legacy', 'org.w3.clearkey|' + key)
    li.setProperty('inputstream.adaptive.stream_headers', hdrs)
    li.setProperty('inputstream.adaptive.manifest_headers', hdrs)
    # live_stream_type raw solo per i live (URL con channel=); per i VOD va omesso
    is_live = ('channel=' in mpd) or (it.get('end', '')[:4] >= '2999')
    if ADDON.getSetting('live_async') == 'true' and is_live:
        li.setProperty('inputstream.adaptive.live_stream_type', 'raw')
    bw = ADDON.getSetting('max_bandwidth').strip()
    if bw and bw != '0':
        li.setProperty('inputstream.adaptive.max_bandwidth', bw)
    li.setLabel(lbl(name))
    li.setInfo('video', {'title': name})
    xbmcplugin.setResolvedUrl(HANDLE, True, li)


def main():
    global _VOD_SRC
    query = urllib.parse.parse_qs(sys.argv[2][1:])
    _VOD_SRC = query.get('src', [''])[0]
    if 'action' in query:
        action = query['action'][0]
        if action == 'nav':
            url = query.get('url', [''])[0]
            if url:
                xbmc.executebuiltin('Container.Update("%s", replace)' % url)
                if HANDLE != -1:
                    xbmcplugin.endOfDirectory(HANDLE)
        elif action == 'root':
            root_view()
        elif action == 'guida':
            guida_view()
        elif action == 'guidacomp':
            guida_comp_view(query.get('comp', [''])[0], query.get('name', [''])[0])
        elif action == 'sky':
            sky_view()
        elif action == 'sky1':
            sky1_view(query.get('back', [''])[0])
        elif action == 'sky2':
            sky2_view(query.get('back', [''])[0])
        elif action == 'sky3':
            sky3_view(query.get('back', [''])[0])
        elif action == 'sky4':
            sky4_view(query.get('back', [''])[0])
        elif action == 'sky5':
            sky5_view(query.get('back', [''])[0])
        elif action == 'sky6':
            sky6_view(query.get('back', [''])[0])
        elif action == 'sky6nation':
            sky6_nation_view(query.get('nation', [''])[0], query.get('back', [''])[0])
        elif action == 'sky7':
            sky7_view(query.get('back', [''])[0])
        elif action == 'sky7list':
            sky7_list_view(query.get('idx', ['0'])[0], query.get('back', [''])[0])
        elif action == 'sky7cat':
            sky7_cat_view(query.get('idx', ['0'])[0], query.get('cat', [''])[0], query.get('back', [''])[0])
        elif action == 'calcioevent':
            calcio_event_view(query.get('url', [''])[0], query.get('t', [''])[0])
        elif action == 'sportplay':
            li = resolve_sportonline(query.get('url', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'sport':
            sky_view()
        elif action == 'vavooplay':
            li = resolve_vavoo(query.get('url', [''])[0], query.get('t', [''])[0], query.get('p', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'tv':
            tv_view()
        elif action == 'dazn':
            dazn_json_view()
        elif action == 'eventi1':
            eventi1_json_view()
        elif action == 'voddazn':
            vod_json_view()
        elif action == 'testcat':
            test_cat_view(query.get('cat', [''])[0])
        elif action == 'testplay':
            test_play(query.get('cat', [''])[0], query.get('idx', ['0'])[0])
        elif action == 'vod':
            vod_view()
        elif action == 'films':
            films_view()
        elif action == 'events':
            events_view()
        elif action == 'gsearch':
            gsearch_view(query.get('q', [''])[0])
        elif action == 'autostart':
            autostart_view()
        elif action == 'autostart_toggle':
            autostart_toggle()
        elif action == 'autostart_settings':
            xbmcaddon.Addon('service.kodiakso.autostart').openSettings()
            xbmc.executebuiltin('Container.Update("%s?action=autostart", replace)' % BASE)
        elif action == 'autostart_test':
            xbmc.executebuiltin('RunAddon(plugin.video.kodiakso)')
        elif action == 'autostart_install':
            autostart_install()
        elif action == 'autostart_openrepo':
            xbmc.executebuiltin('ActivateWindow(addonbrowser)')
        elif action == 'update':
            update_view()
        elif action == 'search':
            tmdb_search(query.get('q', [''])[0], int(query.get('page', ['1'])[0]),
                        query.get('back', [''])[0])
        elif action == 'cats':
            tmdb_cats(query.get('mt', ['movie'])[0], query.get('back', [''])[0])
        elif action == 'genres':
            tmdb_genres(query.get('mt', ['movie'])[0], query.get('back', [''])[0])
        elif action == 'list':
            q = query
            tmdb_list(q.get('mt', ['movie'])[0], q.get('kind', [''])[0],
                      q.get('genre', [''])[0], int(q.get('page', ['1'])[0]),
                      q.get('sort_by', [''])[0], q.get('year', [''])[0],
                      q.get('back', [''])[0])
        elif action == 'allsorts':
            tmdb_allsorts(query.get('mt', ['movie'])[0], query.get('back', [''])[0])
        elif action == 'decades':
            tmdb_decades(query.get('mt', ['movie'])[0], query.get('back', [''])[0])
        elif action == 'details':
            tmdb_details(query.get('mt', ['movie'])[0], query.get('id', [''])[0],
                         query.get('back', [''])[0])
        elif action == 'msearch':
            mandra_search_view(query.get('q', [''])[0], query.get('mt', [''])[0],
                               query.get('back', [''])[0])
        elif action == 'mplayauto':
            if _VOD_SRC == '2':
                notify(NAME, 'VOD 2: riproduzione non ancora disponibile')
                xbmcplugin.endOfDirectory(HANDLE)
            else:
                mandra_auto_movie(query.get('q', [''])[0])
        elif action == 'mseasonsauto':
            mandra_auto_series(query.get('q', [''])[0], query.get('back', [''])[0])
        elif action == 'mseason':
            mandra_season_view(query.get('code', [''])[0], query.get('back', [''])[0])
        elif action == 'mepisodes':
            mandra_episodes_view(query.get('par', [''])[0], query.get('back', [''])[0])
        elif action == 'mplay':
            if _VOD_SRC == '2':
                notify(NAME, 'VOD 2: riproduzione non ancora disponibile')
                xbmcplugin.endOfDirectory(HANDLE)
            else:
                li = resolve_scws(query.get('p', [''])[0], query.get('t', [''])[0],
                                  query.get('ept', [''])[0], query.get('s', [''])[0],
                                  query.get('e', [''])[0])
                xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'v2seasons':
            v2_seasons_view(query.get('id', [''])[0], query.get('back', [''])[0])
        elif action == 'v2episodes':
            v2_episodes_view(query.get('id', [''])[0], query.get('s', [''])[0],
                             query.get('back', [''])[0])
        elif action == 'v2play':
            li = resolve_v2(query.get('id', [''])[0], query.get('mtype', ['movie'])[0],
                            query.get('s', ['0'])[0], query.get('e', ['0'])[0],
                            query.get('t', [''])[0], query.get('ept', [''])[0])
            if li:
                xbmcplugin.setResolvedUrl(HANDLE, True, li)
            else:
                notify(NAME, 'Nessun flusso VixSrc disponibile', True)
                xbmcplugin.endOfDirectory(HANDLE)
        elif action == 'skycat':
            sky_cat_view(query.get('cat', [''])[0], query.get('back', [''])[0])
        elif action == 'skyplay':
            li = resolve_sky(query.get('id', [''])[0], query.get('t', [''])[0], query.get('p', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'sportzx':
            sportzx_view()
        elif action == 'ak47_events':
            ak47_events_view()
        elif action == 'ak47_nation':
            ak47_nation_view(query.get('nation', [''])[0])
        elif action == 'ak47_cats':
            ak47_cats_view()
        elif action == 'ddy':
            daddy_view()
        elif action == 'ddy_cat':
            daddy_cat_view(query.get('i', ['0'])[0])
        elif action == 'ddy_play':
            li = resolve_daddy(query.get('c', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'szx_events':
            sportzx_events_view()
        elif action == 'szx_event':
            sportzx_event_view(query.get('id', [''])[0], query.get('back', [''])[0])
        elif action == 'szx_cats':
            sportzx_cat_view()
        elif action == 'szx_catplay':
            sportzx_catplay_view(query.get('link', [''])[0])
        elif action == 'szx_play':
            li = resolve_sportzx(query.get('id', [''])[0], query.get('i', ['0'])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'htsport':
            htsport_view()
        elif action == 'htsport_refresh':
            htsport_refresh()
        elif action == 'htsport_day':
            htsport_day_view(query.get('di', ['0'])[0])
        elif action == 'htsport_comp':
            htsport_comp_view(query.get('di', ['0'])[0], query.get('ci', ['0'])[0])
        elif action == 'htsport_match':
            htsport_match_view(query.get('di', ['0'])[0], query.get('ci', ['0'])[0], query.get('mi', ['0'])[0])
        elif action == 'htsport_play':
            play_htsport(query.get('page', [''])[0])
        elif action == 'sports':
            sports_view()
        elif action == 'sports_refresh':
            sports_refresh()
        elif action == 'sports_play':
            play_sports(query.get('u', [''])[0])
        elif action == 'sz6':
            sz6_view()
        elif action == 'sz6_refresh':
            sz6_refresh()
        elif action == 'sz6_ev':
            sz6_ev_view(query.get('e', [''])[0])
        elif action == 'sz6_play':
            play_sz6(query.get('e', [''])[0], query.get('i', [''])[0])
    elif 'group' in query:
        group_view(query['group'][0], query.get('deep', [''])[0] == '1',
                   query.get('back', [''])[0])
    else:
        root_view()


if __name__ == '__main__':
    main()
