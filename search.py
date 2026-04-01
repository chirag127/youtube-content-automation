with open(r"C:\Users\hp\OneDrive\Documents\GitHub\Auto-YouTube\movies.txt", "r") as f:
    topic_list = f.readlines()

import webbrowser
from time import sleep

import pyautogui

for topic in topic_list:

    url = f"https://www.youtube.com/results?search_query={topic}"

    webbrowser.open(url)

    sleep(2)

    pyautogui.hotkey("ctrl", "w")

    sleep(0.1)
