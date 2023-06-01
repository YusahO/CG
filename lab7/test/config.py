MAIN_COLOUR = "#999999"
ADD_COLOUR = "#EEEEEE"
CANVAS_COLOUR = "#FFFFFF"
DEFAULT_COLOUR = "#000000" 

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Frame sizes (relative).
BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

# Number of rows (some kind of grid) for data.
ROWS = 21

DATA_PART_WIDTH = 0.28 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * WINDOW_HEIGHT)
SLOT_HEIGHT = DATA_HEIGHT // ROWS

FIELD_PART_WIDTH = (1 - DATA_PART_WIDTH) - 4 * BORDERS_PART
FIELD_PART_HEIGHT = 1 - 2 * BORDERS_PART
FIELD_WIDTH = int(FIELD_PART_WIDTH * WINDOW_WIDTH)
FIELD_HEIGHT = int(FIELD_PART_HEIGHT * WINDOW_HEIGHT)
CANVAS_CENTER = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)

FIELD_BORDER_PART = 0.03


class Point:
    def __init__(self, x=0, y=0, colour="#FFFFFF"):
        self.x = x
        self.y = y
        self.colour = colour


MODES = ["Без задержки", "С задержкой"]

INFORMATION = '''\
Цвет по умолчанию: #000000 (черный)
Замер времени проводится...'''


LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3