import os, asyncio
from devotional import build_devotional
from songs import pick_songs
from audio import narrate, combine
from config import *

def run():
    folder = "/inject"
    text = build_devotional(TOPIC)

    text_file = os.path.join(folder, "devotional.txt")
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
            
    narration = "/tmp/narration.mp3"
    asyncio.run(narrate(text, VOICE, narration))

    songs = pick_songs(SONGS_DIR, SONGS_PER_DAY)
    songs = [os.path.join(SONGS_DIR, s) for s in songs]

    output = os.path.join(INJECT_DIR, "daily_devotional.mp3")
    combine(narration, songs, output)
