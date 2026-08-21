import base64
import requests
from Cryptodome.Cipher import AES

APP_PASSWORD = "oAR80SGuX3EEjUGFRwLFKBTiris="
def _generate_aes_key_iv(s: str):
    CHARSET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+!@#$%&="
    def u32(x): return x & 0xFFFFFFFF
    data = s.encode()
    n = len(data)
    u = 0x811c9dc5
    for b in data:
        u = u32((u ^ b) * 0x1000193)
    key = bytearray()
    for i in range(16):
        b = data[i % n]
        u = u32((u * 0x1f) + (i ^ b))
        key.append(CHARSET[u % len(CHARSET)])
    u = 0x811c832a
    for b in data:
        u = u32((u ^ b) * 0x1000193)
    iv = bytearray()
    idx = acc = 0
    while idx != 0x30:
        b = data[idx % n]
        u = u32((u * 0x1d) + (acc ^ b))
        iv.append(CHARSET[u % len(CHARSET)])
        idx += 3
        acc = u32(acc + 7)
    return bytes(key), bytes(iv)

try:
    r = requests.get("https://cdn-stream.top/events.json", headers={'User-Agent': 'Dalvik/2.1.0'})
    b64_data = r.json().get("data", "")
    print(f"Raw len: {len(b64_data)}")
    b64_data = b64_data.strip()
    b64_data = b64_data.strip().rstrip('=')
    b64_data += '=' * (-len(b64_data) % 4)
    try:
        ct = base64.urlsafe_b64decode(b64_data)
    except:
        ct = base64.b64decode(b64_data, validate=False)
    key, iv = _generate_aes_key_iv(APP_PASSWORD)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16:
        pt = pt[:-pad]
    print(pt[:100])
except Exception as e:
    print(e)
