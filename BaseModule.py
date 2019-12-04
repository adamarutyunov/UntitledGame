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



class Drawer:
    def __init__(self, screen):
        self.screen = screen

        self.drawdelta_x = 0
        self.drawdelta_y = 0
        
        self.location = None        
        self.main_surface = None

    def set_location(self, location):
        self.location = location
        self.main_surface = pygame.Surface(self.location.get_pixel_size())

    def deltax(self, dx):
        self.drawdelta_x += dx

    def deltay(self, dy):
        self.drawdelta_y += dy

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


class Magic:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()  
