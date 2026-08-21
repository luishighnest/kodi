import requests
import base64
import hashlib
import hmac
import json
import time

SZX_BASE = 'https://cdn-stream.top/'
SZX_DIGEST = bytes.fromhex('1676ec7db4771b0d826d70369b579684b182d2c0133be041bdd55f5d6d79a98b')
SZX_SALT = b'sportzx/v2/prk'
SZX_UA = 'Dalvik/2.1.0 (Linux; Android 13)'

_SZX_SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]
_SZX_RSBOX = [0] * 256
for _szx_i, _szx_v in enumerate(_SZX_SBOX):
    _SZX_RSBOX[_szx_v] = _szx_i
_SZX_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d]

def _szx_xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11b
    return a & 0xff

def _szx_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _szx_xtime(a)
        b >>= 1
    return r

def _szx_expand_key(key):
    nk = len(key) // 4
    nr = nk + 6
    w = [list(key[4 * i:4 * i + 4]) for i in range(nk)]
    for i in range(nk, 4 * (nr + 1)):
        t = list(w[i - 1])
        if i % nk == 0:
            t = t[1:] + t[:1]
            t = [_SZX_SBOX[b] for b in t]
            t[0] ^= _SZX_RCON[i // nk - 1]
        elif nk > 6 and i % nk == 4:
            t = [_SZX_SBOX[b] for b in t]
        w.append([w[i - nk][j] ^ t[j] for j in range(4)])
    return w, nr

def _szx_round_key(s, w, rnd):
    for j in range(4):
        for k in range(4):
            s[4 * j + k] ^= w[4 * rnd + j][k]

def _szx_inv_shift_rows(s):
    for r in range(1, 4):
        row = [s[4 * c + r] for c in range(4)]
        row = row[-r:] + row[:-r]
        for c in range(4):
            s[4 * c + r] = row[c]
    return s

def _szx_inv_sub_bytes(s):
    return [_SZX_RSBOX[b] for b in s]

def _szx_inv_mix_columns(s):
    for c in range(4):
        o = 4 * c
        a0, a1, a2, a3 = s[o], s[o + 1], s[o + 2], s[o + 3]
        s[o] = _szx_mul(a0, 14) ^ _szx_mul(a1, 11) ^ _szx_mul(a2, 13) ^ _szx_mul(a3, 9)
        s[o + 1] = _szx_mul(a0, 9) ^ _szx_mul(a1, 14) ^ _szx_mul(a2, 11) ^ _szx_mul(a3, 13)
        s[o + 2] = _szx_mul(a0, 13) ^ _szx_mul(a1, 9) ^ _szx_mul(a2, 14) ^ _szx_mul(a3, 11)
        s[o + 3] = _szx_mul(a0, 11) ^ _szx_mul(a1, 13) ^ _szx_mul(a2, 9) ^ _szx_mul(a3, 14)
    return s

def _szx_decrypt_block(key, ct):
    w, nr = _szx_expand_key(key)
    s = list(ct)
    _szx_round_key(s, w, nr)
    for rnd in range(nr - 1, 0, -1):
        _szx_inv_shift_rows(s)
        s = _szx_inv_sub_bytes(s)
        _szx_round_key(s, w, rnd)
        _szx_inv_mix_columns(s)
    _szx_inv_shift_rows(s)
    s = _szx_inv_sub_bytes(s)
    _szx_round_key(s, w, 0)
    return bytes(s)

def _szx_aes_cbc_decrypt(key, iv, ct):
    pt = bytearray()
    prev = iv
    for off in range(0, len(ct), 16):
        blk = _szx_decrypt_block(key, ct[off:off + 16])
        pt += bytes(a ^ b for a, b in zip(blk, prev))
        prev = ct[off:off + 16]
    return bytes(pt)

def _szx_decrypt(data):
    try:
        b = data.rstrip('=')
        blob = base64.urlsafe_b64decode(b + '=' * (-len(b) % 4))
        if len(blob) < 49:
            print("Blob too short:", len(blob))
            return None
        if blob[0] not in (2, 3):
            print("Blob version not 2 or 3:", blob[0])
            return None
        iv = blob[1:17]
        tag = blob[-32:]
        ct = blob[17:-32]
        kd = hmac.new(SZX_SALT, SZX_DIGEST, hashlib.sha256).digest()
        enc = hmac.new(kd, b'enc', hashlib.sha256).digest()
        mac = hmac.new(kd, b'mac', hashlib.sha256).digest()
        computed_mac = hmac.new(mac, blob[:-32], hashlib.sha256).digest()
        if not hmac.compare_digest(computed_mac, tag):
            print("MAC mismatch! computed:", computed_mac.hex(), "tag:", tag.hex())
            return None
        pt = _szx_aes_cbc_decrypt(enc, iv, ct)
        pad = pt[-1] if pt else 0
        if 1 <= pad <= 16:
            pt = pt[:-pad]
        return bytes((((b << 5) | (b >> 3)) & 255) ^ SZX_DIGEST[i % 32] for i, b in enumerate(pt))
    except Exception as e:
        print("Decrypt exception:", e)
        return None

try:
    print("Fetching events...")
    r = requests.get(SZX_BASE + "events.json", headers={'User-Agent': SZX_UA})
    print("HTTP", r.status_code)
    raw = r.json().get('data', '')
    print(f"Raw len: {len(raw)}")
    
    if raw:
        dec = _szx_decrypt(raw)
        if dec:
            print(f"Decrypted len: {len(dec)}")
            j = json.loads(dec.decode('utf-8', 'replace'))
            print(f"Parsed {len(j)} categories")
            for c in j[:3]:
                print(c.get('title'))
        else:
            print("Decryption failed!")
    else:
        print("Empty raw data!")
except Exception as e:
    print("Error:", e)
