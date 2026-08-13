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
            label = meta.partition(',')[2].strip()
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
    channels = []
    seen = set()
    try:
        data = requests.get(API + '?numTest=A1A260', headers={'User-Agent': API_UA}, timeout=15).json()
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            mr = it.get('myresolve', '') or ''
            if mr.startswith('sky@@'):
                cid = mr.split('@@', 1)[1]
                if cid not in seen:
                    seen.add(cid)
                    channels.append((strip_color(it.get('title', cid)), cid))
    except Exception as e:
        log('sky A1A260 fail: ' + str(e))
    try:
        data = requests.get(API + '?numTest=A1A122', headers={'User-Agent': API_UA}, timeout=15).json()
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            title = it.get('title', '')
            if 'Sky' in title and ('IT:' in title or 'IT ' in title):
                clean = strip_color(title).replace('IT:', '').replace('IT', '').strip().replace('  ', ' ')
                cid = clean.replace(' ', '').lower()
                if cid == 'skytg24':
                    cid = 'tg24'
                if cid not in seen:
                    seen.add(cid)
                    channels.append((clean, cid))
    except Exception as e:
        log('sky A1A122 fail: ' + str(e))
    if not channels:
        fallback = [("Sky TG 24", "tg24"), ("Sky Uno", "skyuno"), ("Sky Uno +1", "skyunoplus"),
                    ("Sky Atlantic", "skyatlantic"), ("Sky Serie", "skyserie"),
                    ("Sky Collection", "skycollection"), ("Sky Investigation", "skyinvestigation"),
                    ("Sky Adventure", "skyadventure"), ("Sky Crime", "skycrime"),
                    ("Sky Documentaries", "skydocumentaries"), ("Sky Nature", "skynature"),
                    ("History", "historychannel"), ("Comedy Central", "comedycentral"),
                    ("Sky Arte", "skyarte"), ("MTV", "mtv"), ("Sky Sport Uno", "skysportuno"),
                    ("Sky Sport 24", "skysport24"), ("Sky Sport Arena", "skysportarena"),
                    ("Sky Sport Calcio", "skysportcalcio"), ("Sky Sport F1", "skysportf1"),
                    ("Sky Sport Golf", "skysportgolf"), ("Sky Sport Legend", "skysportlegend"),
                    ("Sky Sport Max", "skysportmax"), ("Sky Sport Mix", "skysportmix"),
                    ("Sky Sport MotoGP", "skysportmotogp"), ("Sky Sport Tennis", "skysporttennis"),
                    ("Sky Sport Basket", "skysportbasket")]
        for t, c in fallback:
            channels.append((t, c))
    for n in range(251, 260):
        cid = 'skysport%d' % n
        if cid not in seen:
            seen.add(cid)
            channels.append(('Sky Sport %d' % n, cid))
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
        li = xbmcgui.ListItem(label=ch['label'], path=ch['url'])
        if ch['logo']:
            li.setArt({'thumb': ch['logo']})
        li.setProperty('isPlayable', 'true')
        li.setProperty('inputstream', 'inputstream.adaptive')
        for k, v in ch['props'].items():
            if k == 'inputstream' and not v:
                continue
            li.setProperty(k, v)
        xbmcplugin.addDirectoryItem(HANDLE, ch['url'], li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def sky_view():
    for title, cid in sky_channels():
        li = xbmcgui.ListItem(label=title)
        li.setProperty('isPlayable', 'true')
        url = BASE + '?action=skyplay&id=' + urllib.parse.quote(cid) + '&t=' + urllib.parse.quote(title)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def root_view():
    channels = fetch_channels()
    groups = {}
    for ch in channels:
        groups.setdefault(ch['group'], []).append(ch)
    for group in sorted(groups):
        li = xbmcgui.ListItem(label=group)
        url = BASE + '?group=' + urllib.parse.quote(group)
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)
    sky = xbmcgui.ListItem(label='Sky')
    xbmcplugin.addDirectoryItem(HANDLE, BASE + '?action=sky', sky, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def main():
    query = urllib.parse.parse_qs(sys.argv[2][1:])
    if 'action' in query:
        action = query['action'][0]
        if action == 'sky':
            sky_view()
        elif action == 'skyplay':
            li = resolve_sky(query.get('id', [''])[0], query.get('t', [''])[0])
            xbmcplugin.setResolvedUrl(HANDLE, True, li)
    elif 'group' in query:
        group_view(query['group'][0])
    else:
        root_view()


if __name__ == '__main__':
    main()