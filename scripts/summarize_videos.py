import glob

files = sorted(glob.glob("yt/*.md"))
summary = []

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split('\n')
    title = ""
    date = ""
    transcript_snippet = ""
    
    in_transcript = False
    for line in lines:
        if line.startswith("# "):
            if not title:
                title = line[2:].strip()
        elif line.startswith("**Date:**"):
            date = line.split("**Date:**")[1].strip()
        elif line.startswith("**[Voiceover]**") or line.startswith("*(Transcript not available)*"):
            in_transcript = True
        elif in_transcript and line.strip() and not line.startswith("!["):
            if "not available" in line:
                transcript_snippet = "N/A"
            else:
                transcript_snippet += line + " "
                if len(transcript_snippet) > 200:
                    transcript_snippet = transcript_snippet[:200] + "..."
                    break

    summary.append(f"{date} | {title} | {transcript_snippet}")

with open("video_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(summary))

print("Summary written to video_summary.txt")
