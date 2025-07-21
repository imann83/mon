# SkinBaron Web Monitor (Pushover + Status Panel)

Monitors the latest 10 items on SkinBaron every second and sends instant Pushover notifications.

Also includes a web interface at `/status` to check activity and see if it's running.

## Setup

1. Upload files to GitHub
2. Create a Web Service on [Render.com](https://render.com)
3. Use the following run command:

```
python main.py
```

Service runs on port `10000` and exposes two endpoints:
- `/` – basic check
- `/status` – shows recent detected items