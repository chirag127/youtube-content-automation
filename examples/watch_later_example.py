"""Example: add search results to Watch Later."""

import os

from yt_automation import WatchLaterManager, build_driver

driver = build_driver(profile_dir=os.environ.get("CHROME_PROFILE"))
mgr = WatchLaterManager(driver)

count = mgr.from_search("Python tutorial", max_videos=10)
print(f"Added {count} videos to Watch Later")

driver.quit()
