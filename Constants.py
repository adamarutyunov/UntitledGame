import pygame
from math import ceil

FPS = 60

CELL_SIZE = 64
SCREEN_SIZE = (1920, 1080)

LABEL_COLOR = (186, 111, 0)
GRAY_LABEL_COLOR = (230, 230, 160)
GREEN_LABEL_COLOR = (60, 255, 60)
RED_LABEL_COLOR = (255, 60, 60)

BORDER_COLOR = (255, 216, 0)

INVENTORY_POS = (30, 625)
EFFECTS_WINDOW_POS = (30, 170)
ITEM_CELL_POS = (30, 975)
MAGIC_CELL_POS = (124, 975)
ATTRIBUTE_BAR_POS = (30, 30)
CHARACTERISTICS_WINDOW_POS = (755, 804)


LEFT_DRAW_SIDE = SCREEN_SIZE[0] // 2 - 100
RIGHT_DRAW_SIDE = SCREEN_SIZE[0] // 2 + 100
TOP_DRAW_SIDE = SCREEN_SIZE[1] // 2 - 100
BOTTOM_DRAW_SIDE = SCREEN_SIZE[1] // 2 + 100

def DEF_NULL(*args, **kwargs):
    return

def load_image(path, color_key=None):
    image = pygame.image.load(path)
    image = image.convert_alpha()
    return image

MagicFont = pygame.font.Font("fonts/Magic.ttf", 23)
