import json

with open(r'C:\Users\alecl\.gemini\antigravity\brain\1b2997f7-c241-424f-b3cf-836f849743b8\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '39555492' in line:
            obj = json.loads(line)
            c = obj.get('content', '')
            for l in c.splitlines():
                if any(k in l for k in ['universodream', 'xpcontrol', 'fullapple', 'myvisio', 'wuffy', 'colore', '39555492']):
                    print(l[:400])
