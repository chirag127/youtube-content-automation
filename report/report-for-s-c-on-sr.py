# Physical: {X=1555,Y=399}; Scaled: {X=1244,Y=319}; Relative: {X=1555,Y=399}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #F9F9F6
# Physical: {X=1569,Y=608}; Scaled: {X=1255,Y=486}; Relative: {X=1569,Y=608}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #030303
# Physical: {X=719,Y=423}; Scaled: {X=575,Y=338}; Relative: {X=719,Y=423}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #CDCDCB
# Physical: {X=1183,Y=718}; Scaled: {X=946,Y=574}; Relative: {X=1183,Y=718}; Dpi: 120; Raw Dpi: 141; Dpi Ratio: 0.85; Screen Resolution: {Width=1920, Height=1080}; Pixel Color: #0067E7
import pyautogui
from time import sleep


def click(x, y):
    pyautogui.click(x, y)

# find C:\Users\hp\OneDrive\Documents\GitHub\Auto-YouTube\three-dot-to-report-s-c.png on the screen
# and return the coordinates of the three dots

def main():
    x_three_dots, y_three_dots = pyautogui.locateCenterOnScreen('three-dot-to-report-s-c.png',region = (0,88,1920,932))

    pyautogui.click(x_three_dots, y_three_dots)

    sleep(0.3)

    x_report_s_c, y_report_s_c = x_three_dots, y_three_dots + 209


    pyautogui.click(x_report_s_c, y_report_s_c)

    sleep(0.6)

    pyautogui.click(719,423)

    sleep(0.1)

    pyautogui.click(1183,718)

if __name__ == "__main__":

    print("Press 'alt+r' to start")
    
    while True:
        import keyboard
        if keyboard.is_pressed("alt+ r"):
            main()
        else:
            sleep(0.1)