import pygame
from pygame.rect import Rect
from LocationModule import *

class GameObject:
    def __init__(self, x, y, w, h, speed=[0, 0]):
        self.bounds = [x, y, w, h]
        self.speed = speed

    @property
    def left(self):
        return self.bounds[0]

    @property
    def right(self):
        return self.bounds[0] + self.bounds[2]

    @property
    def top(self):
        return self.bounds[1]

    @property
    def bottom(self):
        return self.bounds[1] + self.bounds[3]

    @property
    def width(self):
        return self.bounds[2]

    @property
    def height(self):
        return self.bounds[3]

    @property
    def center(self):
        return (self.centerx, self.centery)

    @property
    def centerx(self):
        return self.bounds[0] + self.bounds[2] / 2

    @property
    def centery(self):
        return self.bounds[1] + self.bounds[3] / 2

    def move(self, dx, dy):
        self.bounds[0] += dx
        self.bounds[1] += dy

    def update(self):
        self.move(*self.speed)


class Entity(GameObject):
    def __init__(self, x, y, w, h, speed, max_speed):
        super().__init__(x, y, w, h, speed)
        self.max_speed = max_speed

    def accelerate(self, dxs, dys):
        self.speed[0] += dxs
        self.speed[1] += dys
        
        if self.speed[0] > self.max_speed:
            self.speed[0] = self.max_speed
        if self.speed[0] < -self.max_speed:
            self.speed[0] = -self.max_speed
        if self.speed[1] > self.max_speed:
            self.speed[1] = self.max_speed
        if self.speed[1] < -self.max_speed:
            self.speed[1] = -self.max_speed

    def slow_down(self, k):
        delta = self.max_speed / 10
        if self.speed[k] > 0:
            self.speed[k] -= delta
            if self.speed[k] < 0:
                self.speed[k] = 0
        elif self.speed[k] < 0:
            self.speed[k] += delta
            if self.speed[k] > 0:
                self.speed[k] = 0
        

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 60, 60, [0, 0], 2)
        self.x_delta = 0
        self.y_delta = 0

    def deltax(self, dx):
        self.x_delta += dx

    def deltay(self, dy):
        self.y_delta += dy

    def update_vector(self, xs, ys):
        delta = self.max_speed / 5 
        dxs = delta * xs
        dys = delta * ys
        self.accelerate(dxs, dys)

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(screen,
                           (255, 255, 255),
                           (30, 30),
                           round(self.width / 2))

        return screen

    def update(self):
        self.update_vector(self.x_delta, self.y_delta)
        self.slow_down(0)
        self.slow_down(1)
        super().update()
        self.x_delta = 0
        self.y_delta = 0


class Drawer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.drawdelta_x = 0
        self.drawdelta_y = 0
        
        self.set_location()      

    def set_location(self):
        self.location = self.game.get_location()
        self.main_surface = pygame.Surface(self.location.get_pixel_size())

    def deltax(self, dx):
        self.drawdelta_x += dx

    def deltay(self, dy):
        self.drawdelta_y += dy

    def get_dd_x(self):
        return self.drawdelta_x

    def get_dd_y(self):
        return self.drawdelta_y

    def draw(self, objects):
        self.main_surface.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))
        self.main_surface.blit(self.location.draw(), (0, 0))
        for obj in objects:
            draw_surface = obj.draw()
            if draw_surface:
                self.main_surface.blit(draw_surface, (obj.left, obj.top))
        self.screen.blit(self.main_surface, (-self.drawdelta_x, -self.drawdelta_y))
        pygame.display.flip()

    def update_drawdeltas(self):
        player = self.game.get_main_player()
        
        if player.top - self.get_dd_y() < 50:
            self.deltay(player.top - self.get_dd_y() - 50)
        if player.bottom - self.get_dd_y() > 250:
            self.deltay(player.bottom - self.get_dd_y() - 250)
        if player.left - self.get_dd_x() < 50:
            self.deltax(player.left - self.get_dd_x() - 50)
        if player.right - self.get_dd_x() > 250:
            self.deltax(player.right - self.get_dd_x() - 250)



class EventHandler:
    def __init__(self, game):
        self.game = game

    def process_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.handle_events(events)
        self.handle_keys(keys)

    def handle_events(self, events):
        for event in events:
            if event.type is pygame.QUIT:
                self.game.close()

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.game.main_player.deltax(-1)
        if keys[pygame.K_RIGHT]:
            self.game.main_player.deltax(1)
        if keys[pygame.K_UP]:
            self.game.main_player.deltay(-1)
        if keys[pygame.K_DOWN]:
            self.game.main_player.deltay(1)
            
class Magic:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()  
