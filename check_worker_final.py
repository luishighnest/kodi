import requests

worker_url = "https://polished-sky-a2c7.rmddk2364.workers.dev"

print("--- Interrogazione /debug del Worker ---")
try:
    r_dbg = requests.get(worker_url + "/debug", timeout=25)
    print("Debug status:", r_dbg.status_code)
    print("Debug response snippet:\n", r_dbg.text[:600])
except Exception as e:
    print("Debug error:", e)

print("\n--- Interrogazione /playlist.m3u ---")
try:
    r_m3u = requests.get(worker_url + "/playlist.m3u", timeout=25)
    print("M3U status:", r_m3u.status_code)
    print("M3U length:", len(r_m3u.text))
    print("M3U content preview:\n", repr(r_m3u.text[:400]))
except Exception as e:
    print("M3U error:", e)
