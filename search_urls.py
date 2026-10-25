import json
import re

with open(r'C:\Users\alecl\.gemini\antigravity\brain\1b2997f7-c241-424f-b3cf-836f849743b8\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '37020661' in line or '39532463' in line or '39555492' in line or '39594846' in line:
            # check if there are raw codes or texts in this line
            m = re.findall(r'(https?://[^\s"\'\)\>\\]+)', line)
            m_filtered = [u for u in m if any(k in u for k in ['iptv-org', 'whitesea', 'xpcontrol', 'fullapple', 'wuffy', 'colore', 'tvfree', '.m3u'])]
            if m_filtered:
                print(f"Step {i} matching URLs ({len(m_filtered)}):")
                for u in set(m_filtered):
                    print(" ", u)
