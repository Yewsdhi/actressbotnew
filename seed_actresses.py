#!/usr/bin/env python3
"""Import up to 500 Indian film actresses with real Wikipedia thumbnail URLs.

Run once after setting MONGO_URI and DB_NAME:
    python seed_actresses.py

Uses the same collection/schema as the bot: anime_characters with
img_url, name, anime, rarity, and id fields. Existing names are not duplicated.
"""
import os
import sys
import time
import urllib.parse
import urllib.request
import json
from pymongo import MongoClient

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "ActressArenaGoldSeeder/1.0 (Telegram game database setup)"
TARGET = 500
RARITIES = ["⚪ Common", "🟣 Rare", "🟢 Medium", "🟡 Legendary", "💮 Special Edition"]

def api(params):
    params = dict(params)
    params.setdefault("format", "json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def get_titles():
    data = api({"action": "parse", "page": "List_of_Indian_film_actresses", "prop": "links"})
    titles = []
    seen = set()
    for link in data.get("parse", {}).get("links", []):
        title = link.get("title", "").strip()
        if link.get("ns") == 0 and title and not any(x in title for x in [":", "#"]):
            if title not in seen:
                seen.add(title)
                titles.append(title)
    return titles

def get_pages_with_images(titles):
    results = []
    for start in range(0, len(titles), 40):
        batch = titles[start:start + 40]
        data = api({
            "action": "query", "prop": "pageimages|info", "inprop": "url",
            "piprop": "thumbnail", "pithumbsize": 900,
            "titles": "|".join(batch),
        })
        for page in data.get("query", {}).get("pages", {}).values():
            thumb = page.get("thumbnail", {}).get("source")
            title = page.get("title", "").replace("_", " ").strip()
            if thumb and title and not page.get("missing"):
                results.append({"name": title, "img_url": thumb,
                                "profile_url": page.get("fullurl", "")})
        time.sleep(0.15)
    return results

def main():
    mongo_uri = os.environ.get("MONGO_URI", "").strip()
    db_name = os.environ.get("DB_NAME", "waifu_bot").strip()
    if not mongo_uri:
        sys.exit("ERROR: Set MONGO_URI (and optionally DB_NAME) before running.")

    print("Fetching Indian film actress names from Wikipedia...")
    titles = get_titles()
    print(f"Found {len(titles)} linked names. Resolving image thumbnails...")
    candidates = get_pages_with_images(titles)

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=15000)
    client.admin.command("ping")
    collection = client[db_name]["anime_characters"]
    existing = {d.get("name", "").casefold() for d in collection.find({}, {"name": 1})}
    next_id = 1
    for doc in collection.find({}, {"id": 1}):
        try:
            next_id = max(next_id, int(doc.get("id", 0)) + 1)
        except (TypeError, ValueError):
            pass

    docs = []
    for item in candidates:
        if item["name"].casefold() in existing:
            continue
        n = len(docs)
        docs.append({
            "id": str(next_id + n).zfill(4),
            "name": item["name"],
            "anime": "Indian Cinema",
            "rarity": RARITIES[min(4, (n % 100) // 20)],
            "img_url": item["img_url"],
            "profile_url": item["profile_url"],
        })
        if len(docs) == TARGET:
            break

    if len(docs) < TARGET:
        print(f"Only {len(docs)} new entries with image thumbnails are available; no partial import performed.")
        print("Add more verified actress pages/images or remove existing duplicates, then rerun.")
        sys.exit(2)

    result = collection.insert_many(docs, ordered=False)
    print(f"SUCCESS: inserted {len(result.inserted_ids)} actresses into {db_name}.anime_characters")
    print("Restart the bot after import. The /guess drop system will use this collection.")
    client.close()

if __name__ == "__main__":
    main()
