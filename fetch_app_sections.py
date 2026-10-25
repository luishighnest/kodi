import urllib.request
import re

# AppCreator24 sections:
# ID 3634278
# Section 37020661 (TVFREE)
# Section 39532463 (iptv wuffy)
# Section 39555492 (IPTV colore)
# Section 39594846 (iptv colore test)

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}

for sec_id in [37020661, 39532463, 39555492, 39594846]:
    url = f"https://www.appcreator24.com/app/section.php?idapp=3634278&idsection={sec_id}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        print(f"=== SECTION {sec_id} (len {len(html)}) ===")
        # find scripts or links
        links = re.findall(r'https?://[^\s"\'\<\>]+', html)
        m3u_or_api = [l for l in links if any(k in l.lower() for k in ['.m3u', 'get.php', 'playlist', 'api', 'iptv-org', 'xpcontrol', 'fullapple'])]
        print("Special links:", set(m3u_or_api))
        # Look for var or fetch or m3u8
        for l in html.splitlines():
            if any(k in l.lower() for k in ['m3u', 'fetch(', 'http://', 'https://']) and len(l.strip()) < 300:
                print("  Line:", l.strip())
    except Exception as e:
        print(f"Error fetching section {sec_id}: {e}")
