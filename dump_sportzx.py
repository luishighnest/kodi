import sys
lines = open(r'C:\Users\alecl\AppData\Roaming\Kodi\addons\plugin.video.mandrakodi\myResolver.py', encoding='utf-8').read().splitlines()
start = [i for i, l in enumerate(lines) if 'def get_channels(' in l]
if start:
    for l in lines[start[0]:start[0]+150]:
        print(l)
else:
    print("Not found")
