import pyautogui
from time import sleep
import keyboard

# Physical: {X=1756,Y=260}
# Physical: {X=1444,Y=271}
# Physical: {X=1564,Y=411}


# define a function to click on the 3 dots on the search results
def click_3_dots():
    pyautogui.click(1756, 260)

# define a function to click on the checkbox on the search results to select all the videos.


def click_checkbox():
    pyautogui.click(1444, 271)

# define a function to click on the save to watch later button


def click_save_to_wl():
    pyautogui.click(1564, 411)


def main():

    click_3_dots()
    sleep(0.5)
    click_checkbox()
    sleep(0.5)
    click_save_to_wl()


if __name__ == '__main__':

    while True:

        if keyboard.is_pressed('ctrl + c'):
            for i in range(1, 10):

                main()

                pyautogui.hotkey('ctrl', 'tab')

                sleep(1)
