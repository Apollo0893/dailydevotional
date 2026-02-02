import asyncio
import edge_tts
from pydub import AudioSegment

async def narrate(text, voice, out):
    tts = edge_tts.Communicate(text, voice)
    await tts.save(out)

def combine(narration, songs, output):
    audio = AudioSegment.from_mp3(narration)
    for song in songs:
        audio += AudioSegment.from_mp3(song)
    audio.export(output, format="mp3")
