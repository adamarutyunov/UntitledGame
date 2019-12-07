import pygame
from BaseModule import GameObject


class Entity(GameObject):
    def __init__(self, x, y, w, h, speed, game):
        super().__init__(x, y, w, h, speed)
        self.game = game
        self.max_speed = 0
        self.max_health = 0
        self.max_mana = 0

        self.health = 0
        self.mana = 0

    def set_max_speed(self, speed):
        self.max_speed = speed

    def set_max_health(self, hp):
        self.max_health = hp

    def set_max_mana(self, mp):
        self.max_mana = mp

    def get_max_speed(self):
        return self.max_speed

    def get_max_health(self):
        return self.max_health

    def get_max_mana(self):
        return self.max_mana

    def get_health(self):
        return self.health

    def get_mana(self):
        return self.mana

    def get_speed(self):
        return self.speed

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
    def __init__(self, x, y, game):
        super().__init__(x, y, 60, 60, [0, 0], game)
        self.x_delta = 0
        self.y_delta = 0
        self.set_max_health(100)
        self.set_max_mana(100)
        self.set_max_speed(2)

        self.health = self.get_max_health()
        self.mana = self.get_max_mana()

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

        hits = list(filter(lambda x: not x.transition, pygame.sprite.spritecollide(self,                                                                                   self.game.get_environment_objects(),
                                                                                   False)))
        if hits:
            self.speed[0] = -self.speed[0]
            self.speed[1] = -self.speed[1]

        super().update()
        
        self.x_delta = 0
        self.y_delta = 0
