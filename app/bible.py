import requests

def get_verses(topic, limit=3):
    r = requests.get("https://bible-api.com/search", params={"query": topic, "limit": limit})
    data = r.json()
    return [v["text"] for v in data.get("verses", [])]
