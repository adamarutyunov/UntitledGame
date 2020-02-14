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
PixelTimes = pygame.font.Font("fonts/PixelTimes.ttf", 50)

class Game:
    def __init__(self): 
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SRCALPHA)

        self.main_player = None
        self.main_drawer = None
        self.main_event_handler = None
        self.main_gui = None

        self.gui_state = False

        self.current_location = None
        
    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def get_location(self):
        return self.current_location

    def get_objects(self):
        return self.current_location.get_objects()

    def get_environment_objects(self):
        return self.current_location.get_environment_objects()

    def set_main_player(self, player):
        self.main_player = player

    def set_main_drawer(self, drawer):
        self.main_drawer = drawer

    def set_main_event_handler(self, event_handler):
        self.main_event_handler = event_handler

    def set_main_gui(self, gui):
        self.main_gui = gui

    def set_main_music_module(self, music_module):
        self.main_music_module = music_module

    def get_main_player(self):
        return self.main_player

    def get_main_drawer(self):
        return self.main_drawer

    def get_main_event_handler(self):
        return self.main_event_handler

    def get_main_gui(self):
        return self.main_gui

    def get_main_music_module(self):
        return self.main_music_module

    def load_location(self, location):
        self.current_location = location
        self.size = self.current_location.get_pixel_size()
        self.main_drawer.set_location()
        self.main_gui.add_info(location.name, 120)

    def spawn_object(self, obj):
        self.current_location.spawn_object(obj)

    def spawn_environment_object(self, obj):
        self.current_location.spawn_ecvironment_object(obj)

    def draw(self):
        self.main_drawer.draw()

    def set_gui_state(self, state):
        self.gui_state = state

    def toggle_gui(self):
        self.gui_state = not self.gui_state

    def get_gui_state(self):
        return self.gui_state

    def close(self):
        pygame.quit()

    def update(self):
        self.main_event_handler.process_events()
        self.main_drawer.update_drawdeltas()
        self.current_location.update()

    def delete_object(self, obj):
        self.current_location.remove_object(obj)

UGame = Game()
