import pygame
from base import *


class Game:
    def __init__(self):
        pygame.init()

        self.w, self.h = 500, 500
        self.size = (self.w, self.h)
        self.screen = pygame.display.set_mode(size)
        
        self.player = Player()
        self.object.append(self.player)

        self.keys_down = set()
        
    @property
    def get_size(self):
        return self.size

    def spawn_object(self, obj):
        self.objects.append(obj)

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def close(self):
        pygame.quit()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type is pygame.KEYDOWN:
                self.keys_down.add(event.key)
            elif event.type is pygame.KEYUP:
                self.keys_down.discard(event.key)

        self.handle_shortcuts()
        for obj in self.objects:
            obj.update()

    def handle_shortcuts(self):
        self.player.update_vector()
        


UGame = Game()
screen = pygame.display.set_mode(UGame.get_size())

while True:
    UGame.update()
    UGame.draw()
    
