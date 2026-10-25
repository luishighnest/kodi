import json

# Let's inspect step 13 content in transcript_full.jsonl to find the exact details of the TV sections
with open(r'C:\Users\alecl\.gemini\antigravity\brain\1b2997f7-c241-424f-b3cf-836f849743b8\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i == 18 or i == 17:
            obj = json.loads(line)
            c = obj.get('content', '')
            for target in ['37020661', '39532463', '39555492', '39594846', 'TVFREE', 'iptv wuffy', 'IPTV colore']:
                if target in c:
                    idx = 0
                    while True:
                        pos = c.find(target, idx)
                        if pos == -1: break
                        s = max(0, pos - 200)
                        e = min(len(c), pos + 400)
                        print(f"--- MATCH {target} in step {i} ---")
                        print(c[s:e])
                        print("="*60)
                        idx = pos + len(target)
