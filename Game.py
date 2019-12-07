import pygame
from BaseModule import *
from Constants import *
from LocationModule import *
from TechnicalModule import *
from EntityModule import *


class Game:
    def __init__(self):
        self.objects = []
        self.environment_objects = []
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

        self.main_player = None
        self.main_drawer = None
        self.main_event_handler = None
        self.main_gui = None
        
    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def get_location(self):
        return self.location

    def get_objects(self):
        return self.objects

    def get_environment_objects(self):
        return self.environment_objects

    def set_main_player(self, player):
        self.main_player = player

    def set_main_drawer(self, drawer):
        self.main_drawer = drawer

    def set_main_event_handler(self, event_handler):
        self.main_event_handler = event_handler

    def set_main_gui(self, gui):
        self.main_gui = gui

    def get_main_player(self):
        return self.main_player

    def get_main_drawer(self):
        return self.main_drawer

    def get_main_event_handler(self):
        return self.main_event_handler

    def get_main_gui(self):
        return self.main_gui

    def load_location(self, location):
        self.location = location
        self.size = self.location.get_pixel_size()

    def spawn_object(self, obj):
        self.objects.append(obj)

    def spawn_environment_object(self, obj):
        self.environment_objects.append(obj)

    def draw(self):
        self.main_drawer.draw(self.objects)

    def close(self):
        pygame.quit()

    def update(self):
        self.main_event_handler.process_events()
        self.main_drawer.update_drawdeltas()
        for obj in self.objects:
            obj.update()

pygame.init()
clock = pygame.time.Clock()
fps = 60

UGame = Game()

FirstLocation = Location(UGame)
FirstLocation.load(f"{locations_path}/FirstLocation.loc")
UGame.load_location(FirstLocation)

GameDrawer = Drawer(UGame)
UGame.set_main_drawer(GameDrawer)

GameEventHandler = EventHandler(UGame)
UGame.set_main_event_handler(GameEventHandler)

GameGUI = GUI(UGame)
UGame.set_main_gui(GameGUI)

player = Player(100, 100, UGame)

UGame.set_main_player(player)
UGame.spawn_object(UGame.get_main_player())

while True:
    UGame.update()
    UGame.draw()
    pygame.event.pump()
    clock.tick(fps)
pygame.quit()
    
