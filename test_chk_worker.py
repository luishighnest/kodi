import requests

worker_url = "https://polished-sky-a2c7.rmddk2364.workers.dev"

# 1. Test /playlist.m3u
r1 = requests.get(worker_url + "/playlist.m3u")
print("Playlist status:", r1.status_code)
print("Playlist length:", len(r1.text))
print("Playlist content:\n", repr(r1.text))
