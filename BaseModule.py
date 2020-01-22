import pygame


class GameObject:
    def __init__(self, x, y, w, h, speed=[0, 0]):
        self.bounds = [x, y, w, h]
        self.update_rect()
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
        self.update_rect()

    def set_x(self, x):
        self.bounds[0] = x
        self.update_rect()

    def set_y(self, y):
        self.bounds[1] = y
        self.update_rect()

    def update(self):
        self.move(*self.speed)

    def update_rect(self):
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)


class Item:
    def __init__(self, function=lambda: None, name=''):
        self.function = function
        self.name = name

        self.icon = None

    def use(self, obj):
        self.function(obj)

    def load_icon(self, icon):
        self.icon = icon

    def get_icon(self):
        return self.icon

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Weapon(Item):
    def __init__(self, attack_radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack_radius = attack_radius

    def get_attack_radius(self):
        return self.attack_radius

    def set_attack_radiue(self, attack_radius):
        self.attack_radius = attack_radius

    def use(self, obj):
        for e in obj.get_attacked_enemies(self.get_attack_radius()):
            super().use(e)
