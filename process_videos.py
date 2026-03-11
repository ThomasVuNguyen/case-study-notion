import json
import urllib.request
import os
import re

files = ['trailers.json', 'tutorials.json', 'intros.json', 'popular.json', 'videos.json']

videos = []
for f_name in files:
    if os.path.exists(f_name):
        with open(f_name, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    videos.append(data)
                except json.JSONDecodeError:
                    pass

selected_videos = []
seen_ids = set()
keywords = ['trailer', 'tutorial', 'intro', 'guide', 'how to', 'tour']

for v in videos:
    if not v: continue
    vid_id = v.get('id')
    uploader = v.get('uploader', '')
    
    # We only want Notion official videos
    if not uploader or 'Notion' not in uploader:
        continue
        
    if vid_id in seen_ids:
        continue
        
    title = v.get('title', '').lower()
    view_count = v.get('view_count', 0)
    
    # Must be a trailer/tutorial/intro by title, OR have >100k views
    is_keyword = any(k in title for k in keywords)
    is_popular = view_count and view_count > 100000
    
    if is_keyword or is_popular or True: 
        # Actually since ytsearch specifically fetched matching ones, we should just include all fetched from those small files
        pass

    seen_ids.add(vid_id)
    selected_videos.append(v)
    
    if len(selected_videos) >= 15: # Get up to 15 videos
        break

print(f"Found {len(selected_videos)} Notion videos.")

if not os.path.exists('images'):
    os.makedirs('images')

if not os.path.exists('yt'):
    os.makedirs('yt')

import subprocess

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
        # Remove timestamps format like <00:00:01.000><c> etc.
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'Align:.*?$', '', line)
        line = line.strip()
        
        if not line: continue
        
        # Auto-subs often repeat the same line as it builds up. 
        # Only add if it's not substantially similar to the previous line.
        if not text_lines or text_lines[-1] != line:
            text_lines.append(line)
            
    if not text_lines:
        return "\n*(Transcript is empty)*\n"
        
    script = "\n## Transcript\n\n**[Voiceover]**\n\n\""
    
    # Bundle text into paragraphs
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

# Create a markdown for each video
for i, v in enumerate(selected_videos):
    title = v.get('title', f'Unknown Title {i}')
    url = v.get('webpage_url', f"https://www.youtube.com/watch?v={v.get('id')}")
    
    thumbs = v.get('thumbnails', [])
    thumb_url = ''
    if thumbs:
        sorted_thumbs = sorted(thumbs, key=lambda x: x.get('width', 0) or 0)
        thumb_url = sorted_thumbs[-1].get('url')
    
    if not thumb_url:
        thumb_url = f"https://i.ytimg.com/vi/{v.get('id')}/maxresdefault.jpg"
        
    # Sanitize title for filename
    safe_title = re.sub(r'[^a-zA-Z0-9]', '-', title).strip('-').lower()
    safe_title = re.sub(r'-+', '-', safe_title)
    if not safe_title:
        safe_title = f"video_{i}"
        
    md_filename = f"yt/{safe_title}.md"
    image_filename = f"images/{safe_title}.jpg"
    
    # Download thumbnail
    try:
        urllib.request.urlretrieve(thumb_url, image_filename)
        img_md = f"![{title}](../{image_filename})"
    except Exception as e:
        print(f"Failed to download {thumb_url}: {e}")
        img_md = f"*(Thumbnail failed to download)*"
        
    # Download Subtitles
    vtt_base = f"yt/{safe_title}"
    print(f"Downloading subtitles for {safe_title}...")
    subprocess.run([
        "./yt-dlp", "--write-auto-sub", "--write-sub", 
        "--sub-lang", "en", "--sub-format", "vtt", 
        "--skip-download", "-o", f"{vtt_base}.%(ext)s", url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # yt-dlp might save as .en.vtt
    vtt_file = f"{vtt_base}.en.vtt"
    transcript_md = clean_vtt(vtt_file)
    
    # Clean up vtt files
    if os.path.exists(vtt_file):
        os.remove(vtt_file)
        
    md_content = f"# {title}\n\n"
    md_content += f"**URL:** [{url}]({url})\n\n"
    md_content += f"{img_md}\n"
    md_content += f"{transcript_md}\n"
    
    with open(md_filename, 'w') as f:
        f.write(md_content)

print("Successfully created markdown files with transcripts in the yt/ directory.")
