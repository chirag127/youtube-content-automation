"""Example: post a comment on a list of videos."""

import os

from yt_automation import CommentBot, build_driver

COMMENT = "Great video, thanks for sharing!"
URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
]

driver = build_driver(profile_dir=os.environ.get("CHROME_PROFILE"))
bot = CommentBot(driver)

results = bot.comment_on_videos(URLS, COMMENT)
for url, ok in results.items():
    print(f"{'OK' if ok else 'FAIL'} {url}")

driver.quit()
