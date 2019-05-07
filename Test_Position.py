# This is a script for finding the position to click
# Screenshot pixel and clicking position are not the same!

from pynput.mouse import Button, Controller

mouse = Controller()

def click(x_pos, y_pos):
    mouse.position = (x_pos, y_pos)
    mouse.click(Button.left, 1)

# Change the x and y pos to check where you click
click(100,100)