from __future__ import annotations
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def _request_json(model: str, prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
    "model": model,
    "prompt": prompt,
    "stream": False,
    "format": "json",
    "options": {
        "num_predict": 1200,
        "temperature": 0.2,
    },
},
        timeout=300,
    )
    response.raise_for_status()
    payload = response.json()
    return json.loads(payload["response"])


def generate_presentation(topic: str, model: str, slide_count: int, skill_text: str):
    prompt = f"""
You are a presentation automation agent.
IMPORTANT LANGUAGE RULE:
The entire presentation must be written in Turkish.
All titles, subtitles, slide titles, key messages, bullet points, visual directions, speaker notes, and all other generated text must be in Turkish.
Do not use English words or sentences unless they are technical terms that are commonly used in Turkish.
Use correct Turkish characters: ç, Ç, ğ, Ğ, ı, İ, ö, Ö, ş, Ş, ü, Ü.
Never translate Turkish source material into English.
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
IMPORTANT LANGUAGE RULE:
The entire presentation must be written in Turkish.
All titles, subtitles, slide titles, key messages, bullet points, visual directions, speaker notes, and all other generated text must be in Turkish.
Do not use English words or sentences unless they are technical terms that are commonly used in Turkish.
Use correct Turkish characters: ç, Ç, ğ, Ğ, ı, İ, ö, Ö, ş, Ş, ü, Ü.
Never translate Turkish source material into English.
If the source material is Turkish, preserve its language and terminology.
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
STRICT SLIDE COUNT RULE:
You MUST generate exactly {slide_count} slides in the "slides" array.
Do not generate fewer or more slides than requested.
Input truncated because of local context limit: {str(truncated).lower()}

SOURCE MATERIAL:
---
{material}
--- END SOURCE MATERIAL ---

Önce kaynak içeriği Document Skill kullanarak analiz et, ardından Presentation Skill kullanarak sunumu oluştur.
Kaynakta bulunmayan hiçbir bilgiyi uydurma. Belirsizlikleri ve sınırlamaları koru.
Kaynak izlenebilirliği için ilgili her slaytın sources alanında kaynak dosyanın adını kullan.
Sunumun kullanıcıya görünen TÜM içeriğini Türkçe üret. İngilizce başlık, açıklama, madde veya görsel yönlendirme üretme.

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
