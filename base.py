import pygame
from pygame.rect import Rect


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
        return self.bounds[2] + self.bounds[3]

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
        super().__init__(x, y, 30, 30, [0, 0], 1)
        self.x_delta = 0
        self.y_delta = 0

    def update_vector(self, xs, ys):
        delta = self.max_speed / 5 
        dxs = delta * xs
        dys = delta * ys
        self.accelerate(dxs, dys)

    def draw(self, screen):
        pygame.draw.circle(screen,
                           (255, 255, 255),
                           (self.left, self.top),
                           self.width)

    def update(self):
        self.update_vector(self.x_delta, self.y_delta)
        self.slow_down(0)
        self.slow_down(1)
        super().update()


class Location:
    pass


class Magic:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()  
