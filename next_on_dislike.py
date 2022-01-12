import pyautogui
import keyboard
from time import sleep


def main():

    if keyboard.is_pressed("n"):
        sleep(0.5)
        print("n is pressed")
        pyautogui.press("d")
        sleep(0.5)
        pyautogui.hotkey("shift", "n")


if __name__ == "__main__":

    while True:
        main()
        sleep(0.1)
