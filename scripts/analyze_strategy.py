import os
import glob
from google import genai
from google.genai import types

# Find all markdown files in yt/
# Sort chronologically by the prefix (001 to 459)
files = sorted(glob.glob("yt/*.md"))

all_text = ""
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        all_text += f"\n--- File: {os.path.basename(file)} ---\n"
        all_text += f.read()

# Prompt for the LLM
prompt = """
You are an expert content strategist and marketing analyst studying the complete historical archive of official Notion YouTube videos.
I have compiled the transcripts and metadata of their 459 videos (under 10m in length) in chronologically ascending order (from oldest 001 to newest 459).

Please critically analyze this archive and provide a comprehensive report describing:
1. THE OVERALL EVOLUTION: How has Notion's YouTube video content, messaging, and stylistic strategy evolved from their earliest days to the present? Break this down into distinct "Eras" or phases.
2. WHAT WORKED vs WHAT DIDN'T: Identify patterns in content types, series, or video formats that were heavily leaned into and expanded upon (successful) vs those that were tried and quickly abandoned or sidelined (unsuccessful).
3. THE LAUNCH PLAYBOOK: How does Notion use their YouTube channel during major feature launches (e.g., Notion AI, Projects, Calendar)? How do they build hype and educate users simultaneously?
4. CORE THEMES & AUDIENCES: Who are they talking to? How do they balance marketing to casual individuals/students versus B2B/Enterprise teams? 
5. ACTIONABLE TAKEAWAYS: Based strictly on Notion's historical data here, what are 5 bullet points of advice that a new SaaS startup should learn and adopt for their own YouTube strategy?

Use specific examples (referencing video titles or approximations of dates/topics from the provided transcripts) to back up your points.
"""

# Call the Gemini API.
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment.")
    exit(1)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[prompt, all_text],
)

with open('strategy_analysis.md', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("Analysis complete. Saved to strategy_analysis.md")
