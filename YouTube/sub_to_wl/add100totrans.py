import pyautogui
from functions import *

x_offset = -25

# Physical: {X=677,Y=445}
# Physical: {X=728,Y=454}
# Physical: {X=775,Y=546}
# defining the function to click on the 3 dots button at (x,y) coordinates = (680,480)

# Physical: {X=676,Y=444}
# Physical: {X=736,Y=464}
# Physical: {X=772,Y=542}

def click_on_three_dots_on_subcription():
    pyautogui.moveTo(680, 445)
    pyautogui.click()


# defining the function to click on the checkbox button to select all videos on the page at (x,y) coordinates = (730,490)
def click_on_checkbox_on_subcription():
    pyautogui.moveTo(730, 464)
    pyautogui.click()


# defining the function to click on the "Add to queue" button at (x,y) coordinates = (800,570)
def click_on_add_to_queue_on_subcription():
    pyautogui.moveTo(730, 542)
    pyautogui.click()

# click on expand at 1400,680


def click_on_expand_on_subcription():
    pyautogui.moveTo(1400, 680)
    pyautogui.click()

# defining the function to click on the save button at (x,y) coordinates = (1350,270)
# click on the save above the queue playlist created by the addtop100toE function


def click_on_the_save_above_the_queue_playlist_created_by_the_add100totrans_function():
    pyautogui.moveTo(1350, 270)
    pyautogui.click()

# defining the function to click on the trans playlist at (x,y) coordinates = (880,500)
# click on the trans playlist after click on the save button above the queue playlist created by the addtop100toE function


def click_on_trans_playlist_after_click_on_the_save_button_above_the_queue_playlist_created_by_the_add100totrans_function():
    pyautogui.moveTo(880, 500)
    pyautogui.click()


def main():

    sleep(10)

    click_on_three_dots_on_subcription()

    sleep(0.5)

    click_on_checkbox_on_subcription()

    sleep(0.5)

    click_on_add_to_queue_on_subcription()

    sleep(5)

    click_on_expand_on_subcription()

    sleep(1)

    click_on_the_save_above_the_queue_playlist_created_by_the_add100totrans_function()

    sleep(2)

    click_on_trans_playlist_after_click_on_the_save_button_above_the_queue_playlist_created_by_the_add100totrans_function()

    sleep(2)


if __name__ == '__main__':
    while True:

        wait_for_do_key()

        main()
