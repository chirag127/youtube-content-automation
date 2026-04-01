from time import sleep

import keyboard
import pyautogui

# Physical: {X=537,Y=218}; Scaled: {X=429,Y=174}; Relative: {X=-469,Y=-105}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #F1F1EF
# Physical: {X=643,Y=443}; Scaled: {X=514,Y=354}; Relative: {X=106,Y=227}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #F1F1EF
# Physical: {}; Scaled: {X=888,Y=461}; Relative: {X=442,Y=298}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #FF4E4F


def main():

    sleep(0.5)

    # Load the module
    pyautogui.rightClick()

    # Wait for the menu to appear
    sleep(0.1)

    # find current coordinates
    current_x, current_y = pyautogui.position()

    # Click on the leave group option
    pyautogui.click(current_x + 100, current_y + 225)

    # Wait for the menu to appear
    sleep(0.1)

    # click on the leave group option
    pyautogui.click(1111, 577)

    sleep(0.1)

    pyautogui.click(current_x, current_y)


if __name__ == "__main__":

    while True:

        if keyboard.is_pressed("ctrl+a"):

            main()

        else:

            sleep(0.1)
