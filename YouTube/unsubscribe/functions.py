from time import sleep

import keyboard
import pyautogui


# defining the function to wait for user to press z key
def wait_for_do_key():
    while not keyboard.is_pressed("z"):
        sleep(0.1)


# defining the function to close the tab
def close_tab():
    pyautogui.hotkey("ctrl", "w")
