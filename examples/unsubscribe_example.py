"""Example: unsubscribe from all channels."""

import os

from yt_automation import SubscriptionManager, build_driver

driver = build_driver(profile_dir=os.environ.get("CHROME_PROFILE"))
mgr = SubscriptionManager(driver)

names = mgr.list_subscriptions()
print(f"Found {len(names)} subscriptions")

count = mgr.unsubscribe_all(max_channels=50)
print(f"Unsubscribed from {count} channels")

driver.quit()
