import os, asyncio
from devotional import build_devotional
from songs import pick_songs
from audio import narrate, combine
from config import *

def run():
    text = build_devotional(TOPIC)

    # Get the INJECT_DIR from your config
    devotional_file = os.path.join(INJECT_DIR, 'daily_devotional.txt')
    
    # Write the devotional text to a file in the INJECT_DIR
    with open(devotional_file, 'w') as f:
        f.write(text)
    
    print(f"Devotional written to: {devotional_file}")
            
    narration = "/tmp/narration.mp3"
    asyncio.run(narrate(text, VOICE, narration))

    songs = pick_songs(SONGS_DIR, SONGS_PER_DAY)
    songs = [os.path.join(SONGS_DIR, s) for s in songs]

    output = os.path.join(INJECT_DIR, "daily_devotional.mp3")
    combine(narration, songs, output)
