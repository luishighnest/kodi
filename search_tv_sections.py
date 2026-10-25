import json
import re

sections_to_check = ['39390317', '37020661', '39532463', '39594846', '39555492']

with open(r'C:\Users\alecl\.gemini\antigravity\brain\1b2997f7-c241-424f-b3cf-836f849743b8\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        for sec in sections_to_check:
            if sec in line:
                print(f"Match for sec {sec} in line {idx}:")
                # print snippet
                pos = line.find(sec)
                start = max(0, pos - 100)
                end = min(len(line), pos + 1000)
                print(line[start:end])
                print("="*60)
