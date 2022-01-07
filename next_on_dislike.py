import pyautogui
import keyboard
from time import sleep


def main():

    if keyboard.is_pressed("d"):
        print("d is pressed")
        sleep(0.01)
        pyautogui.hotkey("shift", "n")


if __name__ == "__main__":

    while True:
        main()
        sleep(0.1)
