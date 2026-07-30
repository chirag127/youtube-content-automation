"""Example: search YouTube and print results."""

from yt_automation import SearchClient, build_driver

driver = build_driver(headless=True)
client = SearchClient(driver)

# Uses Data API v3 if YOUTUBE_API_KEY is set, else Selenium fallback
results = client.search("Selenium Python tutorial", max_results=5)
for r in results:
    print(r["title"], "->", r["url"])

driver.quit()
