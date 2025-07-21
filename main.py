import requests
import time
import hashlib

PUSHOVER_USER_KEY = "uuhb4p38no4o13os33uakfe5su3ed4"
PUSHOVER_API_TOKEN = "a5u6n3uhp19izybbhkojqkbfh25ff5"
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

URL = "https://skinbaron.de/en/csgo?plb=0.04&pub=71.5&sort=BP"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

seen_ids = set()

def send_notification(title, message):
    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message
    }
    requests.post(PUSHOVER_API_URL, data=payload)

def get_items():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Error fetching data")
        return []

    html = response.text
    items = []
    for part in html.split('<a href="/en/csgo/')[1:11]:
        try:
            link = part.split('"')[0]
            name_part = part.split('title="')[1].split('"')[0]
            item_id = hashlib.md5(link.encode()).hexdigest()
            items.append({"id": item_id, "name": name_part, "link": f"https://skinbaron.de/en/csgo/{link}"})
        except Exception:
            continue
    return items

def main_loop():
    global seen_ids
    while True:
        items = get_items()
        for item in items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                print(f"New item: {item['name']}")
                send_notification("New SkinBaron Item", f"{item['name']}
{item['link']}")
        time.sleep(1)

if __name__ == "__main__":
    main_loop()