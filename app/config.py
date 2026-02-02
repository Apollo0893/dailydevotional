import os
from datetime import date

WEEK = (date.today().day - 1) // 7 + 1
TOPIC = os.getenv(f"WEEK_{WEEK}_TOPIC", "faith")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

INJECT_DIR = os.getenv("INJECT_DIR", "/inject")
SONGS_DIR = os.getenv("SONGS_DIR", "/songs")
SONGS_PER_DAY = int(os.getenv("SONGS_PER_DAY", 3))
VOICE = os.getenv("VOICE", "en-US-AriaNeural")
