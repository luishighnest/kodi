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
    pname = title
    if parIn.startswith('skysport') and not pname.upper().startswith('SKY'):
        pname = 'SKY ' + pname
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


def sky_view():
    home_button()
    for cat in (CAT_INT, CAT_SPORT):
        label = lbl(cat)
        try:
            c = _sky_counts(cat)
            label += ' | CANALI ATTIVI: %d • CANALI IN SCADENZA: %d • CANALI SCADUTI: %d' % (c.get('ok', 0), c.get('soon', 0), c.get('exp', 0))
        except Exception as e:
            log('sky_counts %s: %s' % (cat, e))
        li = xbmcgui.ListItem(label=label)
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


def resolve_v2(id_, mtype='movie', season='0', episode='0', title=''):
    base = 'https://videm.xyz'
    season = str(season or '0')
    episode = str(episode or '0')
    if mtype == 'tv':
        embed = base + '/embed/tv/%s/%s/%s' % (id_, season, episode)
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
                                      q.get('s') or season, q.get('e') or episode)
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
    li = xbmcgui.ListItem(label=lbl(title or pick.get('name') or 'VidAPI'))
    li.setPath(purl)
    li.setInfo('video', {'title': title, 'mediatype': 'movie' if mtype == 'movie' else 'episode'})
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
            li.setArt({'thumb': TMDB_IMG + 'w342' + poster})
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
            li.setArt({'thumb': TMDB_IMG + 'w342' + still})
        etitle = '%s S%sE%s' % (tname, s, n)
        li.setInfo('video', {'title': etitle, 'plot': ep.get('overview') or '', 'mediatype': 'episode'})
        url = _tmdb_url('v2play', id=id_, mtype='tv', s=s, e=str(n), t=etitle)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_add_item(it, mtype, back=''):
    title = html.unescape(it.get('title') or it.get('name') or '')
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
    li = xbmcgui.ListItem(path=urlSc, label='[COLOR snow]%s[/COLOR]' % (title or ''), offscreen=True)
    if s and e:
        li.setLabel2('S%dE%d: %s' % (s, e, eptitle or ''))
    li.setInfo('video', {'title': title or ''})
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
                poster_url = SQUARE_ICON
                fanart_url = None
                for im in title_obj.get('images', []):
                    if im.get('type') == 'poster' and im.get('filename'):
                        poster_url = 'https://cdn.streamingunity.vip/images/' + im['filename']
                    elif im.get('type') == 'background' and im.get('filename'):
                        fanart_url = 'https://cdn.streamingunity.vip/images/' + im['filename']
                seasons = title_obj.get('seasons', [])
                for s in seasons:
                    n = s.get('number')
                    if n and n > 0:
                        s_num = str(n)
                        par = f"{code}---{s_num}"
                        stitle = f"Stagione {s_num}"
                        li = xbmcgui.ListItem(label=lbl(stitle))
                        art = {'thumb': poster_url, 'poster': poster_url}
                        if fanart_url:
                            art['fanart'] = fanart_url
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
        url = _tmdb_url('mplay', p=parIn, t=show_name, ept=name, s=numSea, e=numep)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
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


def events_view():
    home_button()
    li = xbmcgui.ListItem(label=lbl('Eventi 1'))
    li.setArt({'thumb': LOGO_BASE + 'eventi_icon.png'})
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?group=' + urllib.parse.quote('Eventi'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 2 (Sportzx)'))
    li.setArt({'thumb': LOGO_BASE + 'sportzx.png'})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('sportzx'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('Eventi 3 (Daddy)'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('ddy'), li, isFolder=True)
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


def sportzx_view():
    back_button(BASE + '?action=events')
    li = xbmcgui.ListItem(label=lbl('Eventi live'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('szx_events'), li, isFolder=True)
    li = xbmcgui.ListItem(label=lbl('SportzX TV'))
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('szx_cats'), li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


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
    try:
        ch = _szx_channels(eid)[int(idx)]
    except Exception:
        notify('Sportzx', 'Canale non disponibile', True)
        return xbmcgui.ListItem()
    link = ch.get('link') or ''
    if not link:
        notify('Sportzx', 'Nessun link per questo canale', True)
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


def empty_item():
    li = xbmcgui.ListItem(label=' ')
    li.setArt({'thumb': EMPTY_LOGO, 'icon': EMPTY_LOGO})
    xbmcplugin.addDirectoryItem(HANDLE, BASE, li, isFolder=False)


def _ver_tuple(s):
    return tuple(int(x) for x in re.findall(r'\d+', s) or ['0'])


def check_update():
    try:
        r = requests.get(REPO_BASE + '/addons.xml', timeout=15)
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
        z = requests.get(REPO_BASE + '/zips/plugin.video.kodiakso/plugin.video.kodiakso-' + new + '.zip',
                         timeout=120)
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
    back_button(BASE + '?action=root')
    check_update()
    xbmc.executebuiltin('Container.Update("%s?action=root", replace)' % BASE)
    xbmcplugin.endOfDirectory(HANDLE)


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
        ('EVENTI', LOGO_BASE + 'eventi_icon.png', BASE + '?action=events'),
        ('SKY', LOGO_BASE + 'skyhd.png', BASE + '?action=sky'),
        ('DAZN', LOGO_BASE + 'dazn.png', BASE + '?group=' + urllib.parse.quote('DAZN')),
        ('TV', LOGO_BASE + 'tv_icon.png', BASE + '?action=tv'),
    ]
    if ADDON.getSetting('home_tmdb') != 'false':
        home_items.append(('VOD 1', LOGO_BASE + 'netflix.png', BASE + '?action=films'))
        home_items.append(('VOD 2', LOGO_BASE + 'netflix.png', BASE + '?action=films&src=2'))
    for label, icon, url in home_items:
        if label == 'VOD 1':
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

    xbmcplugin.endOfDirectory(HANDLE)


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
        elif action == 'sky':
            sky_view()
        elif action == 'tv':
            tv_view()
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
                            query.get('t', [''])[0])
            if li:
                xbmcplugin.setResolvedUrl(HANDLE, True, li)
            else:
                notify(NAME, 'Nessun flusso VixSrc disponibile', True)
                xbmcplugin.endOfDirectory(HANDLE)
        elif action == 'skycat':
            sky_cat_view(query.get('cat', [''])[0], query.get('back', [''])[0])
        elif action == 'skyplay':
            li = resolve_sky(query.get('id', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'sportzx':
            sportzx_view()
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
    elif 'group' in query:
        group_view(query['group'][0], query.get('deep', [''])[0] == '1',
                   query.get('back', [''])[0])
    else:
        root_view()


if __name__ == '__main__':
    main()