import os, random

def pick_songs(song_dir, count):
    songs = [f for f in os.listdir(song_dir) if f.endswith(".mp3")]
    return random.sample(songs, min(count, len(songs)))
