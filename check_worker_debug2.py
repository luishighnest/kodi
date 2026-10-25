import requests

worker_url = "https://polished-sky-a2c7.rmddk2364.workers.dev"

print("--- Interrogazione /debug ---")
try:
    r = requests.get(worker_url + "/debug", timeout=20)
    print("Status:", r.status_code)
    print("Response snippet:", r.text[:600])
except Exception as e:
    print("Err:", e)
