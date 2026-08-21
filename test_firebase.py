import requests
fid = "fake_fid_0123456789012"
install_url = "https://firebaseinstallations.googleapis.com/v1/projects/sportzx-7cc3f/installations"
install_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Dalvik/2.1.0 (Linux; Android 13)",
    "x-firebase-client": "H4sIAAAAAAAAAKtWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA",
    "x-goog-api-key": "AIzaSyBa5qiq95T97xe4uSYlKo0Wosmye_UEf6w"
}
install_body = {
    "fid": fid,
    "appId": "1:446339309956:android:b26582b5d2ad841861bdd1",
    "authVersion": "FIS_v2",
    "sdkVersion": "a:18.0.0"
}
try:
    r = requests.post(install_url, json=install_body, headers=install_headers)
    token = r.json().get("authToken", {}).get("token")
    print("Token:", token)
    config_url = "https://firebaseremoteconfig.googleapis.com/v1/projects/446339309956/namespaces/firebase:fetch"
    config_headers = {
        "Content-Type": "application/json",
        "X-Firebase-RC-Fetch-Type": "BASE/1",
        "X-Goog-Api-Key": "AIzaSyBa5qiq95T97xe4uSYlKo0Wosmye_UEf6w",
        "X-Goog-Firebase-Installations-Auth": token,
    }
    config_body = {
        "appVersion": "3.2",
        "appInstanceIdToken": token,
        "appInstanceId": fid,
        "appId": "1:446339309956:android:b26582b5d2ad841861bdd1",
    }
    r2 = requests.post(config_url, json=config_body, headers=config_headers)
    print("Config:", r2.json().get("entries", {}).get("api_url"))
except Exception as e:
    print(e)
