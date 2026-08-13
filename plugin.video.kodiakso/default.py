# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import base64
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE = sys.argv[0]
NAME = ADDON.getAddonInfo('name')

DEFAULT_URL = 'https://luishighnest.github.io/kodi/playlist.m3u'
PLAYLIST_URL = ADDON.getSetting('playlist_url').strip() or DEFAULT_URL


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
            props[key.strip()] = value.strip().strip('"')
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


def play(url, props):
    li = xbmcgui.ListItem(label=NAME, path=url)
    li.setProperty('isPlayable', 'true')
    li.setProperty('inputstream', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', props.get('inputstream.adaptive.manifest_type', 'mpd'))
    for k in ('inputstream.adaptive.license_type', 'inputstream.adaptive.license_key'):
        if props.get(k):
            li.setProperty(k, props[k])
    xbmcplugin.setResolvedUrl(HANDLE, True, li)


def encode_payload(title, url, props):
    payload = json.dumps({'label': title, 'url': url, 'props': props})
    token = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii').rstrip('=')
    return token


def group_view(group):
    channels = fetch_channels()
    for ch in channels:
        if ch['group'] != group:
            continue
        li = xbmcgui.ListItem(label=ch['label'])
        if ch['logo']:
            li.setArt({'thumb': ch['logo']})
        li.setProperty('IsPlayable', 'true')
        token = encode_payload(ch['label'], ch['url'], ch['props'])
        url = BASE + '?play=' + urllib.parse.quote(token)
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
    xbmcplugin.endOfDirectory(HANDLE)


def main():
    query = urllib.parse.parse_qs(sys.argv[2][1:])
    if 'play' in query:
        token = urllib.parse.unquote(query['play'][0])
        padded = token + '=' * (-len(token) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode('ascii')).decode('utf-8'))
        play(data['url'], data['props'])
    elif 'group' in query:
        group_view(query['group'][0])
    else:
        root_view()


if __name__ == '__main__':
    main()
