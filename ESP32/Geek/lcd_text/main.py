import ST7789
from machine import Pin,PWM
import time
import gc
import colors

if __name__=='__main__':
    try:
        gc.enable()

        print("Instantiate ST7789 class - Started")
        LCD = ST7789.ST7789()
        print("Instantiate ST7789 class - Complete")

        LCD.fill(colors.BLACK)
        LCD.text("Hello World", 2, 2, colors.WHITE)
        LCD.text("HELLO WORLD", 2, 20, colors.CYAN)
        LCD.fill_rect(0, 40, 20, 20, colors.RED)

        print("Show - Started")
        LCD.show()
        print("Show - Complete")
        
        while(1):
            time.sleep(1)

        LCD.fill(LCD.black)
    except:
        print("An exception occurred")