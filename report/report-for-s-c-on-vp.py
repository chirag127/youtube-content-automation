import pyautogui
from time import sleep
import keyboard


def click(x, y):
    pyautogui.click(x, y)
    sleep(0.5)


def main():
    click(1243, 928)
    click(1327, 938)
    click(717, 245)
    click(795, 267)
    click(859, 468)
    click(1198, 946)
    click(1157, 785)
    sleep(0.3)
    click(1173, 703)


if __name__ == "__main__":

    while True:
        if keyboard.is_pressed("alt+ r"):
            main()
        else:
            sleep(0.1)
