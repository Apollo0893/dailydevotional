import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

from config import MIN_WORDS

def generate_reflection(topic, verses):
    prompt = f"""
Write a Christian devotional reflection on the topic "{topic}".

Requirements:
- At least {MIN_WORDS} words
- Scripture-centered
- Pastoral tone
- Designed for spoken audio
- No song lyrics
- Flowing narrative, not bullet points

Verses:
{chr(10).join(verses)}
"""

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
    )
    return r.json()["response"]

