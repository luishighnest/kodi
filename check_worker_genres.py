import requests

# Test if the worker has /test_profile or let's test specific stalker queries
# Let's inspect what genres nxtbox returns
worker_url = "https://polished-sky-a2c7.rmddk2364.workers.dev"

# Let's query what happens on genres
r = requests.get(worker_url + "/playlist.m3u")
print("Status:", r.status_code, "len:", len(r.text))
