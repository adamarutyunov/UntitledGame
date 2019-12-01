import pygame
from BaseModule import *


class Game:
    def __init__(self):
        self.w, self.h = 1000, 500
        self.size = (self.w, self.h)
        self.screen = pygame.display.set_mode(self.get_size())
        
        self.objects = []
        self.location = FirstLocation
        
    def get_size(self):
        return self.size

    def spawn_object(self, obj):
        self.objects.append(obj)

    def draw(self):
        self.screen.fill((0, 0, 0))
        location = self.location.draw()
        for obj in self.objects:
            obj.draw(self.screen)
        

        self.screen.blit(location, (0, 0))
        pygame.display.flip()

    def close(self):
        pygame.quit()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type is pygame.QUIT:
                self.close()
        for obj in self.objects:
            obj.update()
        

pygame.init()
clock = pygame.time.Clock()
fps = 60

UGame = Game()

player = Player(100, 100)
UGame.spawn_object(player)

while True:
    # Need to be vyneseno to dedicated EventHandler class
    keys = pygame.key.get_pressed()
    x_speed = 0
    y_speed = 0
    if keys[pygame.K_LEFT]:
        x_speed -= 1
    if keys[pygame.K_RIGHT]:
        x_speed += 1
    if keys[pygame.K_UP]:
        y_speed -= 1
    if keys[pygame.K_DOWN]:
        y_speed += 1
    player.x_delta = x_speed
    player.y_delta = y_speed
        
    UGame.update()
    UGame.draw()
    clock.tick(fps)

pygame.quit()
    
