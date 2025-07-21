# SkinBaron Monitor with Pushover

Monitors the last 10 items on SkinBaron and sends instant Pushover notifications when new items appear.

## Setup

1. Clone the repo
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the script:

```
python main.py
```

## Configuration

Set your `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` in `main.py`.

You can deploy this on Render.com or Replit for 24/7 monitoring.