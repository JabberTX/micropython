import ST7789
from machine import Pin, UART
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
            self.LCD.fill(color.BLACK)
            self.LCD.text("Waiting for GPS...", 2, 2, color.GREEN)
            self.LCD.show()
            print("Display Initialized")
        except Exception as e:
            print(f"An exception occurred: {e}")

    def update_display(self, latitude, lat_dir, longitude, lon_dir):
        try:
            self.LCD.fill(color.BLACK)  # Clear the screen before updating
            self.LCD.text(f"Lat: {latitude} {lat_dir}", 2, 2, color.GREEN)
            self.LCD.text(f"Lon: {longitude} {lon_dir}", 2, 20, color.BLUE)
            self.LCD.show()
            print("Display Updated with GPS Data")
        except Exception as e:
            print(f"Problem updating display: {e}")

    def shutdown(self):
        try:
            self.LCD.fill(color.PURPLE)
            self.LCD.show()
            print("Display filled with PURPLE")
        except Exception as e:
            print(f"Problem shutting down: {e}")

def parse_gps(data):
    # Print raw data for debugging
    print(f"Raw GPS Data: {data}")

    # Decode the data and split on commas
    data = data.decode('ascii').strip().split(',')

    # Data Def - $GPRMC,hhmmss.sss,A,lat,lat_dir,long,long_dir,speed,course,date,variation,mode*checksum
    # Check if the data is a GPRMC sentence
    
    if data[0] == '$GPGGA':
        latitude = data[2]
        lat_dir = data[3]
        longitude = data[4]
        lon_dir = data[5]
        
        return latitude, lat_dir, longitude, lon_dir
    else:
        print("Non-GPRMC data received")
        return None

try:

    # Initialize UART with the correct baud rate
    uart = UART(1, baudrate=9600, tx=Pin(43), rx=Pin(44), timeout=1000)
    time.sleep(2)  # Allow GPS to start

    while True:
        # Read a line from the UART
        data = uart.readline()
        if data:
            gps_data = parse_gps(data)
            if gps_data:
                latitude, lat_dir, longitude, lon_dir = gps_data
                display.update_display(latitude, lat_dir, longitude, lon_dir)
        
        time.sleep(1)  # Update every second

except KeyboardInterrupt:
    display.shutdown()
