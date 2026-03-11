import json
import urllib.request
import os
import re
import subprocess

queries = [
    "ytsearch300:Notion",
    "ytsearch300:Notion tutorial",
    "ytsearch300:Notion guide",
    "ytsearch300:Notion release",
    "ytsearch300:Notion update"
]

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

videos_data = {}

for q in queries:
    print(f"Executing {q}...")
    result = subprocess.run([yt_dlp_cmd, "-J", "--flat-playlist", q], capture_output=True, text=True)
    if result.returncode != 0:
        continue
    for line in result.stdout.split('\n'):
        if not line.strip(): continue
        try:
            data = json.loads(line)
            entries = data.get('entries', [])
            if not entries: entries = [data]
            for v in entries:
                if not v: continue
                vid_id = v.get('id')
                uploader = v.get('uploader', '')
                duration = v.get('duration', 0)
                # Keep only official Notion channel, under 10 mins
                if uploader == 'Notion' and duration and duration < 600:
                    if vid_id not in videos_data:
                        videos_data[vid_id] = v
        except Exception:
            pass

# Now we need full info for these selected ones because flat-playlist might not have upload_date
# Wait, let's just use url to yt-dlp again to get upload_date and transcripts
selected_videos = list(videos_data.values())
print(f"Found {len(selected_videos)} unique Notion videos under 10m.")

full_videos = []
for v in selected_videos:
    vid_id = v.get('id')
    url = f"https://www.youtube.com/watch?v={vid_id}"
    print(f"Fetching full metadata for {vid_id}...")
    result = subprocess.run([yt_dlp_cmd, "-J", "--no-warnings", url], capture_output=True, text=True)
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            if data:
                full_videos.append(data)
        except Exception:
            pass

# Sort by upload_date
full_videos.sort(key=lambda x: x.get('upload_date', '99999999'))

print(f"Sorted {len(full_videos)} videos from oldest to newest.")

if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('yt'):
    os.makedirs('yt')

for i, v in enumerate(full_videos):
    title = v.get('title', 'Unknown Title')
    url = v.get('webpage_url', f"https://www.youtube.com/watch?v={v.get('id')}")
    upload_date = v.get('upload_date', 'Unknown')
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        
    thumbs = v.get('thumbnails', [])
    thumb_url = ''
    if thumbs:
        sorted_thumbs = sorted(thumbs, key=lambda x: x.get('width', 0) or 0)
        thumb_url = sorted_thumbs[-1].get('url')
    if not thumb_url:
        thumb_url = f"https://i.ytimg.com/vi/{v.get('id')}/maxresdefault.jpg"
        
    safe_title = re.sub(r'[^a-zA-Z0-9]', '-', title).strip('-').lower()
    safe_title = re.sub(r'-+', '-', safe_title)
    if not safe_title:
        safe_title = f"video_{i}"
        
    # Prepend index so files order oldest to newest in the folder
    prefix = f"{i+1:03d}"
    md_filename = f"yt/{prefix}-{safe_title}.md"
    image_filename = f"images/{prefix}-{safe_title}.jpg"
    
    try:
        urllib.request.urlretrieve(thumb_url, image_filename)
        img_md = f"![{title}](../{image_filename})"
    except Exception as e:
        img_md = f"*(Thumbnail failed to download)*"
        
    vtt_base = f"yt/{prefix}-{safe_title}"
    print(f"({i+1}/{len(full_videos)}) Processing {safe_title}...")
    subprocess.run([
        yt_dlp_cmd, "--write-auto-sub", "--write-sub", 
        "--sub-lang", "en", "--sub-format", "vtt", 
        "--skip-download", "--no-warnings", "-o", f"{vtt_base}.%(ext)s", url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
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

print("Done. All videos downloaded, sorted, and formatted in yt/")
