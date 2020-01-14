import pygame
from math import copysign
from BaseModule import *
from Constants import *


class Entity(GameObject):
    def __init__(self, x, y, w, h, speed, game):
        super().__init__(x, y, w, h, speed)
        self.game = game

        self.max_speed = 0
        self.max_health = 0
        self.max_mana = 0

        self.health = 0
        self.mana = 0

        self.effects = []
        self.inventory = [None] * 28
        self.current_item_index = 0

        self.strength_characteristic = 0
        self.speed_characteristic = 0
        self.intelligence_characteristic = 0

        self.move_state = [1, 0]

        self.pixmaps = {}

        self.pixmap_ticks = 0

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

    def set_health(self, health):
        self.health = health
        self.game.get_main_gui().get_attribute_bar().redraw()

    def set_mana(self, mana):
        self.mana = mana
        self.game.get_main_gui().get_attribute_bar().redraw()

    def change_health(self, health):
        self.health += health
        self.game.get_main_gui().get_attribute_bar().redraw()

    def change_mana(self, mana):
        self.mana += mana
        self.game.get_main_gui().get_attribute_bar().redraw()

    def get_strength_characteristic(self):
        return self.strength_characteristic

    def get_speed_characteristic(self):
        return self.speed_characteristic

    def get_intelligence_characteristic(self):
        return self.intelligence_characteristic

    def set_strength_characteristic(self, strength):
        self.strength_characteristic = strength

    def set_speed_characteristic(self, speed):
        self.speed_characteristic = speed

    def set_intelligence_characteristic(self, intelligence):
        self.intelligence_characteristic = intelligence

    def change_strength_characteristic(self, strength):
        self.strength_characteristic += strength

    def change_speed_characteristic(self, speed):
        self.speed_characteristic += speed

    def change_intelligence_characteristic(self, intelligence):
        self.intelligence_characteristic += intelligence

    def fill_attributes(self):
        self.health = self.get_max_health()
        self.mana = self.get_max_mana()

    def get_move_state(self):
        return self.move_state

    def set_move_state(self, dxs, dys):
        if dxs == dys == 0:
            return

        if dxs > 0:
            self.move_state[0] = 1
        elif dxs < 0:
            self.move_state[0] = -1
        else:
            self.move_state[0] = 0

        if dys > 0:
            self.move_state[1] = 1
        elif dys < 0:
            self.move_state[1] = -1
        else:
            self.move_state[1] = 0
            
    def accelerate(self, dxs, dys):
        self.set_move_state(dxs, dys)
        if dxs != 0 or dys != 0:
            self.pixmap_ticks += 1
        
        self.speed[0] += dxs
        self.speed[1] += dys

        move_vector = (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        
        if move_vector > self.max_speed:
            if self.speed[1] == 0:
                self.speed[0] = copysign(self.max_speed, self.speed[0])
            elif self.speed[0] == 0:
                self.speed[1] = copysign(self.max_speed, self.speed[1])
            else:
                sy = (self.max_speed ** 2 / ((self.speed[0] / self.speed[1]) ** 2 + 1)) ** 0.5
                sx = sy * self.speed[0] / self.speed[1]
                self.speed = [copysign(sx, self.speed[0]), copysign(sy, self.speed[1])]

    def update_vector(self, xs, ys):
        delta = self.max_speed / 5 
        dxs = delta * xs
        dys = delta * ys
        self.accelerate(dxs, dys)

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

    def get_item(self, item):
        if not None in self.inventory:
            return
        self.inventory[self.inventory.index(None)] = item

    def remove_item(self, item):
        self.inventory.remove(item)

    def update(self):
        super().update()
        last_x, last_y = self.center

        walls = list(filter(lambda x: not x.transition, pygame.sprite.spritecollide(self, self.game.get_environment_objects(), False)))
        
        center = self.center

        for wall in walls:
            wx = wall.centerx
            wy = wall.centery
            if abs(last_x - wx) >= abs(last_y - wy):
                if self.speed[0] > 0:
                    self.set_x(wall.rect.left - self.width)
                elif self.speed[0] < 0:
                    self.set_x(wall.rect.right)
                self.speed[0] = 0
            if abs(last_x - wx) <= abs(last_y - wy):
                if self.speed[1] > 0:
                    self.set_y(wall.rect.top - self.height)
                elif self.speed[1] < 0:
                    self.set_y(wall.rect.bottom)
                self.speed[1] = 0

        for effect in self.effects:
            effect.run(self)
        self.effects = list(filter(lambda x: x.is_active(), self.effects))

        if self.mana < 0:
            self.mana = 0

        self.slow_down(0)
        self.slow_down(1)

        if self.get_health() <= 0:
            self.game.get_objects().remove(self)

    def affect_effect(self, effect):
        self.effects.append(effect)

    def get_attacked_enemies(self, attack_range):
        attacked_enemies = []
        enemies = self.game.get_objects()
        move_status = self.get_move_state()
        for e in enemies:
            dx = e.centerx - self.centerx
            dy = e.centery - self.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if (dx * move_status[0] >= 0 and dy * move_status[1] >= 0 and
                    dist < attack_range and e is not self):
                attacked_enemies.append(e)
        return attacked_enemies

    def use_current_item(self):
        current_item = self.inventory[self.current_item_index]

        if type(current_item) is None:
            return

        current_item.use(self)
        

class Player(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 42, 90, [0, 0], game)
        
        self.x_delta = 0
        self.y_delta = 0

        self.set_max_health(100)
        self.set_max_mana(100)
        self.set_max_speed(5)

        self.fill_attributes()

        self.texture_path = "textures/player/"
        self.load_pixmaps()

    def load_pixmaps(self):
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps[0] = [load_image(gtn("player_up_1"), -1),
                           load_image(gtn("player_up_2"), -1)]
        self.pixmaps[1] = [load_image(gtn("player_right_1"), -1),
                           load_image(gtn("player_right_2"), -1)]
        self.pixmaps[2] = [load_image(gtn("player_down_1"), -1),
                           load_image(gtn("player_down_2"), -1)]
        self.pixmaps[3] = [load_image(gtn("player_left_1"), -1),
                           load_image(gtn("player_left_2"), -1)]

    def calculate_current_pixmap(self):
        move_state = self.get_move_state()
        if move_state[0] == 1:
            self.current_pixmap_index = 1
        elif move_state[0] == -1:
            self.current_pixmap_index = 3
        elif move_state[1] == 1:
            self.current_pixmap_index = 2
        elif move_state[1] == -1:
            self.current_pixmap_index = 0

    def deltax(self, dx):
        self.x_delta += dx

    def deltay(self, dy):
        self.y_delta += dy

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.current_pixmap_index][self.pixmap_ticks // 10 % 2],
                    (0, 0))
        return screen

    def update(self):
        self.update_vector(self.x_delta, self.y_delta)
        self.calculate_current_pixmap()

        super().update()

        self.x_delta = 0
        self.y_delta = 0


class Zombie(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 60, 60, [0, 0], game)

        self.set_max_health(50)
        self.set_max_mana(100)
        self.set_max_speed(2)

        self.fill_attributes()

        self.vision_radius = 500
        self.attack_radius = 50

        self.power = 10
        self.attack_cooldown = 60
        self.current_cooldown = 0

        self.targets = [Player]

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(screen,
                           (255, 0, 0),
                           (30, 30),
                           round(self.width / 2))
        return screen
        
    def update(self):
        enemies = list(filter(lambda x: type(x) in self.targets, self.game.get_objects()))

        if not enemies:
            return

        nearest_player = min(enemies, key=lambda x: (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2)
        distance_to_nearest_player = ((self.centerx - nearest_player.centerx) ** 2 +
                                      (self.centery - nearest_player.centery) ** 2) ** 0.5
        
        if distance_to_nearest_player <= self.attack_radius:
            if self.current_cooldown <= 0:
                nearest_player.change_health(-self.power)
                self.current_cooldown = self.attack_cooldown
        elif distance_to_nearest_player <= self.vision_radius:
            dx = self.centerx - nearest_player.centerx
            dy = self.centery - nearest_player.centery

            if abs(dx) > abs(dy):
                dx, dy = copysign(1, -dx), copysign(abs(dy / dx), -dy)
            elif abs(dx) < abs(dy):
                dy, dx = copysign(1, -dy), copysign(abs(dx / dy), -dx)
            else:
                dy, dx = copysign(1, -dy), copysign(1, -dx)

            self.update_vector(dx, dy)

        if self.current_cooldown > 0:
            self.current_cooldown -= 1

        super().update()

