import pyautogui
import time
import keyboard


# write a code to watch all video in the watch later list of youtube videos
# and play the video when the user presses the space bar
# pause going to the next video when the user presses the x key
# and resume going to the next video when the user presses the z key


def main():

    print("main function executed")
    x = False
    key_to_pause_going_to_Next_video = "x"
    key_to_resume_going_to_Next_video = "z"
    key_to_pause_for_some_minutes_going_to_Next_video = "p"

    while True:

        for i in range(0, 100):

            if keyboard.is_pressed(key_to_pause_going_to_Next_video):

                x = False
                print("key_to_pause_going_to_Next_video is pressed")

            if keyboard.is_pressed(key_to_pause_for_some_minutes_going_to_Next_video):
                time_to_pause_for_some_minutes_going_to_Next_video = 100
                print("key_to_pause_for_some_minutes_going_to_Next_video is pressed")
                time.sleep(time_to_pause_for_some_minutes_going_to_Next_video)


            while not x:

                if keyboard.is_pressed(key_to_resume_going_to_Next_video):

                    x = True

                if keyboard.is_pressed(key_to_pause_going_to_Next_video):

                    x = False

                time.sleep(0.01)

            time.sleep(0.05)

        pyautogui.hotkey("shift", "n")

        print("next is pressed.")


if __name__ == "__main__":

    main()
