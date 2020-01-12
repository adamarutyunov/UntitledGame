import pygame

CELL_SIZE = 64
SCREEN_SIZE = (1920, 1080)

LEFT_DRAW_SIDE = SCREEN_SIZE[0] // 2 - 100
RIGHT_DRAW_SIDE = SCREEN_SIZE[0] // 2 + 100
TOP_DRAW_SIDE = SCREEN_SIZE[1] // 2 - 100
BOTTOM_DRAW_SIDE = SCREEN_SIZE[1] // 2 + 100

def DEF_NULL(*args, **kwargs):
    return

def load_image(path, color_key=None):
    image = pygame.image.load(path)
    if color_key is not None:
        if color_key == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
