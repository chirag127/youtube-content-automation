import pyautogui
from time import sleep
import webbrowser

# Physical: {X=1756,Y=260}
# Physical: {X=1444,Y=271}
# Physical: {X=1564,Y=411}


# define a function to click on the 3 dots on the search results
def main():
    image_path = "stowl\\i.png"
    image_3_dots = pyautogui.locateOnScreen(image_path, grayscale=True, confidence=0.9)
    x, y = pyautogui.center(image_3_dots)
    y = y - 20
    pyautogui.click(x, y)

    sleep(0.5)

    x_checkbox = x - 312
    y_checkbox = y - 11
    pyautogui.click(x_checkbox, y_checkbox)

    sleep(0.2)

    # define a function to click on the save to watch later button

    x_save_to_wl = x - 312

    y_save_to_wl = y + 151

    pyautogui.click(x_save_to_wl, y_save_to_wl)

    sleep(0.5)


with open("stowl\\topic.txt", "r") as f:

    topics = f.readlines()


if __name__ == "__main__":

    for topic in topics:

        webbrowser.open("https://www.youtube.com/results?search_query=" + topic)

        sleep(6)

        main()

        sleep(2)

        pyautogui.hotkey("ctrl", "w")

        sleep(1)
