# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE = sys.argv[0]
NAME = ADDON.getAddonInfo('name')

PLAYLIST_FILE = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'playlist.m3u')
PLAYLIST_URL = ADDON.getSetting('playlist_url').strip()


def get_playlist():
    text = ''
    if PLAYLIST_URL:
        try:
            r = requests.get(PLAYLIST_URL, timeout=15)
            r.raise_for_status()
            text = r.text
        except Exception:
            text = ''
    if not text and os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, 'r', encoding='utf-8-sig') as f:
            text = f.read()
    return text


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


def group_view(group):
    channels = parse_m3u(get_playlist())
    for ch in channels:
        if ch['group'] != group:
            continue
        li = xbmcgui.ListItem(label=ch['label'])
        if ch['logo']:
            li.setArt({'thumb': ch['logo']})
        li.setProperty('IsPlayable', 'true')
        data = urllib.parse.quote(json.dumps({'url': ch['url'], 'props': ch['props']}))
        url = BASE + '?play=' + data
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def root_view():
    channels = parse_m3u(get_playlist())
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
        data = json.loads(urllib.parse.unquote(query['play'][0]))
        play(data['url'], data['props'])
    elif 'group' in query:
        group_view(query['group'][0])
    else:
        root_view()


if __name__ == '__main__':
    main()
