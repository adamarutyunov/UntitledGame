import pygame
pygame.init()
pygame.display.set_mode((1, 1))

from BaseModule import *
from Constants import *
from LocationModule import *
from TechnicalModule import *
from EntityModule import *
from MagicModule import *


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

    def get_main_player(self):
        return self.main_player

    def get_main_drawer(self):
        return self.main_drawer

    def get_main_event_handler(self):
        return self.main_event_handler

    def get_main_gui(self):
        return self.main_gui

    def load_location(self, location):
        self.current_location = location
        self.size = self.current_location.get_pixel_size()

    def spawn_object(self, obj):
        self.current_location.spawn_object(obj)

    def spawn_environment_object(self, obj):
        self.current_location.spawn_ecvironment_object(obj)

    def draw(self):
        self.main_drawer.draw(self.current_location.get_objects())

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
        for obj in self.current_location.get_objects():
            obj.update()

clock = pygame.time.Clock()
UGame = Game()
pygame.display.update()

FirstLocation = Location(UGame)
FirstLocation.load(f"{locations_path}/FirstLocation.loc")
UGame.load_location(FirstLocation)


player = Player(100, 100, UGame)
zombie = Zombie(200, 100, UGame)

UGame.set_main_player(player)
UGame.spawn_object(UGame.get_main_player())
UGame.spawn_object(zombie)

GameDrawer = Drawer(UGame)
UGame.set_main_drawer(GameDrawer)

GameEventHandler = EventHandler(UGame)
UGame.set_main_event_handler(GameEventHandler)

GameGUI = GUI(UGame)
UGame.set_main_gui(GameGUI)

###
def damage(obj):
    obj.get_damage(20)

weapon = Weapon(200, damage)
player.get_item(weapon)

my_effect = DecreaseHealthEffect(600, 0.1)
my_effect.set_title("Отпирание прохода Линада Веабаба")
my_effect2 = IncreaseHealthEffect(300, 0.05)
player.affect_effect(my_effect)
player.affect_effect(my_effect2)
player.affect_effect(my_effect)
player.affect_effect(my_effect2)
player.affect_effect(my_effect)
player.affect_effect(my_effect2)
###

while True:
    try:
        UGame.get_main_gui().update()
        UGame.get_main_event_handler().process_events()
        if not UGame.get_gui_state():
            UGame.update()
        UGame.draw()
        pygame.event.pump()
        clock.tick(FPS)
    except pygame.error:
        break
pygame.quit()
    
