import sys, os
sys.path.insert(0, r"C:\Users\alecl\Desktop\kodi_repo\plugin.video.kodiakso")
import default as kodi
import requests

try:
    print("Fetching events...")
    raw = kodi._szx_fetch("events.json")
    print(f"Raw len: {len(raw)}")
    
    if raw:
        dec = kodi._szx_decrypt(raw)
        if dec:
            print(f"Decrypted len: {len(dec)}")
            import json
            j = json.loads(dec.decode('utf-8', 'replace'))
            print(f"Parsed {len(j)} events")
            for ev in j[:3]:
                print(ev.get('title'), ev.get('eventInfo', {}).get('startTime'))
        else:
            print("Decryption failed!")
    else:
        print("Empty raw data!")
except Exception as e:
    print("Error:", e)
