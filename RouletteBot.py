# Ådne Øvrebø 2019 - post@adneovrebo.no

# Remark: This is a Martingale bettingstrategy Roulette Bot! Please feel free to modify after your wishes.
# The roulette bot is created to be working with the Immersive Live Casino, but can easly be modified to work elsewhere.

from pynput.mouse import Button, Controller
import time
import pyautogui
import os

class RouletteBot:
    def __init__(self):
        self.__mouse = Controller()    # Initializing controller for controlling mouse and clicks

        # Initializing variables
        self.__bet_executed = True
        self.__screenshot = None
        self.__running = True
        self.__bettingcolor = "red"     # The color you want to bet on
        self.__previuos_color = None
        self.__iterations = 0
        self.__times_lost = 0
        self.__times_won = 0
        self.__bettingvalue = None

        self.__voice_activated = True   # Variable for activating or deactivating voice feedback

        # All the position in pixels and colors in RGB to buttons, and status regions.
        self.__red_color = None         # Color used to detect red win
        self.__black_color = None       # Color used to detect black win
        self.__green_color = None       # Color used to detect a green
        self.__pos_result = None        # Position of the result popupbox.
        self.__pos_statusbar = None     # Position of the statusbar (time to bet or not)
        self.__pos_betblack = None      # Position of the button to bet black
        self.__pos_betred = None        # Position of the button to bet red
        self.__pos_double_bet = None    # Position of the button to double/repeat the bet

        self.settings() # Getting the settings for the spesific machine
        self.run()      # Running the RouletteBot

    # Taking a screenshot
    def screenshot(self):
        self.__screenshot = pyautogui.screenshot('settings/my_screenshot.png')

    # Finding the color of the ball
    def color_ball(self):
        pixel = self.__screenshot.getpixel((self.__pos_result[0], self.__pos_result[1]))
        rgb = [pixel[0], pixel[1], pixel[2]]

        if rgb == self.__black_color:
            self.__previuos_color = "black"
        elif rgb == self.__red_color:
            self.__previuos_color = "red"
        elif rgb == self.__green_color:
            self.__previuos_color = "green"

    # Checking if it's time to bet
    def betmode(self):
        color = self.__screenshot.getpixel((self.__pos_statusbar[0], self.__pos_statusbar[1]))
        if color[0] == 86 and color[1]==79 and color[2] == 79:
            self.__bet_executed = False
            return False
        return True

    # Method for adding a startbet
    def bet_startbet(self):
        if self.__bettingcolor == "red":
            pos = self.__pos_betred
        elif self.__bettingcolor == "black":
            pos = self.__pos_betblack
        else:
            raise ValueError("Color is not set right")

        self.__mouse.position = (int(pos[0] /2), int(pos[1] / 2))
        self.__mouse.click(Button.left, 1)

    # Method for doubling and repeating a bet.
    def double_bet(self):
        pos = self.__pos_double_bet
        self.__mouse.position = (int(pos[0] / 2), int(pos[1] / 2))
        self.__mouse.click(Button.left, 1)
        time.sleep(0.2)
        self.__mouse.click(Button.left, 1)

    # The method for running the bot, the idea behind the bot is this:
    #   - If the ball landing on the choosen color bet 1 chip on your color
    #   - If the ball landing on the NOT choosen color the bot will double your previous bet.
    def run(self):
        while self.__running:
            self.screenshot()
            self.color_ball()
            if self.betmode() and not self.__bet_executed:
                if self.__previuos_color == self.__bettingcolor or self.__iterations == 0:
                    self.bet_startbet()
                    say = "You won"
                    self.__times_lost = 0
                    self.__times_won += 1
                else:
                    self.double_bet()
                    say = "You lost"
                    self.__times_lost += 1
                self.__bet_executed = True
                self.__iterations += 1

                print(say + " | Looses: " + str(self.__times_lost) + " | Times won: " + str(self.__times_won) + " | Game number: " + str(self.__iterations))

                if self.__voice_activated:
                    os.system('say ' + say)

    # Method for importing the settings from the txt files.
    def settings(self):
        # Initializing the variables
        list_machines = []
        values = []

        # Getting the machines and numbers
        try:
            machinesfile = open("settings/computer_settings.txt","r")

            counter = 1
            for line in machinesfile:
                line = line.strip("\n")
                print(str(counter) + " : " + line[0:line.index(":")])
                list_machines.append(line[line.index(":")+1:])
                counter += 1
            index_machine = int(input("What machine are you on? Type the number of the machine then 'ENTER' :")) - 1

            src = list_machines[index_machine]
            settingfile = open(src, "r")

            # Getting the numbers from the file
            for line in settingfile:
                value = []
                line.strip("\n")
                line = line[line.index("=")+1:]
                value.append(int(line[0:line.index(",")]))
                while line.find(",") != -1:
                    line = line[line.index(",")+1:]
                    if line.find(",") == -1:
                        value.append(int(line.strip("\n")))
                    else:
                        value.append(int(line[0:line.find(",")]))
                values.append(value)

        except IOError as e:
            print("Error " + str(e))

        finally:
            #Always clouse the files when done
            machinesfile.close()
            settingfile.close()

        #Setting the values
        self.__red_color = values[0]
        self.__black_color = values[1]
        self.__green_color = values[2]
        self.__pos_result = values[3]
        self.__pos_statusbar = values[4]
        self.__pos_betblack = values[5]
        self.__pos_betred = values[6]
        self.__pos_double_bet = values[7]

        print("The setting have successfully been imported!")
        input("Press 'ENTER' to start the Roulette Bot by Ådne Øvrebø :")
        print("Session started!")
        print("")

# Running the program
if __name__ == '__main__':
    RouletteBot()
