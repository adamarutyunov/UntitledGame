import pygame


class GameObject:
    def __init__(self, x, y, w, h, speed=[0, 0]):
        self.bounds = [x, y, w, h]
        self.rect = pygame.Rect(x, y, w, h)
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
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    def update(self):
        self.move(*self.speed)

