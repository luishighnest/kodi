# -*- coding: utf-8 -*-
import time
import sys
import re
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

LICENSE_PROP = 'inputstream.adaptive.license_key'
LICENSE_TYPE_PROP = 'inputstream.adaptive.license_type'
MANIFEST_PROP = 'inputstream.adaptive.manifest_type'


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
    if 'group' in query:
        group_view(query['group'][0])
    else:
        root_view()


if __name__ == '__main__':
    main()