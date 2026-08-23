import os
url = "https://dcb-fs-live-dazn-cdn.dazn.com/@eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODc1OTM1MjgsImtpZCI6IjIwMjIxMTIzIiwicGF0aF9kIjoxLCJwYXRoIjoiZDEwODhlYWU3NjM2NTU0ODE5ZDk0ZGU3NWEzMjliM2M0NDZiODQ2YiIsInNzaWQiOiI5ODI3YzNjZjkxZDMiLCJwcm90byI6ImRhc2giLCJnZW8iOiJpdCIsImFzbiI6WyIxMzMzNSJdLCJpYXQiOjE3ODc1MDcxMjh9.MEAcSpqyDUucSjOY6Ip5CENYYt3BOGY4sf9BkKzoHw0/cmehl9tafhudzj6x6cvop1jj/web/stream.mpd?channel=4510&mta=it&outlet=dazn-italy&plang=it"
title = "Zona Serie A Enilive | TOR-MIL ATA-SAS"
extinf = "#EXTINF:-1 tvg-provider=\"DAZN\" group-title=\"DAZN\", " + title
playlist_path = r"C:\Users\alecl\Desktop\kodi_repo\playlist.m3u"
with open(playlist_path, "a", encoding="utf-8") as f:
    f.write("\n" + extinf + "\n" + url)
print("Appended to playlist.m3u")