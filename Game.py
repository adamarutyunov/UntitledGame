import pygame
from BaseModule import *


class Game:
    def __init__(self):
        self.objects = []
        self.location = FirstLocation

        self.size = self.location.get_pixel_size()
        self.screen = pygame.display.set_mode((1000, 1000))

        self.drawer = Drawer(self.screen)
        self.drawer.set_location(self.location)
        
    def get_size(self):
        return self.size

    def spawn_object(self, obj):
        self.objects.append(obj)

    def draw(self):
        self.drawer.draw(self.objects)

    def close(self):
        pygame.quit()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type is pygame.QUIT:
                self.close()
        for obj in self.objects:
            obj.update()

        if player.top - self.drawer.drawdelta_y < 50:
            self.drawer.deltay(player.top - self.drawer.drawdelta_y - 50)
        if player.bottom - self.drawer.drawdelta_y > 250:
            self.drawer.deltay(player.bottom - self.drawer.drawdelta_y - 250)
        if player.left - self.drawer.drawdelta_x < 50:
            self.drawer.deltax(player.left - self.drawer.drawdelta_x - 50)
        if player.right - self.drawer.drawdelta_x > 250:
            self.drawer.deltax(player.right - self.drawer.drawdelta_x - 250)

pygame.init()
clock = pygame.time.Clock()
fps = 60

UGame = Game()

player = Player(100, 100)
UGame.spawn_object(player)
while True:
    # Need to be vyneseno to dedicated EventHandler class
    keys = pygame.key.get_pressed()
    #print(player.speed)
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
    pygame.event.pump()
    clock.tick(fps)

pygame.quit()
    
