import pygame
import math
from Constants import *
from MagicModule import *


class GameObject:
    def __init__(self, x, y, w, h, game=None, speed=[0, 0]):
        self.bounds = [x, y, w, h]
        self.update_rect()
        self.speed = speed
        self.game = game

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


class Particle(GameObject):
    def __init__(self, x, y, w, h, time):
        super().__init__(x, y, w, h)
        self.pixmap_ticks = -1
        self.time = time
        self.ticks = 0

    def load_pixmaps(self, pixmaps):
        self.pixmaps = pixmaps

    def is_active(self):
        if self.ticks <= self.time:
            return True
        return False

    def draw(self):
        if self.is_active():
            return self.pixmaps[self.pixmap_ticks]
        return None

    def calculate_ticks(self):
        self.period = self.time // len(self.pixmaps)

    def update(self):
        self.pixmap_ticks = self.ticks // self.period
        if self.pixmap_ticks >= len(self.pixmaps):
            self.pixmap_ticks = len(self.pixmaps) - 1
        self.ticks += 1


class HealthUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье лечения")

        self.load_icon(load_image("textures/items/potions/health_up_potion.png"))

    def use(self, obj):
        effect = IncreaseHealthEffect(60, 0.5)
        obj.affect_effect(effect)
        obj.remove_item(self)


class IntelligenceUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье интеллекта")

        self.load_icon(load_image("textures/items/potions/intelligence_up_potion.png"))

    def use(self, obj):
        effect = IncreaseIntelligenceEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)


class StrengthUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье силы")

        self.load_icon(load_image("textures/items/potions/strength_up_potion.png"))

    def use(self, obj):
        effect = IncreaseStrengthEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)


class SpeedUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье скорости")

        self.load_icon(load_image("textures/items/potions/speed_up_potion.png"))

    def use(self, obj):
        effect = IncreaseSpeedEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)


class DamageParticle(Particle):
    def __init__(self):
        self.load_pixmaps([load_image("textures/damage/damage_1.png"),
                             load_image("textures/damage/damage_2.png"),
                             load_image("textures/damage/damage_3.png"),
                             load_image("textures/damage/damage_4.png")])

    def spawn(self, x, y, w, h, time):
        p = Particle(x, y, w, h, time)
        p.pixmaps = self.pixmaps
        p.calculate_ticks()
        return p


class ExplosionParticle(Particle):
    def __init__(self):
        self.load_pixmaps([load_image("textures/damage/boom_1.png"),
                             load_image("textures/damage/boom_2.png"),
                             load_image("textures/damage/boom_3.png"),
                             load_image("textures/damage/boom_4.png")])

    def spawn(self, x, y, w, h, time):
        p = Particle(x, y, w, h, time)
        p.pixmaps = self.pixmaps
        p.calculate_ticks()
        return p


DamageParticleInstance = DamageParticle()
ExplosionParticleInstance = ExplosionParticle()
