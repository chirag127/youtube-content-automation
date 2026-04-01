from time import sleep

import keyboard
import pyautogui


# define function to wait for z key
def wait_for_do_key():
    while not keyboard.is_pressed("alt + d"):
        sleep(0.01)


# define function to close tab


def close_tab():
    pyautogui.hotkey("ctrl", "w")
