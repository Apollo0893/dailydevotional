from bible import get_verses
from llm import generate_reflection

def build_devotional(topic):
    verses = get_verses(topic, 12)
    reflection = generate_reflection(topic, verses)
    return "\n".join(verses) + "\n\n" + reflection
