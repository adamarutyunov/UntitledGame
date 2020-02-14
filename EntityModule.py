import pygame
import random
from math import copysign
from BaseModule import *
from Constants import *
from MagicModule import *
from LocationModule import *


class Entity(GameObject):
    def __init__(self, x, y, w, h, speed, game):
        super().__init__(x, y, w, h, game, speed)
        
        self.max_speed = 0
        self.max_health = 0
        self.max_mana = 0

        self.health = 0
        self.mana = 0

        self.effects = []

        self.inventory = [None] * 28
        self.current_item_index = 0

        self.magic = []
        self.current_magic_index = 0

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
        
        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_attribute_bar()

    def set_mana(self, mana):
        self.mana = mana

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_attribute_bar()

    def change_health(self, health):
        self.health += health

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_attribute_bar()

        if health < 0:
            self.game.spawn_object(DamageParticleInstance.spawn(self.left, self.top,
                                                                self.width, self.height,
                                                                5))

    def change_mana(self, mana):
        self.mana += mana

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_attribute_bar()

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

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_characteristics_window()

    def change_speed_characteristic(self, speed):
        self.speed_characteristic += speed

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_characteristics_window()

    def change_intelligence_characteristic(self, intelligence):
        self.intelligence_characteristic += intelligence

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_characteristics_window()

    def get_basic_strength(self):
        return self.pure_strength

    def get_basic_speed(self):
        return self.pure_speed

    def get_basic_intelligence(self):
        return self.pure_intelligence

    def fill_attributes(self):
        self.health = self.get_max_health()
        self.mana = self.get_max_mana()

    def recalculate_attributes(self):
        self.speed_characteristic = max(self.speed_characteristic, 0)
        self.intelligence_characteristic = max(self.intelligence_characteristic, 0)
        self.strength_characteristic = max(self.strength_characteristic, 0)
        
        self.set_max_mana(self.intelligence_characteristic * 3)
        self.set_max_speed(self.speed_characteristic / 3)
        self.set_max_health(self.strength_characteristic * 3)

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)

    def set_pure_attributes(self):
        self.set_strength_characteristic(self.pure_strength)
        self.set_speed_characteristic(self.pure_speed)
        self.set_intelligence_characteristic(self.pure_intelligence)

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
            return False
        self.inventory[self.inventory.index(None)] = item

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_inventory()
            self.game.get_main_gui().update_item_cell()

    def remove_item(self, item):
        if item not in self.inventory:
            return
        self.inventory.remove(item)
        self.inventory.append(None)

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_inventory()
            self.game.get_main_gui().update_item_cell()

    def update(self):
        super().update()

        self.set_pure_attributes()
        last_x, last_y = self.center

        intersecs = pygame.sprite.spritecollide(self, self.game.get_objects(), False)

        for obj in intersecs:
            if Door in obj.__class__.__mro__:
                obj.change_location(self)
            elif type(obj) is Drop:
                obj.get(self)
            elif type(obj) is MagicDrop:
                obj.get(self)

        walls = list(filter(lambda x: not x.transition, pygame.sprite.spritecollide(self, self.game.get_environment_objects(), False)))
        
        center = self.center

        if walls:
            self.move(-self.speed[0], -self.speed[1])


        for effect in self.effects:
            effect.run(self)
            if not effect.is_active():
                self.remove_effect(effect)

        if self.mana < 0:
            self.mana = 0

        self.recalculate_attributes()

        self.slow_down(0)
        self.slow_down(1)

        if self.get_health() <= 0:
            self.die()

        self.change_health(0.005)
        self.change_mana(0.005)

    def affect_effect(self, effect):
        self.effects.append(effect.copy())

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_effects_window()

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)

            if Player in self.__class__.__mro__:
                self.game.get_main_gui().update_effects_window()

    def get_effects(self):
        return self.effects

    def get_attacked_enemies(self, attack_range):
        attacked_enemies = []
        enemies = self.game.get_objects()
        move_status = self.get_move_state()
        for e in enemies:
            if Entity not in e.__class__.__mro__:
                continue
            dx = e.centerx - self.centerx
            dy = e.centery - self.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if (dx * move_status[0] >= 0 and dy * move_status[1] >= 0 and
                    dist < attack_range and e is not self):
                attacked_enemies.append(e)
        return attacked_enemies

    def use_current_item(self):
        current_item = self.get_current_item()

        if current_item is None:
            return

        current_item.use(self)

    def get_item_by_index(self, i):
        return self.inventory[i]

    def get_current_item(self):
        return self.inventory[self.current_item_index]

    def next_item(self):
        if not any(self.inventory):
            return
        
        while True:
            self.current_item_index += 1
            self.current_item_index %= len(self.inventory)
            if self.get_current_item() is not None:
                break

        self.game.get_main_gui().update_item_cell()

    def prev_item(self):
        if not any(self.inventory):
            return
        
        while True:
            self.current_item_index -= 1
            self.current_item_index %= len(self.inventory)
            if self.get_current_item() is not None:
                break
            
        self.game.get_main_gui().update_item_cell()

    def next_magic(self):
        if not self.magic:
            return
        self.current_magic_index += 1
        self.current_magic_index %= len(self.magic)
        self.game.get_main_gui().update_magic_cell()

    def prev_magic(self):
        if not self.magic:
            return
        self.current_magic_index -= 1
        self.current_magic_index %= len(self.magic)
        self.game.get_main_gui().update_magic_cell()

    def get_inventory(self):
        return self.inventory

    def add_magic(self, magic):
        self.magic.append(magic)

        if Player in self.__class__.__mro__:
            self.game.get_main_gui().update_magic_cell()

    def use_magic(self):
        if len(self.magic) <= self.current_magic_index:
            return
        
        self.magic[self.current_magic_index].use(self)

    def attack_enemy(self, enemy, basic_damage):
        enemy.change_health(basic_damage * (1 + self.strength_characteristic * 3 / 100))

    def get_current_magic(self):
        if not self.magic:
            return None
        return self.magic[self.current_magic_index]

    def die(self):
        x, y = self.centerx, self.centery
        r = 100
        for obj in self.inventory:
            if obj is None:
                continue
            self.game.spawn_object(Drop(x + random.uniform(-1, 1) * r,
                                        y + random.uniform(-1, 1) * r,
                                        self.game, obj))
        
        self.game.get_objects().remove(self)
        

class Player(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 42, 90, [0, 0], game)
        
        self.x_delta = 0
        self.y_delta = 0

        self.pure_strength = 150
        self.pure_speed = 15
        self.pure_intelligence = 15

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.load_pixmaps()
        self.calculate_current_pixmap()

    def load_pixmaps(self):
        self.texture_path = "textures/player/"
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

    def die(self):
        super().die()
        self.game.get_main_gui().die()


class Zombie(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 51, 105, [0, 0], game)

        self.pure_strength = 25
        self.pure_speed = 5
        self.pure_intelligence = 0

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.vision_radius = 500
        self.attack_radius = 50

        self.power = 10
        self.attack_cooldown = 120
        self.current_cooldown = 0

        self.targets = [Player]
        self.load_pixmaps()
        self.calculate_current_pixmap()

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.current_pixmap_index][self.pixmap_ticks // 10 % 2],
                    (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.texture_path = "textures/zombie/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps[0] = [load_image(gtn("zombie_up_1"), -1),
                           load_image(gtn("zombie_up_2"), -1)]
        self.pixmaps[1] = [load_image(gtn("zombie_right_1"), -1),
                           load_image(gtn("zombie_right_2"), -1)]
        self.pixmaps[2] = [load_image(gtn("zombie_down_1"), -1),
                           load_image(gtn("zombie_down_2"), -1)]
        self.pixmaps[3] = [load_image(gtn("zombie_left_1"), -1),
                           load_image(gtn("zombie_left_2"), -1)]

    def calculate_current_pixmap(self):
        move_state = self.get_move_state()

        if abs(self.speed[0]) >= abs(self.speed[1]):
            if move_state[0] == 1:
                self.current_pixmap_index = 1
            elif move_state[0] == -1:
                self.current_pixmap_index = 3
        else:
            if move_state[1] == 1:
                self.current_pixmap_index = 2
            elif move_state[1] == -1:
                self.current_pixmap_index = 0
        
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

        self.calculate_current_pixmap()


class DistortedMan(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 51, 105, [0, 0], game)

        self.pure_strength = 100
        self.pure_speed = 2
        self.pure_intelligence = 50

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.vision_radius = 5000
        self.attack_radius = 50

        self.power = 2
        self.attack_cooldown = 60
        self.current_cooldown = 0

        self.targets = [Player]
        self.load_pixmaps()

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.pixmap_ticks // 10 % 3],
                    (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.texture_path = "textures/distorted_man/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps = [load_image(gtn("distorted_man_1"), -1),
                        load_image(gtn("distorted_man_2"), -1),
                        load_image(gtn("distorted_man_3"), -1)]
        
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
                nearest_player.affect_effect(DecreaseHealthEffect(600, 0.02))
                nearest_player.affect_effect(DecreaseManaEffect(600, 0.02))
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


class GreyDistortedMan(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 51, 105, [0, 0], game)

        self.pure_strength = 150
        self.pure_speed = 4
        self.pure_intelligence = 50

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.vision_radius = 5000
        self.attack_radius = 50

        self.power = 2
        self.attack_cooldown = 60
        self.current_cooldown = 0

        self.targets = [Player]
        self.load_pixmaps()

    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.pixmap_ticks // 10 % 3],
                    (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.texture_path = "textures/grey_distorted_man/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps = [load_image(gtn("grey_distorted_man_1"), -1),
                        load_image(gtn("grey_distorted_man_2"), -1),
                        load_image(gtn("grey_distorted_man_3"), -1)]
        
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
                nearest_player.affect_effect(DecreaseHealthEffect(1000, 0.05))
                nearest_player.affect_effect(DecreaseManaEffect(1000, 0.05))
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


class BurningMan(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 42, 117, [0, 0], game)

        self.pure_strength = 50
        self.pure_speed = 10
        self.pure_intelligence = 0

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.vision_radius = 1000
        self.attack_radius = 600

        self.power = 10
        self.attack_cooldown = 180
        self.current_cooldown = 0

        self.targets = [Player]
        self.load_pixmaps()


    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.pixmap_ticks // 10 % 3],
                    (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.texture_path = "textures/burning_man/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps = [load_image(gtn("burning_man_1"), -1),
                        load_image(gtn("burning_man_2"), -1),
                        load_image(gtn("burning_man_3"), -1)]
        
    def update(self):
        enemies = list(filter(lambda x: type(x) in self.targets, self.game.get_objects()))

        if not enemies:
            return

        nearest_player = min(enemies, key=lambda x: (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2)
        distance_to_nearest_player = ((self.centerx - nearest_player.centerx) ** 2 +
                                      (self.centery - nearest_player.centery) ** 2) ** 0.5
        
        if distance_to_nearest_player <= self.attack_radius:
            if self.current_cooldown <= 0:
                x, y = self.centerx, self.centery
                pos = nearest_player.centerx, nearest_player.centery
                
                tx = pos[0]
                ty = pos[1]
                dx = tx - x
                dy = ty - y
                a = abs(dx / dy)

                sy = copysign((50 / (a ** 2 + 1)) ** 0.5, dy)
                sx = copysign(a * sy, dx)

                self.game.spawn_object(Fireball(x - 32, y - 32, self.game, [sx, sy], self))
                
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

        self.pixmap_ticks += 1


class DarkBurningMan(BurningMan):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)

        self.pure_speed = 2

        self.attack_cooldown = 60
        self.attack_radius = 400

    def load_pixmaps(self):
        self.texture_path = "textures/burning_man_dark/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps = [load_image(gtn("burning_man_dark_1"), -1),
                        load_image(gtn("burning_man_dark_2"), -1),
                        load_image(gtn("burning_man_dark_3"), -1)]


class VioletEye(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 400, 484, [0, 0], game)

        self.pure_strength = 20
        self.pure_speed = 5
        self.pure_intelligence = 100

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.vision_radius = 500
        self.attack_radius = 1000

        self.power = 10
        self.attack_cooldown = 180
        self.current_cooldown = 0

        self.targets = [Player]
        self.load_pixmaps()


    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[self.pixmap_ticks // 200 % 4],
                    (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.texture_path = "textures/boss_violet_eye/"
        def gtn(name):
            return self.texture_path + name + ".png"
        
        self.pixmaps = [load_image(gtn("violet_eye_1"), -1),
                        load_image(gtn("violet_eye_2"), -1),
                        load_image(gtn("violet_eye_3"), -1),
                        load_image(gtn("violet_eye_4"), -1)]
        
    def update(self):
        enemies = list(filter(lambda x: type(x) in self.targets, self.game.get_objects()))

        if not enemies:
            return

        nearest_player = min(enemies, key=lambda x: (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2)
        distance_to_nearest_player = ((self.centerx - nearest_player.centerx) ** 2 +
                                      (self.centery - nearest_player.centery) ** 2) ** 0.5

        
        if distance_to_nearest_player <= self.attack_radius:
            if self.current_cooldown <= 0:
                x, y = self.centerx, self.centery

                self.game.spawn_object(Magicball(x, y, self.game, [5, 0], self))
                self.game.spawn_object(Magicball(x, y, self.game, [-5, 0], self))
                self.game.spawn_object(Magicball(x, y, self.game, [0, 5], self))
                self.game.spawn_object(Magicball(x, y, self.game, [0, -5], self))
                self.game.spawn_object(Magicball(x, y, self.game, [7.07, 7.07], self))
                self.game.spawn_object(Magicball(x, y, self.game, [7.07, -7.07], self))
                self.game.spawn_object(Magicball(x, y, self.game, [-7.07, 7.07], self))
                self.game.spawn_object(Magicball(x, y, self.game, [-7.07, -7.07], self))
                
                self.current_cooldown = self.attack_cooldown
                
        if distance_to_nearest_player <= self.vision_radius:
            self.attack_cooldown = 30
            
            dx = self.centerx - nearest_player.centerx
            dy = self.centery - nearest_player.centery

            dx = -dx
            dy = -dy

            if abs(dx) > abs(dy):
                dx, dy = copysign(1, -dx), copysign(abs(dy / dx), -dy)
            elif abs(dx) < abs(dy):
                dy, dx = copysign(1, -dy), copysign(abs(dx / dy), -dx)
            else:
                dy, dx = copysign(1, -dy), copysign(1, -dx)

            self.update_vector(dx, dy)
        else:
            self.attack_cooldown = 180

        if self.current_cooldown > 0:
            self.current_cooldown -= 1

        super().update()

        self.pixmap_ticks += 1

    def die(self):
        super().die()
        self.game.spawn_object(HellDoor(self.centerx, self.centery,
                                        UGame, TheFinalLocation,
                                        (0, 0)))


class Door(GameObject):
    def __init__(self, x, y, game, loc, new_pos):
        super().__init__(x, y, 45, 45, game)
        self.loc = loc
        self.new_x = new_pos[0]
        self.new_y = new_pos[1]

        self.image = load_image("textures/doors/door_2.png")

    def change_location(self, obj):
        self.game.delete_object(obj)
        if type(obj) is Player:
            self.game.get_screen().fill((0, 0, 0))
            self.game.load_location(self.loc)
        self.loc.spawn_object(obj)
        obj.set_x(self.new_x)
        obj.set_y(self.new_y)

    def draw(self):
        return self.image


class HellDoor(Door):
    def __init__(self, x, y, game, loc, new_pos):
        super().__init__(x, y, game, loc, new_pos)

        self.image = load_image("textures/doors/helldoor_2.png")


class Fireball(GameObject):
    def __init__(self, x, y, game, speed, sender):
        super().__init__(x, y, 45, 45, game, speed)
        self.sender = sender

        if speed[1] == 0:
            if speed[0] > 0:
                self.angle = 90
            else:
                self.angle = 270
        else:
            self.angle = math.degrees(math.atan2(speed[0], speed[1]))
        self.basic_pixmaps = [load_image("textures/balls/fireball_1.png"),
                              load_image("textures/balls/fireball_2.png")]

        self.rotated_pixmaps = list(map(lambda x: pygame.transform.rotate(x, self.angle), self.basic_pixmaps))

        self.ticks = 0

    def update(self):
        self.ticks += 1
        super().update()

        objects = pygame.sprite.spritecollide(self, self.game.get_objects(), False)
        if any(map(lambda x: Entity in x.__class__.__mro__ and
                   type(x) is not DarkBurningMan and
                   x is not self.sender, objects)):
            self.burst()

        environment_objects = pygame.sprite.spritecollide(self, self.game.get_environment_objects(), False)
        if any(map(lambda x: x.get_transition() is False, environment_objects)):
            self.burst()

    def draw(self):
        pix_tic = self.ticks // 5 % len(self.basic_pixmaps)
        
        return self.rotated_pixmaps[pix_tic]

    def burst(self):
        self.game.spawn_object(ExplosionParticleInstance.spawn(self.left + self.speed[0] * 5,
                                                               self.top + self.speed[1] * 5,
                                                               self.width, self.height,
                                                               30))
        objects = list(filter(lambda x: Entity in x.__class__.__mro__ and x is not self.sender and
                              type(x) is not type(self.sender) and
                              (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2 <= 25000,
                              self.game.get_objects()))
        objects += list(filter(lambda x: Entity in x.__class__.__mro__ and x is not self.sender and
                               type(x) is not type(self.sender),
                               pygame.sprite.spritecollide(self, self.game.get_objects(), False)))
        for o in objects:
            o.change_health(-5)
            o.affect_effect(DecreaseHealthEffect(300, 0.02))
        self.game.delete_object(self)


class FrozenBall(GameObject):
    def __init__(self, x, y, game, speed, sender):
        super().__init__(x, y, 90, 90, game, speed)
        self.sender = sender

        if speed[1] == 0:
            if speed[0] > 0:
                self.angle = 90
            else:
                self.angle = 270
        else:
            self.angle = math.degrees(math.atan2(speed[0], speed[1]))
        self.basic_pixmaps = [load_image("textures/balls/frozenball_1.png"),
                              load_image("textures/balls/frozenball_2.png")]

        self.rotated_pixmaps = list(map(lambda x: pygame.transform.rotate(x, self.angle), self.basic_pixmaps))

        self.ticks = 0

    def update(self):
        self.ticks += 1
        super().update()

        objects = pygame.sprite.spritecollide(self, self.game.get_objects(), False)
        if any(map(lambda x: Entity in x.__class__.__mro__ and
                   x is not self.sender, objects)):
            self.burst()

        environment_objects = pygame.sprite.spritecollide(self, self.game.get_environment_objects(), False)
        if any(map(lambda x: x.get_transition() is False, environment_objects)):
            self.burst()

    def draw(self):
        pix_tic = self.ticks // 5 % len(self.basic_pixmaps)
        
        return self.rotated_pixmaps[pix_tic]

    def burst(self):
        self.game.spawn_object(FrozenExplosionParticleInstance.spawn(self.left + self.speed[0] * 5,
                                                               self.top + self.speed[1] * 5,
                                                               self.width, self.height,
                                                               30))
        
        objects = list(filter(lambda x: Entity in x.__class__.__mro__ and x is not self.sender and
                      type(x) is not type(self.sender) and
                      (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2 <= 25000,
                      self.game.get_objects() + list(pygame.sprite.spritecollide(self, self.game.get_objects(), False))))
        objects += list(filter(lambda x: Entity in x.__class__.__mro__ and x is not self.sender and
                               type(x) is not type(self.sender),
                               pygame.sprite.spritecollide(self, self.game.get_objects(), False)))
        for o in objects:
            o.change_health(-10)
            eff = DecreaseSpeedEffect(300, 10)
            eff.set_title("Обморожение")
            o.affect_effect(eff)
        self.game.delete_object(self)


class FireballMagic(Magic):
    def __init__(self):
        super().__init__(self.run, 2.5)

        self.set_name("Огненный шар")
        self.load_icon(pygame.transform.rotate(load_image("textures/balls/fireball_1.png"), 135))

    def run(self, obj):
        x, y = obj.centerx, obj.centery
        pos = pygame.mouse.get_pos()
        tx = pos[0] + obj.game.get_main_drawer().drawdelta_x
        ty = pos[1] + obj.game.get_main_drawer().drawdelta_y
        dx = tx - x
        dy = ty - y

        if dy != 0:
            a = abs(dx / dy)
            sy = copysign((50 / (a ** 2 + 1)) ** 0.5, dy)
            sx = copysign(a * sy, dx)

        else:
            sx = copysign(50 ** 0.5, dx)
            sy = 0

        obj.game.spawn_object(Fireball(x - 32, y - 32, obj.game, [sx, sy], obj))


class FrozenballMagic(Magic):
    def __init__(self):
        super().__init__(self.run, 2.5)

        self.set_name("Ледяной шар")
        self.load_icon(pygame.transform.rotate(load_image("textures/balls/frozenball_1.png"), 135))

    def run(self, obj):
        x, y = obj.centerx, obj.centery
        pos = pygame.mouse.get_pos()
        tx = pos[0] + obj.game.get_main_drawer().drawdelta_x
        ty = pos[1] + obj.game.get_main_drawer().drawdelta_y
        dx = tx - x
        dy = ty - y
        
        if dy != 0:
            a = abs(dx / dy)
            sy = copysign((50 / (a ** 2 + 1)) ** 0.5, dy)
            sx = copysign(a * sy, dx)

        else:
            sx = copysign(50 ** 0.5, dx)
            sy = 0

        obj.game.spawn_object(FrozenBall(x - 32, y - 32, obj.game, [sx, sy], obj))


class HealMagic(Magic):
    def __init__(self):
        super().__init__(self.run, 5)

        self.set_name("Лечение")
        self.load_icon(pygame.transform.rotate(load_image("textures/balls/lifeball.png"), 135))

    def run(self, obj):
        obj.change_health(10)


class Magicball(GameObject):
    def __init__(self, x, y, game, speed, sender):
        super().__init__(x, y, 45, 45, game, speed)
        self.sender = sender

        if speed[1] == 0:
            if speed[0] > 0:
                self.angle = 90
            else:
                self.angle = 270
        else:
            self.angle = math.degrees(math.atan2(speed[0], speed[1]))
        self.basic_pixmaps = [load_image("textures/balls/magicball_1.png"),
                              load_image("textures/balls/magicball_2.png")]

        self.rotated_pixmaps = list(map(lambda x: pygame.transform.rotate(x, self.angle), self.basic_pixmaps))

        self.ticks = 0

    def update(self):
        self.ticks += 1
        super().update()

        objects = pygame.sprite.spritecollide(self, self.game.get_objects(), False)
        if any(map(lambda x: Entity in x.__class__.__mro__ and
                   type(x) is not DarkBurningMan and
                   x is not self.sender, objects)):
            self.burst()

        environment_objects = pygame.sprite.spritecollide(self, self.game.get_environment_objects(), False)
        if any(map(lambda x: x.get_transition() is False, environment_objects)):
            self.burst()

    def draw(self):
        pix_tic = self.ticks // 5 % len(self.basic_pixmaps)
        
        return self.rotated_pixmaps[pix_tic]

    def burst(self):
        self.game.spawn_object(ExplosionParticleInstance.spawn(self.left + self.speed[0] * 5,
                                                               self.top + self.speed[1] * 5,
                                                               self.width, self.height,
                                                               30))
        objects = list(filter(lambda x: Entity in x.__class__.__mro__ and x is not self.sender and
                              type(x) is not type(self.sender) and
                              (self.centerx - x.centerx) ** 2 + (self.centery - x.centery) ** 2 <= 25000,
                              self.game.get_objects()))
        for o in objects:
            o.change_health(-10)
            o.change_mana(-10)
            o.affect_effect(DecreaseHealthEffect(300, 0.02))
            o.affect_effect(DecreaseManaEffect(300, 0.02))
        self.game.delete_object(self)


class FinalSeller(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 64, 64, [0, 0], game)

        self.pure_strength = 1
        self.pure_speed = 1
        self.pure_intelligence = 1000000000

        self.strength_characteristic = self.pure_strength
        self.speed_characteristic = self.pure_speed
        self.intelligence_characteristic = self.pure_intelligence

        self.recalculate_attributes()
        self.fill_attributes()

        self.put_label("")
        self.final = pygame.Surface((1920, 1080))
        pygame.draw.rect(self.final, (255, 255, 255), (0, 0, *SCREEN_SIZE))
        self.final.set_alpha(0)

        self.load_pixmaps()

        self.ticks = 0


    def draw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(self.pixmaps[0],
                    (0, 0))
        self.game.screen.blit(self.label, (SCREEN_SIZE[0] // 2 - self.label.get_rect().width // 2, 900))
        self.game.screen.blit(self.final, (0, 0))
        return screen
    
    def load_pixmaps(self):
        self.pixmaps = [load_image("textures/items/prodavec.png", -1)]
        
    def update(self):
        self.game.get_main_player().fill_attributes()
        self.game.get_main_player().effects = []
        self.game.get_main_gui().clear()
        pygame.mixer.music.stop()

        for obj in self.game.get_objects():
            if obj is not self.game.get_main_player() and obj is not self:
                self.game.delete_object(obj)


        self.ticks += 1

        if self.ticks in range(200, 400):
            self.put_label("So, you win.")
        elif self.ticks in range(600, 800):
            self.put_label("But game is not completed yet.")
        elif self.ticks in range(1200, 1300):
            self.put_label("So...")
        elif self.ticks in range(1400, 1600):
            self.put_label("You are not supposed to be here.")
        else:
            self.put_label("")

        if self.ticks in range(1700, 1956):
            self.final.set_alpha((self.ticks - 1700))

        if self.ticks >= 1956:
            f = Final()

        self.game.screen.blit(self.final, (0, 0))
        super().update()
        

    def put_label(self, label):
        self.label = PixelTimes.render(label, True, (255, 255, 255))


class Final:
    def __init__(self):
        img = load_image("textures/gui/final.png")
        yl = load_image("textures/gui/yl.png")
        clock = pygame.time.Clock()
        self.ticks = 0
        
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            UGame.screen.blit(img, (0, 0))
            if self.ticks >= 90:
                UGame.screen.blit(yl, (SCREEN_SIZE[0] // 2 - yl.get_rect().width // 2, 900))
            pygame.display.flip()
            clock.tick(FPS)

            self.ticks += 1
            
        
