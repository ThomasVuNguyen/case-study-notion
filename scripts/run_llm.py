import os
from google import genai
from google.genai import types

# Use gemini-2.5-pro to analyze the transcripts file
client = genai.Client()

prompt = """
You are an expert content strategist and marketing analyst studying the complete historical archive of official Notion YouTube videos.
I have compiled the transcripts and metadata of their 459 videos (under 10m in length) in chronologically ascending order.

Please critically analyze this archive and provide a comprehensive report describing:
1. THE OVERALL EVOLUTION: How has Notion's YouTube video content, messaging, and stylistic strategy evolved from their earliest days to the present? Break this down into distinct "Eras" or phases.
2. WHAT WORKED vs WHAT DIDN'T: Identify patterns in content types, series, or video formats that were heavily leaned into and expanded upon (successful) vs those that were tried and quickly abandoned or sidelined (unsuccessful).
3. THE LAUNCH PLAYBOOK: How does Notion use their YouTube channel during major feature launches (e.g., Notion AI, Projects, Calendar)? How do they build hype and educate users simultaneously?
4. CORE THEMES & AUDIENCES: Who are they talking to? How do they balance marketing to casual individuals/students versus B2B/Enterprise teams? 
5. ACTIONABLE TAKEAWAYS: Based strictly on Notion's historical data here, what are 5 bullet points of advice that a new SaaS startup should learn and adopt for their own YouTube strategy?

Use specific examples (referencing video titles or approximations of dates/topics from the provided transcripts) to back up your points.
"""

with open("all_transcripts.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Try with a basic generate content call, if we have ambient auth it should work
print("Starting analysis on 1.4MB of text...")
response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[prompt, text],
)

with open('strategy_analysis.md', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("Saved to strategy_analysis.md!")
