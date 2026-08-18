# -*- coding: utf-8 -*-
import time
import sys
import re
import json
import base64
import gzip
import os
import pickle
import urllib.parse
from datetime import datetime, timedelta
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
LABEL = '[B][COLOR snow]%s[/COLOR][/B]'
BANNER_LOGO = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'banner.png')
ICON_LOGO = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'icon.png')

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
_EXP_CACHE_TTL = 180
_EXP_CACHE_TTL_FAIL = 60


def lbl(txt):
    return LABEL % txt


def _top_button(label, icon, url):
    li = xbmcgui.ListItem(label=lbl(label))
    li.setArt({'thumb': LOGO_BASE + icon})
    li.setProperty('IsPlayable', 'false')
    nav = BASE + '?action=nav&url=' + urllib.parse.quote(url, safe='')
    xbmcplugin.addDirectoryItem(HANDLE, nav, li, isFolder=False)


def home_button():
    _top_button('Home', 'home.png', BASE + '?action=root')


def back_button(url=''):
    if not url:
        url = BASE + '?action=root'
    _top_button('Indietro', 'back.png?v=2', url)

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
    except Exception as e:
        xbmc.log('KODIAKSO sky expiry ERR %s: %s' % (cid, e), xbmc.LOGERROR)
        try:
            import traceback
            xbmc.log('KODIAKSO sky expiry TB:\n' + traceback.format_exc(), xbmc.LOGERROR)
        except Exception:
            pass
    _EXP_CACHE[cid] = (time.time(), exp)
    _exp_cache_save(_EXP_CACHE)
    return exp


def resolve_sky(parIn, title):
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
    if not q:
        kb = xbmc.Keyboard('', 'Ricerca globale (canali ed eventi)')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            xbmcplugin.endOfDirectory(HANDLE)
            return
        q = kb.getText().strip()
    ql = q.lower()
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
            li = xbmcgui.ListItem(label=lbl(t))
            logo = LOGOS.get(cid, '')
            li.setArt({'thumb': (LOGO_BASE + logo) if logo else SQUARE_ICON})
            li.setProperty('isPlayable', 'true')
            url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(t)
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
            added += 1

    if not added:
        li = xbmcgui.ListItem(label=lbl('Nessun risultato per "%s"' % q))
        xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sky_view():
    home_button()
    for cat in (CAT_INT, CAT_SPORT):
        li = xbmcgui.ListItem(label=lbl(cat))
        
        url = BASE + '?action=skycat&cat=' + urllib.parse.quote(cat) + '&back=' + urllib.parse.quote(BASE + '?action=sky')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
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
                        int(s[8:10]), int(s[10:12]), int(s[12:14]))
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


def _exp_header(label, count, color):
    li = xbmcgui.ListItem(label='[COLOR %s]%s: %d[/COLOR]' % (color, label, count))
    li.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=root', li, isFolder=False)


def sky_cat_view(cat, back=''):
    back_button(back or (BASE + '?action=sky'))
    epg = epg_load() if ADDON.getSetting('epg_enabled') == 'true' else None
    try:
        chans = sky_channels().get(cat, [])
        counts = {'ok': 0, 'soon': 0, 'exp': 0}
        for title, cid in chans:
            st = _exp_status(_sky_expiry(cid)) or 'ok'
            counts[st] = counts.get(st, 0) + 1
        _exp_header('Canali attivi', counts.get('ok', 0), EXP_OK_COLOR)
        _exp_header('Canali in scadenza (scadono da qui a 1 ora)', counts.get('soon', 0), EXP_SOON_COLOR)
        _exp_header('Canali scaduti', counts.get('exp', 0), EXP_EXP_COLOR)
        for title, cid in chans:
            try:
                label = '[COLOR snow]%s[/COLOR]' % title
                exp = _sky_expiry(cid)
                if exp:
                    label += '   [COLOR %s]%s[/COLOR]' % (_exp_color(_exp_status(exp)), exp.strftime('%d/%m/%Y %H:%M'))
                cur, nxt = _epg_now(cid, epg)
                if cur:
                    label += '   [COLOR %s]%02d:%02d %s[/COLOR]' % (EXP_OK_COLOR, cur[0].hour, cur[0].minute, _epg_short(cur[2]))
                li = xbmcgui.ListItem(label=label)
                logo = LOGOS.get(cid, '')
                li.setArt({'thumb': (LOGO_BASE + logo) if logo else SQUARE_ICON})
                li.setProperty('isPlayable', 'true')
                lines = []
                if exp:
                    lines.append('Scadenza %s' % exp.strftime('%d/%m/%Y %H:%M'))
                if cur:
                    lines.append('Ora %02d:%02d %s' % (cur[0].hour, cur[0].minute, _epg_short(cur[2], 60)))
                if nxt:
                    lines.append('%02d:%02d %s' % (nxt[0].hour, nxt[0].minute, _epg_short(nxt[2], 60)))
                li.setInfo('video', {'title': title, 'plot': ' | '.join(lines)})
                url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(title)
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
    channels = fetch_channels()
    groups = {}
    for ch in channels:
        if ch['group'].lower() in ('dazn', 'eventi'):
            continue
        groups.setdefault(ch['group'], []).append(ch)
    for group in sorted(groups):
        li = xbmcgui.ListItem(label=lbl(group))
        
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
    return BASE + '?action=' + action + '&' + urllib.parse.urlencode(params)


def tmdb_add_item(it, mtype, back=''):
    title = it.get('title') or it.get('name') or ''
    date = it.get('release_date') or it.get('first_air_date') or ''
    label = title + ('  (' + date[:4] + ')' if len(date) >= 4 else '')
    li = xbmcgui.ListItem(label=lbl(label))
    poster = it.get('poster_path')
    li.setArt({'thumb': TMDB_IMG + 'w342' + poster if poster else SQUARE_ICON})
    fan = it.get('backdrop_path')
    if fan:
        li.setArt({'fanart': TMDB_IMG + 'w780' + fan})
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
        url = _tmdb_url('mplayauto', q=title, back=back)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
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
    title = j.get('title') or j.get('name') or ''
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

    play = xbmcgui.ListItem(label=lbl('▶  Riproduci con Mandrakodi'))
    play.setArt({'thumb': SQUARE_ICON})
    details_url = BASE + '?action=details&mt=' + urllib.parse.quote(mtype) + '&id=' + urllib.parse.quote(id_)
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('msearch', q=title, mt=mtype, back=details_url), play, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_search(query='', page=1, back=''):
    back_button(back or (BASE + '?action=films'))
    page = int(page)
    if not query:
        kb = xbmc.Keyboard('', 'Cerca in TMDB')
        kb.doModal()
        if not kb.isConfirmed() or not kb.getText().strip():
            xbmcplugin.endOfDirectory(HANDLE)
            return
        query = kb.getText().strip()
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


def resolve_scws(parIn, title):
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
        notify(title or parIn, 'Errore risoluzione link', True)
        return xbmcgui.ListItem()

    hdrs = 'User-Agent=' + UA + '&Referer=' + cs + '&Origin=' + cs + '&verifypeer=false'
    li = xbmcgui.ListItem(path=urlSc, offscreen=True)
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
    notify(query or 'Film', 'Nessun risultato su Mandrakodi', True)
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
    notify(query or 'Serie', 'Nessuna serie su Mandrakodi', True)
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
        li = xbmcgui.ListItem(label=lbl('Nessun risultato su Mandrakodi'))
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('msearch', q=query), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def mandra_season_view(code, back=''):
    back_button(back or (BASE + '?action=films'))
    data = requests.get(API + '?numTest=A1A356&mode=2&code=' + urllib.parse.quote(code),
                        headers={'User-Agent': API_UA}, timeout=25).json()
    xbmcplugin.setContent(HANDLE, 'tvshows')
    season_url = BASE + '?action=mseason&code=' + urllib.parse.quote(code)
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
    show_name = props['title']['name']
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
        name = ep.get('name') or label
        li = xbmcgui.ListItem(label=lbl(label))
        plot = (ep.get('plot') or '').replace('&#39;', "'").replace('&amp;', '&')
        info = {'title': name, 'plot': plot, 'mediatype': 'episode',
                'tvshowtitle': show_name, 'season': numSea}
        try:
            info['episode'] = int(ep.get('number') or 0)
        except (TypeError, ValueError):
            pass
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
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('mplay', p=parIn, t=label), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def films_view():
    home_button()
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


def root_view():
    bann = xbmcgui.ListItem(label='[B][COLOR gray]PZ8[/COLOR][/B]')
    bann.setArt({'banner': BANNER_LOGO, 'clearlogo': BANNER_LOGO, 'icon': ICON_LOGO, 'thumb': ''})
    bann.setInfo('video', {'title': 'PZ8', 'plot': 'SPORT | TV | VOD'})
    bann.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(HANDLE, BASE, bann, isFolder=True)

    li = xbmcgui.ListItem(label=lbl('Ricerca globale'))
    li.setArt({'thumb': SEARCH_ICON})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('gsearch'), li, isFolder=True)

    home_items = [
        ('SKY', LOGO_BASE + 'skyhd.png', BASE + '?action=sky'),
        ('DAZN', LOGO_BASE + 'dazn.png', BASE + '?group=' + urllib.parse.quote('DAZN')),
        ('EVENTI', LOGO_BASE + 'eventi_icon.png', BASE + '?group=' + urllib.parse.quote('Eventi')),
        ('TV', LOGO_BASE + 'tv_icon.png', BASE + '?action=tv'),
    ]
    if ADDON.getSetting('home_tmdb') != 'false':
        home_items.append(('VOD', LOGO_BASE + 'netflix.png', BASE + '?action=films'))
    for label, icon, url in home_items:
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': icon or SQUARE_ICON})
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def main():
    query = urllib.parse.parse_qs(sys.argv[2][1:])
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
        elif action == 'sky':
            sky_view()
        elif action == 'tv':
            tv_view()
        elif action == 'films':
            films_view()
        elif action == 'gsearch':
            gsearch_view(query.get('q', [''])[0])
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
            mandra_auto_movie(query.get('q', [''])[0])
        elif action == 'mseasonsauto':
            mandra_auto_series(query.get('q', [''])[0], query.get('back', [''])[0])
        elif action == 'mseason':
            mandra_season_view(query.get('code', [''])[0], query.get('back', [''])[0])
        elif action == 'mepisodes':
            mandra_episodes_view(query.get('par', [''])[0], query.get('back', [''])[0])
        elif action == 'mplay':
            li = resolve_scws(query.get('p', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'skycat':
            sky_cat_view(query.get('cat', [''])[0], query.get('back', [''])[0])
        elif action == 'skyplay':
            li = resolve_sky(query.get('id', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
    elif 'group' in query:
        group_view(query['group'][0], query.get('deep', [''])[0] == '1',
                   query.get('back', [''])[0])
    else:
        root_view()


if __name__ == '__main__':
    main()