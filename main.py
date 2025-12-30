import pyautogui
import time
time.sleep(3)
image_location1 = pyautogui.locateOnScreen('button.png',confidence=0.8)
print(image_location1)
if image_location1:
    x, y, width, height = image_location1
    pyautogui.click(x + width / 2, y + height / 2)
time.sleep(2)
image_location2 = pyautogui.locateOnScreen('sign_in.png',confidence=0.8)
if image_location2:
    x, y, width, height = image_location2
    pyautogui.click(x + width / 2, y + height / 2)
