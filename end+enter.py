import pyautogui
from time import sleep
import keyboard


def main():
    pyautogui.press("down")
    sleep(0.01)
    pyautogui.press("end")
    sleep(0.01)
    pyautogui.press("enter")
    sleep(0.01)


if __name__ == "__main__":

    key_to_start_adding_spaces = "z"
    key_to_stop_adding_spaces = "x"
    true_false = False

    while True:

        if keyboard.is_pressed(key_to_start_adding_spaces):
            true_false = True
            print("Started")
            sleep(0.01)
        if keyboard.is_pressed(key_to_stop_adding_spaces):
            true_false = False
            print("Stopped")
            sleep(0.01)
        if true_false:
            main()

        sleep(0.01)
