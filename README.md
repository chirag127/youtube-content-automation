# YouTube Content Automation

[![Stars](https://img.shields.io/github/stars/chirag127/YouTube-Content-Automation-Python-Lib?style=flat-square)](https://github.com/chirag127/YouTube-Content-Automation-Python-Lib/stargazers)
[![MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://python.org)

Python library to automate YouTube actions — watch-later, subscriptions, comments, playback, reporting, search — via **Selenium element-based automation** and the **YouTube Data API v3**.

**Element/selector-driven. No pixel coordinates. No image matching.**

---

## Features

| Class | Actions |
|---|---|
| `WatchLaterManager` | Add search results / history / all-results to Watch Later |
| `SubscriptionManager` | List subscriptions, unsubscribe-all |
| `CommentBot` | Post comments on videos (from list or file) |
| `PlaybackController` | Watch-all playlist, skip-on-dislike, auto-advance |
| `ReportManager` | Report videos for spam / content violations |
| `SearchClient` | Search via Data API v3 (with key) or Selenium fallback |
| `TelegramGroupManager` | Leave Telegram groups via Telegram Web (unrelated to YouTube; separate module) |

---

## Install

```bash
pip install -e .
# or just install deps
pip install -r requirements.txt
```

Requires Python 3.10+, Google Chrome, and [ChromeDriver](https://chromedriver.chromium.org/) on PATH.

---

## Login setup

All YouTube automation requires a logged-in Chrome session.

1. Create (or locate) a Chrome profile that is logged into YouTube.
2. Set the `CHROME_PROFILE` environment variable to that profile path:

```bash
# Windows
set CHROME_PROFILE=C:\Users\YourName\AppData\Local\Google\Chrome\User Data\Profile 1

# Linux / macOS
export CHROME_PROFILE=~/.config/google-chrome/Profile\ 1
```

No passwords or cookies are stored in the code. The driver reads from your real Chrome profile.

Optionally set `YOUTUBE_API_KEY` for API-powered search:

```bash
set YOUTUBE_API_KEY=your_data_api_v3_key
```

---

## Usage

### Watch Later

```python
from yt_automation import WatchLaterManager, build_driver

driver = build_driver()
mgr = WatchLaterManager(driver)

# Add first 20 search results to Watch Later
mgr.from_search("Python tutorial", max_videos=20)

# Add from history
mgr.from_history(max_videos=10)

# Scroll + add all results
mgr.from_all_results("data structures", scroll_rounds=5, max_videos=50)

driver.quit()
```

### Subscriptions

```python
from yt_automation import SubscriptionManager, build_driver

driver = build_driver()
mgr = SubscriptionManager(driver)

names = mgr.list_subscriptions()
print(names)

mgr.unsubscribe_all(max_channels=100)
driver.quit()
```

### Comments

```python
from yt_automation import CommentBot, build_driver

driver = build_driver()
bot = CommentBot(driver)

bot.comment_on_video("https://youtube.com/watch?v=XYZ", "Great video!")
bot.comment_from_file("urls.txt", "Thanks for sharing!")
driver.quit()
```

### Search

```python
from yt_automation import SearchClient, build_driver

driver = build_driver(headless=True)
client = SearchClient(driver)

results = client.search("Selenium tutorial", max_results=10)
for r in results:
    print(r["title"], r["url"])
driver.quit()
```

### Reporting

```python
from yt_automation import ReportManager, build_driver
from yt_automation.reporting import REPORT_SPAM_TEXT

driver = build_driver()
mgr = ReportManager(driver)
mgr.report_video("https://youtube.com/watch?v=XYZ", reason=REPORT_SPAM_TEXT)
driver.quit()
```

### Playback

```python
from yt_automation import PlaybackController, build_driver

driver = build_driver()
ctrl = PlaybackController(driver)
ctrl.watch_all_in_watch_later(seconds_per_video=60, max_videos=20)
driver.quit()
```

---

## Run tests

```bash
pip install pytest
pytest
```

Tests mock the WebDriver — no real browser required to run the test suite.

---

## Selector maintenance

All CSS selectors and aria-labels are defined as named constants at the top of each module (e.g. `SEL_VIDEO_RENDERER`, `ARIA_SAVE_TO_WATCH_LATER`). When YouTube's DOM changes, update the constant in one place.

---

## Disclaimer

Automating YouTube may violate [YouTube's Terms of Service](https://www.youtube.com/t/terms). This library is intended for **personal and educational use only**. Use responsibly.

---

## License

MIT — see [LICENSE](LICENSE).
