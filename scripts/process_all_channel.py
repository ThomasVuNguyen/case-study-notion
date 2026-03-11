import json
import urllib.request
import os
import re
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

if os.path.exists('yt'):
    shutil.rmtree('yt')
if os.path.exists('images'):
    shutil.rmtree('images')

os.makedirs('yt')
os.makedirs('images')

yt_dlp_cmd = "./yt-dlp"

def clean_vtt(vtt_path):
    if not os.path.exists(vtt_path):
        return "\n*(Transcript not available)*\n"
    
    with open(vtt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line or line == 'WEBVTT' or '-->' in line or line.startswith('Language:') or line.startswith('Kind:'):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'Align:.*?$', '', line)
        line = line.strip()
        
        if not line: continue
        
        if not text_lines or text_lines[-1] != line:
            text_lines.append(line)
            
    if not text_lines:
        return "\n*(Transcript is empty)*\n"
        
    script = "\n## Transcript\n\n**[Voiceover]**\n\n\""
    
    words = ' '.join(text_lines).split()
    paragraph = []
    for w in words:
        paragraph.append(w)
        if len(paragraph) > 60:
            script += ' '.join(paragraph) + "\"\n\n\""
            paragraph = []
            
    if paragraph:
         script += ' '.join(paragraph) + "\"\n"
    else:
         script = script.rstrip('"\n') + "\n"
         
    return script

videos = []
with open('all_channel_videos.jsonl', 'r') as f:
    for line in f:
        try:
            d = json.loads(line)
            dur = d.get('duration')
            if dur is not None and dur < 600:
                videos.append(d)
        except Exception:
            pass

# The list is from newest to oldest. Reverse it to get oldest to newest.
videos.reverse()
print(f"Total videos to process: {len(videos)}")

def process_video(i, v):
    vid_id = v['id']
    url = f"https://www.youtube.com/watch?v={vid_id}"
    vtt_base = f"yt/temp_{vid_id}"
    
    # First get metadata
    cmd_meta = [
        yt_dlp_cmd, "--dump-json", "--no-warnings", url
    ]
    res_meta = subprocess.run(cmd_meta, capture_output=True, text=True)
    if res_meta.returncode != 0:
        return f"Failed metadata {vid_id}"
        
    try:
        data = json.loads(res_meta.stdout)
    except json.JSONDecodeError:
        return f"Failed parsed metadata {vid_id}"
        
    # Second, download subtitles
    cmd_sub = [
        yt_dlp_cmd, "--write-auto-sub", "--write-sub", 
        "--sub-lang", "en", "--sub-format", "vtt", 
        "--skip-download", "--no-warnings", 
        "-o", f"{vtt_base}.%(ext)s", url
    ]
    subprocess.run(cmd_sub, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    title = data.get('title', 'Unknown Title')
    upload_date = data.get('upload_date', 'Unknown')
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        
    thumbs = data.get('thumbnails', [])
    thumb_url = ''
    if thumbs:
        sorted_thumbs = sorted(thumbs, key=lambda x: x.get('width', 0) or 0)
        thumb_url = sorted_thumbs[-1].get('url')
    if not thumb_url:
        thumb_url = f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg"
        
    safe_title = re.sub(r'[^a-zA-Z0-9]', '-', title).strip('-').lower()
    safe_title = re.sub(r'-+', '-', safe_title)
    if not safe_title:
        safe_title = f"video_{vid_id}"
        
    prefix = f"{i+1:03d}"
    md_filename = f"yt/{prefix}-{safe_title}.md"
    image_filename = f"images/{prefix}-{safe_title}.jpg"
    
    try:
        urllib.request.urlretrieve(thumb_url, image_filename)
        img_md = f"![{title}](../{image_filename})"
    except Exception as e:
        img_md = f"*(Thumbnail failed to download)*"
        
    vtt_file = f"{vtt_base}.en.vtt"
    transcript_md = clean_vtt(vtt_file)
    
    if os.path.exists(vtt_file):
        os.remove(vtt_file)
        
    md_content = f"# {title}\n\n"
    md_content += f"**URL:** [{url}]({url})\n"
    md_content += f"**Date:** {upload_date}\n\n"
    md_content += f"{img_md}\n"
    md_content += f"{transcript_md}\n"
    
    with open(md_filename, 'w') as f:
        f.write(md_content)
        
    return f"Processed {prefix}-{safe_title}"

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(process_video, i, v): v for i, v in enumerate(videos)}
    count = 0
    for future in as_completed(futures):
        count += 1
        res = future.result()
        print(f"[{count}/{len(videos)}] {res}", flush=True)

print("Finished processing all 459 videos.")
