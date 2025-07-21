import requests
import time
import hashlib
import threading
from flask import Flask
import os

PUSHOVER_USER_KEY = "uuhb4p38no4o13os33uakfe5su3ed4"
PUSHOVER_API_TOKEN = "a5u6n3uhp19izybbhkojqkbfh25ff5"
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

URL = "https://skinbaron.de/en/csgo?plb=0.04&pub=71.5&sort=BP"
HEADERS = {"User-Agent": "Mozilla/5.0"}

seen_ids = set()
app = Flask(__name__)
status_data = {"last_check": "Never", "new_items": []}

def send_notification(title, message):
    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message
    }
    try:
        requests.post(PUSHOVER_API_URL, data=payload)
    except:
        pass

def get_items():
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code != 200:
            return []
        html = response.text
        items = []
        for part in html.split('<a href="/en/csgo/')[1:11]:
            try:
                link = part.split('"')[0]
                name_part = part.split('title="')[1].split('"')[0]
                item_id = hashlib.md5(link.encode()).hexdigest()
                items.append({
                    "id": item_id,
                    "name": name_part,
                    "link": f"https://skinbaron.de/en/csgo/{link}"
                })
            except:
                continue
        return items
    except:
        return []

def monitor_loop():
    global status_data
    while True:
        items = get_items()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        status_data["last_check"] = now
        for item in items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                status_data["new_items"].append({"time": now, "name": item["name"], "link": item["link"]})
                send_notification("New SkinBaron Item", f"{item['name']}\n{item['link']}")
        time.sleep(1)

@app.route("/")
def home():
    return "<h1>SkinBaron Monitor is Running ✅</h1><p>Check /status for latest activity.</p>"

@app.route("/status")
def status():
    html = f"<h2>Last Check: {status_data['last_check']}</h2><ul>"
    for item in status_data["new_items"][-10:][::-1]:
        html += f"<li><b>{item['time']}</b>: <a href='{item['link']}' target='_blank'>{item['name']}</a></li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    threading.Thread(target=monitor_loop, daemon=True).start()
    send_notification("SkinBaron Monitor Started ✅", "Monitoring is now running!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))