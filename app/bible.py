import requests

def get_verses(topic, limit=12):
    verses = []
    page = 1

    while len(verses) < limit:
        r = requests.get(
            "https://bible-api.com/search",
            params={"query": topic, "limit": 12, "page": page}
        )
        data = r.json()
        verses.extend(v["text"] for v in data.get("verses", []))
        page += 1

        if not data.get("verses"):
            break

    return verses[:limit]
