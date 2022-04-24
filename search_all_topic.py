import webbrowser
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


# syllabus = "Virtual Instrumentation,Graphical programming techniques,Data types,Advantage of Virtual Instrumentation techniques,Concept of WHILE,FOR loops,Arrays,Clusters , graphs,Structures,Case,Sequence , Formula nodes,Need of software based instruments , industrial automation"


# topic_list = syllabus.split(",")

with open(r"C:\Users\hp\OneDrive\Documents\GitHub\Auto-YouTube\movies.txt", "r") as f:
    topic_list = f.readlines()

# define the functiont to search all item the topic-list on youtube

topic_list_len = len(topic_list)

for topic in topic_list:
    topic = topic.strip()
    search_query = f'{topic}'
    search_url = f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%253D%253D"
    webbrowser.open(search_url)


if __name__ == "__main__":

    while True:

        if keyboard.is_pressed("ctrl + c"):

            for _ in range(1, topic_list_len):
                main()

                pyautogui.hotkey("ctrl", "tab")

                sleep(1)

            break
