import json
import os
import re

json_file = 'search_1.json'
videos = []
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'entries' in data:
                    videos.extend(data['entries'])
                else:
                    videos.append(data)
            except json.JSONDecodeError:
                pass

notion_videos = []
for v in videos:
    if not v: continue
    uploader = v.get('uploader', '')
    duration = v.get('duration', 0)
    if 'Notion' in uploader and duration and duration < 600:
        notion_videos.append(v)
        
print(f"Found {len(notion_videos)} Notion videos under 10m.")
if notion_videos:
    for i, v in enumerate(notion_videos[:5]):
        print(f"{i+1}. {v.get('title')} ({v.get('duration')}s) - {v.get('uploader')}")

