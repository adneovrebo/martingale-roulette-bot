# This is a script for getting and testing the colors of pixel on the screen

import pyautogui

def get_color(x_pos, y_pos):
    screenshot = pyautogui.screenshot('settings/my_screenshot.png')
    RGBcolor = screenshot.getpixel((x_pos,y_pos))
    print(RGBcolor)

# How many times to you want to check that pixel?
for x in range(100):
    # Write the position of the pixel you want to check
    get_color(1000, 1000)

