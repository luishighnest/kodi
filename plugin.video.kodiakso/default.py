# -*- coding: utf-8 -*-
import time
import sys
import re
import json
import base64
import urllib.parse
from datetime import datetime, timedelta
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
LABEL = '[B][COLOR snow]%s[/COLOR][/B]'


def lbl(txt):
    return LABEL % txt

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

CAT_INT = 'Intrattenimento'
CAT_SPORT = 'Sport'

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
        data = requests.get(API + '?numTest=A1A260', headers={'User-Agent': API_UA}, timeout=15).json()
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            mr = it.get('myresolve', '') or ''
            if mr.startswith('sky@@'):
                push(mr.split('@@', 1)[1])
    except Exception as e:
        log('sky A1A260 fail: ' + str(e))
    try:
        data = requests.get(API + '?numTest=A1A122', headers={'User-Agent': API_UA}, timeout=15).json()
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
    if not order:
        for cid in SKY_DEFS:
            push(cid)
    for n in range(251, 260):
        push('skysport%d' % n)
    channels = {CAT_INT: [], CAT_SPORT: []}
    for cid in order:
        if cid.startswith('skysport') and cid not in SKY_DEFS:
            m = re.match(r'^skysport(\d+)$', cid)
            name = ('Sky Sport ' + m.group(1)) if m else cid
        else:
            name = SKY_DEFS.get(cid, (cid, ''))[0]
        cat = SKY_DEFS.get(cid, (cid, CAT_SPORT if cid.startswith('skysport') else CAT_INT))[1]
        channels[cat].append((name, cid))
    return channels


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
    if 'EXPIRE' not in fine:
        try:
            exp = datetime.strptime(fine, '%d/%m/%Y %H:%M:%S') + timedelta(hours=2)
            if exp < datetime.now():
                notify(title or parIn, 'Link scaduto ' + exp.strftime('%d/%m/%Y %H:%M:%S'), True)
        except Exception:
            pass

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


def group_view(group):
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


def sky_view():
    for cat in (CAT_INT, CAT_SPORT):
        li = xbmcgui.ListItem(label=lbl(cat))
        
        url = BASE + '?action=skycat&cat=' + urllib.parse.quote(cat)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def sky_cat_view(cat):
    for title, cid in sky_channels().get(cat, []):
        li = xbmcgui.ListItem(label=lbl(title))
        logo = LOGOS.get(cid, '')
        li.setArt({'thumb': (LOGO_BASE + logo) if logo else SQUARE_ICON})
        li.setProperty('isPlayable', 'true')
        url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(title)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def tv_view():
    channels = fetch_channels()
    groups = {}
    for ch in channels:
        if ch['group'].lower() in ('dazn', 'eventi'):
            continue
        groups.setdefault(ch['group'], []).append(ch)
    for group in sorted(groups):
        li = xbmcgui.ListItem(label=lbl(group))
        
        url = BASE + '?group=' + urllib.parse.quote(group)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


TMDB_KEY = ADDON.getSetting('tmdb_key').strip() or '2e0b38cfb2936cec8ab1ce48e4335ac3'
TMDB_LANG = ADDON.getSetting('tmdb_language').strip() or 'it-IT'
TMDB_ADULT = ADDON.getSetting('tmdb_adult') == 'true'
TMDB_URL = 'https://api.themoviedb.org/3'
TMDB_IMG = 'https://image.tmdb.org/t/p/'

HOME_SECTIONS = [('Film', 'movie'), ('Serie TV', 'tv')]
FILM_CATS = [('Popolari', 'popular'), ('In sala', 'now_playing'),
             ('Prossimamente', 'upcoming'), ('Più votati', 'top_rated'),
             ('Per genere', '')]
TV_CATS = [('Popolari', 'popular'), ('In onda oggi', 'airing_today'),
           ('In TV', 'on_the_air'), ('Più votate', 'top_rated'),
           ('Per genere', '')]


def tmdb_get(path, **params):
    params['api_key'] = TMDB_KEY
    params.setdefault('language', TMDB_LANG)
    r = requests.get(TMDB_URL + path, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def _tmdb_url(action, **params):
    return BASE + '?action=' + action + '&' + urllib.parse.urlencode(params)


def tmdb_add_item(it, mtype):
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
        url = _tmdb_url('mplayauto', q=title)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    else:
        url = _tmdb_url('mseasonsauto', q=title)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)


def tmdb_list(mtype, kind='', genre='', page=1):
    page = int(page)
    if genre:
        path = '/discover/' + mtype
        params = {'with_genres': genre, 'sort_by': 'popularity.desc', 'page': page}
    else:
        path = '/%s/%s' % (mtype, kind)
        params = {'page': page}
    j = tmdb_get(path, **params)
    xbmcplugin.setContent(HANDLE, 'movies' if mtype == 'movie' else 'tvshows')
    for it in j.get('results', []):
        tmdb_add_item(it, mtype)
    if page < (j.get('total_pages') or 1) and j.get('results'):
        li = xbmcgui.ListItem(label=lbl('Prossima pagina  ►'))
        
        url = _tmdb_url('list', mt=mtype, kind=kind, genre=genre, page=str(page + 1))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_cats(mtype):
    cats = FILM_CATS if mtype == 'movie' else TV_CATS
    for label, kind in cats:
        li = xbmcgui.ListItem(label=lbl(label))
        
        url = _tmdb_url('genres', mt=mtype) if not kind else _tmdb_url('list', mt=mtype, kind=kind, page='1')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_genres(mtype):
    j = tmdb_get('/genre/%s/list' % mtype)
    for g in sorted(j.get('genres', []), key=lambda x: x['name']):
        li = xbmcgui.ListItem(label=lbl(g['name']))
        
        url = _tmdb_url('list', mt=mtype, genre=str(g['id']), page='1')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_details(mtype, id_):
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
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('msearch', q=title, mt=mtype), play, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_search(query='', page=1):
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
    for it in j.get('results', []):
        if it.get('media_type') in ('movie', 'tv'):
            tmdb_add_item(it, it.get('media_type'))
    if page < (j.get('total_pages') or 1) and j.get('results'):
        li = xbmcgui.ListItem(label=lbl('Prossima pagina  ►'))
        
        url = _tmdb_url('search', q=query, page=str(page + 1))
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
    stream = _scws_pick_variant(urlSc, cs, title)
    if not stream:
        return xbmcgui.ListItem()
    li = xbmcgui.ListItem(path=stream, offscreen=True)
    li.setContentLookup(False)
    li.setMimeType('application/x-mpegURL')
    li.setProperty('inputstream', 'inputstream.ffmpegdirect')
    li.setProperty('inputstream.ffmpegdirect.manifest_type', 'hls')
    li.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')
    li.setProperty('inputstream.ffmpegdirect.stream_headers', hdrs)
    return li


def _scws_abs(base, uri):
    if uri.startswith(('http://', 'https://')):
        return uri
    if uri.startswith('/'):
        pr = urllib.parse.urlparse(base)
        return pr.scheme + '://' + pr.netloc + uri
    return base.rsplit('/', 1)[0] + '/' + uri


def _scws_pick_variant(master, base, title):
    try:
        r = requests.get(master, headers={'user-agent': UA, 'referer': base,
                                          'origin': base, 'verifypeer': 'false'}, timeout=25)
        r.raise_for_status()
        text = r.text
    except Exception as e:
        xbmc.log('KODIAKSO scws variant ERR: ' + str(e), xbmc.LOGERROR)
        return master
    lines = text.splitlines()
    audio_media = [ln for ln in lines if ln.startswith('#EXT-X-MEDIA')]
    variants = []
    for i, ln in enumerate(lines):
        if ln.startswith('#EXT-X-STREAM-INF'):
            res = re.search(r'RESOLUTION=(\d+)x(\d+)', ln)
            bw = re.search(r'BANDWIDTH=(\d+)', ln)
            vuri = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if vuri and not vuri.startswith('#'):
                if res:
                    h = int(res.group(2))
                    name = '%dp' % h
                elif bw:
                    name = '%d kbps' % (int(bw.group(1)) // 1000)
                else:
                    name = 'Auto'
                variants.append((name, ln, vuri))
    if not variants:
        return master
    picked = None
    if len(variants) > 1:
        names = [v[0] for v in variants]
        idx = xbmcgui.Dialog().select(title or 'Qualità video', names)
        picked = variants[idx] if idx >= 0 else None
    else:
        picked = variants[0]
    if not picked:
        return None
    name, sinf, vuri = picked
    vurl = _scws_abs(master, vuri)
    if not audio_media:
        return vurl
    try:
        aud_rows = []
        for a in audio_media:
            grp = re.search(r'GROUP-ID="([^"]+)"', a)
            uri = re.search(r'URI="([^"]+)"', a)
            if grp and uri:
                aud_rows.append(a.replace('URI="%s"' % uri.group(1),
                                          'URI="%s"' % _scws_abs(master, uri.group(1))))
        if not aud_rows:
            return vurl
        vgrp = re.search(r'AUDIO="([^"]+)"', sinf)
        if vgrp:
            aud_rows = [a for a in aud_rows
                        if re.search(r'GROUP-ID="%s"' % re.escape(vgrp.group(1)), a)]
        m3u = '#EXTM3U\n'
        ver = re.search(r'^#EXT-X-VERSION:(\d+)$', text, re.M)
        if ver:
            m3u += '#EXT-X-VERSION:%s\n' % ver.group(1)
        m3u += '\n'.join(aud_rows) + '\n'
        m3u += sinf + '\n' + vurl + '\n'
        import os
        import xbmcvfs
        tmp = xbmcvfs.translatePath('special://temp/')
        fp = os.path.join(tmp, 'kodiakso_%d.m3u8' % time.time())
        with open(fp, 'w') as f:
            f.write(m3u)
        return fp
    except Exception as e:
        xbmc.log('KODIAKSO scws mini-master ERR: ' + str(e), xbmc.LOGERROR)
        return vurl


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


def mandra_auto_series(query):
    try:
        data = requests.get(API + '?numTest=A1A332A&mode=1&search=' + urllib.parse.quote(query),
                            headers={'User-Agent': API_UA}, timeout=25).json()
    except Exception as e:
        xbmc.log('KODIAKSO mandra series ERR: ' + str(e), xbmc.LOGERROR)
        notify(query or 'Serie', 'Errore ricerca', True)
        xbmcplugin.endOfDirectory(HANDLE)
        return
    for it in data.get('items', []):
        ext = it.get('externallink', '') or ''
        m = re.search(r'code=([^&]+)', ext)
        if m:
            mandra_season_view(m.group(1))
            return
    notify(query or 'Serie', 'Nessuna serie su Mandrakodi', True)
    xbmcplugin.endOfDirectory(HANDLE)


def mandra_search_view(query, mtype=''):
    if not query:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    data = requests.get(API + '?numTest=A1A332A' + ('&mode=1' if mtype == 'tv' else '') + '&search=' + urllib.parse.quote(query),
                        headers={'User-Agent': API_UA}, timeout=25).json()
    xbmcplugin.setContent(HANDLE, 'movies' if mtype == 'movie' else 'tvshows')
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
                url = _tmdb_url('mseason', code=m.group(1))
                xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
                added += 1
    if not added:
        li = xbmcgui.ListItem(label=lbl('Nessun risultato su Mandrakodi'))
        xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('msearch', q=query), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def mandra_season_view(code):
    data = requests.get(API + '?numTest=A1A356&mode=2&code=' + urllib.parse.quote(code),
                        headers={'User-Agent': API_UA}, timeout=25).json()
    xbmcplugin.setContent(HANDLE, 'tvshows')
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
        url = _tmdb_url('mepisodes', par=par)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def mandra_episodes_view(par):
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
    li = xbmcgui.ListItem(label=lbl('Ricerca'))
    
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('search'), li, isFolder=True)
    for label, mtype in HOME_SECTIONS:
        li = xbmcgui.ListItem(label=lbl(label))
        
        url = _tmdb_url('cats', mt=mtype)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def root_view():
    home_items = [
        ('SKY', LOGO_BASE + 'skyhd.png', BASE + '?action=sky'),
        ('DAZN', LOGO_BASE + 'dazn.png', BASE + '?group=' + urllib.parse.quote('DAZN')),
        ('EVENTI', LOGO_BASE + 'eventi_icon.png', BASE + '?group=' + urllib.parse.quote('Eventi')),
        ('TV', LOGO_BASE + 'tv_icon.png', BASE + '?action=tv'),
    ]
    if ADDON.getSetting('home_tmdb') != 'false':
        home_items.append(('FILM & SERIE TV', LOGO_BASE + 'netflix.png', BASE + '?action=films'))
    for label, icon, url in home_items:
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': icon or SQUARE_ICON})
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def main():
    query = urllib.parse.parse_qs(sys.argv[2][1:])
    if 'action' in query:
        action = query['action'][0]
        if action == 'sky':
            sky_view()
        elif action == 'tv':
            tv_view()
        elif action == 'films':
            films_view()
        elif action == 'search':
            tmdb_search(query.get('q', [''])[0], int(query.get('page', ['1'])[0]))
        elif action == 'cats':
            tmdb_cats(query.get('mt', ['movie'])[0])
        elif action == 'genres':
            tmdb_genres(query.get('mt', ['movie'])[0])
        elif action == 'list':
            q = query
            tmdb_list(q.get('mt', ['movie'])[0], q.get('kind', [''])[0],
                      q.get('genre', [''])[0], int(q.get('page', ['1'])[0]))
        elif action == 'details':
            tmdb_details(query.get('mt', ['movie'])[0], query.get('id', [''])[0])
        elif action == 'msearch':
            mandra_search_view(query.get('q', [''])[0], query.get('mt', [''])[0])
        elif action == 'mplayauto':
            mandra_auto_movie(query.get('q', [''])[0])
        elif action == 'mseasonsauto':
            mandra_auto_series(query.get('q', [''])[0])
        elif action == 'mseason':
            mandra_season_view(query.get('code', [''])[0])
        elif action == 'mepisodes':
            mandra_episodes_view(query.get('par', [''])[0])
        elif action == 'mplay':
            li = resolve_scws(query.get('p', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
        elif action == 'skycat':
            sky_cat_view(query.get('cat', [''])[0])
        elif action == 'skyplay':
            li = resolve_sky(query.get('id', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
    elif 'group' in query:
        group_view(query['group'][0])
    else:
        root_view()


if __name__ == '__main__':
    main()