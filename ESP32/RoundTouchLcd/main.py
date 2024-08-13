from window import *
from util import *
from display import Display
from spiderbot_window import SpiderBot
from welcome_window import WelcomeWindow
import time, esp32, machine
from machine import Pin


sleep_flag = False

def sleep_handler():
    global sleep_flag
    sleep_flag = True

def do_sleep():
    global sleep_flag
    print('Going to sleep')
    sleep_flag = False

class Failsafe:
    def __init__(self):
        print('Universal Robot Control')
        self.display = Display()
        print('Display initialized')

        self.display.screen.fill(Color.BACKGROUND.as565())
        print('Screen cleared')

        self.window_manager = WindowManager(self.display, sleep_handler)
        print('Window Manager initialized')

        self.main = SpiderBot(self.window_manager, self.display)
        self.robot_chain = WindowChain('Robots', [self.main.root_window, self.main.root_window])
        self.welcome = WelcomeWindow(self.window_manager, self.display, self.robot_chain)
        self.welcome.register_theme_callback(self.switched_theme)
        self.welcome_chain = WindowChain('Welcome', [self.welcome.window, self.welcome.theme_window])
        self.window_manager.push_window_chain(self.welcome_chain)

    def shutdown(self):
        self.window_manager.shutdown()

    def switched_theme(self):
        self.window_manager.pop_window()
        self.welcome = WelcomeWindow(self.window_manager, self.display, self.robot_chain)
        self.welcome.register_theme_callback(self.switched_theme)
        self.welcome_chain = WindowChain('Welcome', [self.welcome.theme_window, self.welcome.window])
        self.window_manager.push_window_chain(self.welcome_chain)


theme = Theme.read_from_file('modern_dark')
theme.apply()

failsafe = Failsafe()

try:
    while True:
        time.sleep_ms(100)
        if sleep_flag:
            do_sleep()
except KeyboardInterrupt:
    failsafe.shutdown()
