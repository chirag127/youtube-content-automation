import webbrowser
from time import sleep

import pyautogui
import pyperclip

# Physical: {X=242,Y=492}


with open("Auto-comment\\url.txt", "r") as f:

    urls = f.readlines()


def main(url):

    webbrowser.open(url)

    sleep(5)

    pyautogui.press("pagedown")

    sleep(2)

    comment_corners = pyautogui.locateOnScreen("Auto-comment\\add_comment.png", grayscale=True)

    comment_x, comment_y = pyautogui.center(comment_corners)

    pyautogui.click(comment_x, comment_y)

    sleep(1)

    pyautogui.hotkey("ctrl", "v")

    sleep(1)

    pyautogui.hotkey("ctrl", "enter")

    sleep(0.01)

    print("Done for " + url)

    sleep(1)

    pyautogui.hotkey("ctrl", "w")


if __name__ == "__main__":

    pyperclip.copy("""Many Professors in the college are criticizing the event consisting of the ramp walk and the "story of the unsung India" they are saying that they had not seen this kind of event in any college where the students are not getting the chance to debate or group discussion which are actually performed by the students in the placement conducted by the companies. They also keep asking us that will the companies give us the jobs on the basis of the ramp walk or the knowledge of the unsung India or our nationalism. From the day the event of the "Bharat ki Ankahi Ansuni Kahaniya" as soon as the Professor of the college go outside the classroom many students starts the chanting political slogans like "bharat mata ki jai" in class disturbing the other students and making too much noise in the classroom and creating too much noise, disturbance and degrading the discipline and the atmosphere of the college.   """)

    for url in urls:

        main(url)
