import json
import urllib.request
import os
import re
import subprocess

urls = [
    "https://www.youtube.com/watch?v=GImxy01wW0o",
    "https://www.youtube.com/watch?v=mXQavYhN0Ak"
]

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

if not os.path.exists('images'):
    os.makedirs('images')

if not os.path.exists('yt'):
    os.makedirs('yt')

yt_dlp_cmd = "./yt-dlp"

for url in urls:
    print(f"Fetching metadata for {url}...")
    result = subprocess.run([yt_dlp_cmd, "-J", url], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to fetch metadata: {result.stderr}")
        continue
    
    v = json.loads(result.stdout)
    title = v.get('title', 'Unknown Title')
    vid_id = v.get('id')
    
    thumbs = v.get('thumbnails', [])
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
        
    md_filename = f"yt/{safe_title}.md"
    image_filename = f"images/{safe_title}.jpg"
    
    try:
        urllib.request.urlretrieve(thumb_url, image_filename)
        img_md = f"![{title}](../{image_filename})"
    except Exception as e:
        print(f"Failed to download {thumb_url}: {e}")
        img_md = f"*(Thumbnail failed to download)*"
        
    vtt_base = f"yt/{safe_title}"
    print(f"Downloading subtitles for {safe_title}...")
    subprocess.run([
        yt_dlp_cmd, "--write-auto-sub", "--write-sub", 
        "--sub-lang", "en", "--sub-format", "vtt", 
        "--skip-download", "-o", f"{vtt_base}.%(ext)s", url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    vtt_file = f"{vtt_base}.en.vtt"
    transcript_md = clean_vtt(vtt_file)
    
    if os.path.exists(vtt_file):
        os.remove(vtt_file)
        
    md_content = f"# {title}\n\n"
    md_content += f"**URL:** [{url}]({url})\n\n"
    md_content += f"{img_md}\n"
    md_content += f"{transcript_md}\n"
    
    with open(md_filename, 'w') as f:
        f.write(md_content)

print("Done.")
