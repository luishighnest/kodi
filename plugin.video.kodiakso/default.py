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

API = 'https://test34344.herokuapp.com/filter.php'
SECRET = b'my_secret_key'
API_UA = 'Kodi/19.0 (Windows NT 10.0; Win64; x64) App_Bitness/64 Version/19.0-Matrix'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
HOST = 'https://www.nowtv.it'
LOGO_BASE = 'https://luishighnest.github.io/kodi/logos/'
SQUARE_ICON = LOGO_BASE + 'square.png'
DOT_ICON = LOGO_BASE + 'dot.png'
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
    url = PLAYLIST_URL + ('&' if '?' in PLAYLIST_URL else '?') + '_=' + str(int(time.time()))
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def fetch_channels():
    try:
        return parse_m3u(get_playlist())
    except Exception:
        xbmcgui.Dialog().notification(NAME, 'Impossibile scaricare la playlist', xbmcgui.NOTIFICATION_ERROR)
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
        xbmcgui.Dialog().notification(title or parIn, 'Errore risoluzione link', xbmc.NOTIFICATION_ERROR)
        return xbmcgui.ListItem()

    manifest = data['manifest']
    kid = data['kid']
    key = data['key']
    fine = data.get('fine', '')
    if 'EXPIRE' not in fine:
        try:
            exp = datetime.strptime(fine, '%d/%m/%Y %H:%M:%S') + timedelta(hours=2)
            if exp < datetime.now():
                xbmcgui.Dialog().notification(title or parIn, 'Link scaduto ' + exp.strftime('%d/%m/%Y %H:%M:%S'),
                                              xbmcgui.NOTIFICATION_ERROR, 5000)
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
        li.setArt({'thumb': DOT_ICON})
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
        li.setArt({'thumb': DOT_ICON})
        url = BASE + '?group=' + urllib.parse.quote(group)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


TMDB_KEY = '2e0b38cfb2936cec8ab1ce48e4335ac3'
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
    params.setdefault('language', 'it-IT')
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
    url = _tmdb_url('details', mt=mtype, id=str(it['id']))
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
        li.setArt({'thumb': DOT_ICON})
        url = _tmdb_url('list', mt=mtype, kind=kind, genre=genre, page=str(page + 1))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_cats(mtype):
    cats = FILM_CATS if mtype == 'movie' else TV_CATS
    for label, kind in cats:
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': DOT_ICON})
        url = _tmdb_url('genres', mt=mtype) if not kind else _tmdb_url('list', mt=mtype, kind=kind, page='1')
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def tmdb_genres(mtype):
    j = tmdb_get('/genre/%s/list' % mtype)
    for g in sorted(j.get('genres', []), key=lambda x: x['name']):
        li = xbmcgui.ListItem(label=lbl(g['name']))
        li.setArt({'thumb': DOT_ICON})
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
    j = tmdb_get('/search/multi', query=query, include_adult='false', page=page)
    xbmcplugin.setContent(HANDLE, 'movies')
    for it in j.get('results', []):
        if it.get('media_type') in ('movie', 'tv'):
            tmdb_add_item(it, it.get('media_type'))
    if page < (j.get('total_pages') or 1) and j.get('results'):
        li = xbmcgui.ListItem(label=lbl('Prossima pagina  ►'))
        li.setArt({'thumb': DOT_ICON})
        url = _tmdb_url('search', q=query, page=str(page + 1))
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def films_view():
    li = xbmcgui.ListItem(label=lbl('Ricerca'))
    li.setArt({'thumb': DOT_ICON})
    xbmcplugin.addDirectoryItem(HANDLE, _tmdb_url('search'), li, isFolder=True)
    for label, mtype in HOME_SECTIONS:
        li = xbmcgui.ListItem(label=lbl(label))
        li.setArt({'thumb': DOT_ICON})
        url = _tmdb_url('cats', mt=mtype)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def root_view():
    home_items = [
        ('SKY', LOGO_BASE + 'skyhd.png', BASE + '?action=sky'),
        ('DAZN', LOGO_BASE + 'dazn.png', BASE + '?group=' + urllib.parse.quote('DAZN')),
        ('EVENTI', LOGO_BASE + 'eventi.png', BASE + '?group=' + urllib.parse.quote('Eventi')),
        ('TV', LOGO_BASE + 'tv.png', BASE + '?action=tv'),
        ('FILM & SERIE TV', LOGO_BASE + 'netflix.png', BASE + '?action=films'),
    ]
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