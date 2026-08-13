# -*- coding: utf-8 -*-
import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE = sys.argv[0]
NAME = ADDON.getAddonInfo('name')

FEEDS = [
    {'title': 'Canale Demo 1', 'url': 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'},
    {'title': 'Canale Demo 2', 'url': 'https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8'},
    {'title': 'Canale Demo 3', 'url': 'https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8'},
]

def play(url):
    li = xbmcgui.ListItem(label=NAME, path=url)
    li.setProperty('isPlayable', 'true')
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

def main():
    if len(sys.argv) > 1:
        query = urllib.parse.parse_qs(sys.argv[2][1:])
        if 'play' in query:
            play(query['play'][0])
            return
    for feed in FEEDS:
        li = xbmcgui.ListItem(label=feed['title'])
        li.setInfo('video', {'title': feed['title']})
        url = BASE + '?play=' + urllib.parse.quote(feed['url'])
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)

if __name__ == '__main__':
    main()
