# color_lib.py

# Define colors in RGB565 format
RED = bytearray([0xF8, 0x00])
GREEN = bytearray([0x07, 0xE0])
BLUE = bytearray([0x00, 0x1F])
WHITE = bytearray([0xFF, 0xFF])
BLACK = bytearray([0x00, 0x00])
YELLOW = bytearray([0xFF, 0xE0])
CYAN = bytearray([0x00, 0xFF])
MAGENTA = bytearray([0xF8, 0x1F])
GRAY = bytearray([0x7F, 0x7F])
DARK_RED = bytearray([0x80, 0x00])
DARK_GREEN = bytearray([0x00, 0x40])
DARK_BLUE = bytearray([0x00, 0x10])
ORANGE = bytearray([0xFC, 0x00])

# Dictionary to map color names to bytearrays
color_map = {
    'red': RED,
    'green': GREEN,
    'blue': BLUE,
    'white': WHITE,
    'black': BLACK,
    'yellow': YELLOW,
    'cyan': CYAN,
    'magenta': MAGENTA,
    'gray': GRAY,
    'dark_red': DARK_RED,
    'dark_green': DARK_GREEN,
    'dark_blue': DARK_BLUE,
    'orange': ORANGE
}

def get_color(name):
    """Get color bytearray by name."""
    return color_map.get(name.lower(), BLACK)  # Default to black if color not found
