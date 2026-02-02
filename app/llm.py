import requests
from config import OLLAMA_URL, OLLAMA_MODEL

def generate_reflection(topic, verses):
    prompt = f"""Write a short Christian devotional reflection on {topic}.
Verses:
{chr(10).join(verses)}
"""

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return r.json()["response"]
