from __future__ import annotations
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def _request_json(model: str, prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
        timeout=300,
    )
    response.raise_for_status()
    payload = response.json()
    return json.loads(payload["response"])


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
    return _request_json(model, prompt)


def generate_presentation_from_document(
    document_text: str,
    source_name: str,
    model: str,
    slide_count: int,
    document_skill: str,
    presentation_skill: str,
):
    # Yerel modellerin bağlamını gereksiz yere taşırmamak için aşırı büyük girdileri sınırla.
    # Kesme açıkça prompt'a bildirilir; kaynak dosyanın kendisi değiştirilmez.
    max_chars = 60_000
    truncated = len(document_text) > max_chars
    material = document_text[:max_chars]

    prompt = f"""
You are a document-to-presentation automation agent.

DOCUMENT SKILL:
---
{document_skill}
---

PRESENTATION SKILL:
---
{presentation_skill}
---

Source document: {source_name}
Requested slide count: {slide_count}
Input truncated because of local context limit: {str(truncated).lower()}

SOURCE MATERIAL:
---
{material}
--- END SOURCE MATERIAL ---

First analyze the source using the Document Skill, then create the presentation using the Presentation Skill.
Do not invent facts that are absent from the source. Preserve uncertainty and limitations.
For traceability, use the source filename in each relevant slide's sources array.

Return ONLY valid JSON with this exact top-level shape:
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
      "sources": ["{source_name}"]
    }}
  ]
}}
Do not wrap JSON in markdown fences.
"""
    return _request_json(model, prompt)
