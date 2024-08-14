import ST7789
from machine import Pin, PWM
import time
import gc
import color_lib as color

class Display:
    def __init__(self):
        try:
            gc.enable()
            print("GC Enabled")

            print("Instantiate ST7789 class - Started")
            self.LCD = ST7789.ST7789() 
            
            print("set window")
            self.LCD.set_window()
            print("set window complete")
            self.LCD.fill(color.BLACK)
            self.LCD.text("Hello World", 2, 2, color.GREEN)

            self.LCD.show()
            print("Display Updated")
        except Exception as e:
            print(f"An exception occurred: {e}")
            
    def shutdown(self):
        try:
            self.LCD.fill(color.PURPLE)
            print("Display filled with PURPLE")
        except Exception as e:
            print(f"Problem shutting down: {e}")

try:
    display = Display()
    while True:
        time.sleep_ms(100)
except KeyboardInterrupt:
    display.shutdown()