from __future__ import annotations
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_presentation(topic: str, model: str, slide_count: int, skill_text: str):
    prompt = f"""
You are a presentation automation agent.

Follow this skill specification:
--- SKILL ---
{skill_text}
--- END SKILL ---

Create a {slide_count}-slide presentation about:
{topic}

Return ONLY valid JSON with this shape:
{{
  "title": "...",
  "subtitle": "...",
  "audience": "...",
  "goal": "...",
  "slides": [
    {{
      "id": "01",
      "title": "...",
      "key_message": "...",
      "content": ["...", "..."],
      "visual": "...",
      "speaker_notes": "...",
      "sources": []
    }}
  ]
}}
Do not wrap JSON in markdown fences.
"""
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    return json.loads(payload["response"])
