import json

sections = ['37020661', '39532463', '39555492', '39594846']
# Search step 12 where the sections are described
with open(r'C:\Users\alecl\.gemini\antigravity\brain\1b2997f7-c241-424f-b3cf-836f849743b8\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i in [12, 13, 16, 17, 18]:
            obj = json.loads(line)
            c = obj.get('content', '')
            for s in sections:
                if s in c:
                    print(f"--- Section {s} in Step {i} ---")
                    # extract lines containing section s
                    for l in c.splitlines():
                        if s in l:
                            print(l[:300])
