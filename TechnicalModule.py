import pygame
from LocationModule import *
from Constants import *
from EntityModule import *
from itertools import cycle
from random import shuffle, randint


class Drawer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.get_screen()

        self.drawdelta_x = 0
        self.drawdelta_y = 0     

    def set_location(self):
        self.location = self.game.get_location()
        self.main_surface = pygame.Surface(self.location.get_pixel_size(), pygame.SRCALPHA)

    def deltax(self, dx):
        self.drawdelta_x += dx

    def deltay(self, dy):
        self.drawdelta_y += dy

    def get_dd_x(self):
        return self.drawdelta_x

    def get_dd_y(self):
        return self.drawdelta_y

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 1920, 1080))
        self.screen.blit(self.location.draw(), (-self.drawdelta_x, -self.drawdelta_y))

        objects = self.game.get_objects()
        for obj in objects:
            draw_surface = obj.draw()
            if draw_surface:
                self.screen.blit(draw_surface, (obj.left - self.drawdelta_x,
                                                obj.top - self.drawdelta_y))
                hp_indicator = self.game.get_main_gui().get_health_indicator(obj)
                if hp_indicator:
                    self.screen.blit(hp_indicator, (obj.left - self.drawdelta_x,
                                                    obj.top - self.drawdelta_y - 10 - hp_indicator.get_rect().height))

        self.game.get_main_gui().draw()

    def update_drawdeltas(self):
        player = self.game.get_main_player()
        
        if player.top - self.get_dd_y() < TOP_DRAW_SIDE:
            self.deltay(player.top - self.get_dd_y() - TOP_DRAW_SIDE)
        if player.bottom - self.get_dd_y() > BOTTOM_DRAW_SIDE:
            self.deltay(player.bottom - self.get_dd_y() - BOTTOM_DRAW_SIDE)
        if player.left - self.get_dd_x() < LEFT_DRAW_SIDE:
            self.deltax(player.left - self.get_dd_x() - LEFT_DRAW_SIDE)
        if player.right - self.get_dd_x() > RIGHT_DRAW_SIDE:
            self.deltax(player.right - self.get_dd_x() - RIGHT_DRAW_SIDE)

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.last_keys = pygame.key.get_pressed()

    def process_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.handle_events(events)
        self.handle_keys(keys)
        self.last_keys = keys

    def handle_events(self, events):
        for event in events:
            if event.type is pygame.QUIT:
                self.game.close()
            elif event.type is pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.get_main_player().use_current_item()
                elif event.button == 4:
                    self.game.get_main_player().next_item()
                elif event.button == 5:
                    self.game.get_main_player().prev_item()

    def handle_keys(self, keys):
        if keys[pygame.K_a]:
            self.game.get_main_player().deltax(-1)
        if keys[pygame.K_d]:
            self.game.get_main_player().deltax(1)
        if keys[pygame.K_w]:
            self.game.get_main_player().deltay(-1)
        if keys[pygame.K_s]:
            self.game.get_main_player().deltay(1)
        
        if keys[pygame.K_TAB] and not self.last_keys[pygame.K_TAB]:
            self.game.toggle_gui()
        if keys[pygame.K_r] and not self.last_keys[pygame.K_r]:
            self.game.get_main_player().use_magic()

        if keys[pygame.K_q] and not self.last_keys[pygame.K_q]:
            self.game.get_main_player().prev_magic()
        if keys[pygame.K_e] and not self.last_keys[pygame.K_e]:
            self.game.get_main_player().next_magic()
            


class GUIModule:
    def __init__(self, pixmap, game):
        self.game = game
        
        self.pixmap = pixmap
        self.rect = self.pixmap.get_rect()
        self.context_menu_size = (0, 0)
        
        self.width = self.rect.width
        self.height = self.rect.height

        self.screen = None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_context_menu_size(self):
        return self.context_menu_size

    def set_context_menu_size(self, w, h):
        self.context_menu_size = (w, h)

    def redraw(self):
        pass

    def draw(self):
        return self.screen

    def get_context_menu(self, x, y):
        return None


class Inventory(GUIModule):
    def __init__(self, game):
        self.cells_pixmap = load_image("textures/gui/inventory.png")
        super().__init__(self.cells_pixmap, game)

        self.label = MagicFont.render("Inventory", True, LABEL_COLOR)
        self.label_rect = self.label.get_rect()


    def get_selected_cell(self, x, y):
        x -= 3
        y -= 28

        if x < 0 or y < 0 or x > self.width or y > self.height:
            return None

        cell_x = x // 98
        cell_y = y // 98

        res = cell_y * 7 + cell_x
        if res > 27 or res < 0:
            return None

        return res

    def get_context_menu(self, x, y):
        selected_cell = self.get_selected_cell(x, y)
        if selected_cell is None:
            return None
        
        selected_item = self.game.get_main_player().get_item_by_index(selected_cell)

        if selected_item is None:
            return None

        icon = selected_item.get_icon()
        name = selected_item.get_name()
        
        name_pixmap = MagicFont.render(name, True, LABEL_COLOR)
        name_pixmap_rect = name_pixmap.get_rect()

        self.set_context_menu_size(name_pixmap_rect.width + 40, 40)

        context_menu = pygame.Surface(self.context_menu_size, pygame.SRCALPHA)

        pygame.draw.rect(context_menu, (0, 0, 0), (0, 0, *self.context_menu_size))
        pygame.draw.rect(context_menu, BORDER_COLOR, (0, 0, *self.context_menu_size), 2)

        context_menu.blit(name_pixmap, (self.context_menu_size[0] // 2 - name_pixmap.get_rect().width // 2, 10))

        return context_menu
        

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))

        screen.blit(self.cells_pixmap, (0, 0))
        screen.blit(self.label, (self.width // 2 - self.label_rect.width // 2, 6))

        inventory = self.game.get_main_player().get_inventory()

        for i, item in enumerate(inventory):
            if item is None:
                continue
            icon = pygame.transform.scale(item.get_icon(), (72, 72))

            screen.blit(icon, (i % 7 * 98 + 16, i // 7 * 98 + 42))

        self.screen = screen


class CharacteristicsWindow(GUIModule):
    def __init__(self, game):
        self.characteristics_window_pixmap = load_image("textures/gui/characteristics_window.png")

        super().__init__(self.characteristics_window_pixmap, game)

        self.label = MagicFont.render("Characteristics", True, LABEL_COLOR)
        self.label_rect = self.label.get_rect()

    def redraw(self):
        player = self.game.get_main_player()
        
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))

        screen.blit(self.characteristics_window_pixmap, (0, 0))
        screen.blit(self.label, (self.width // 2 - self.label_rect.width // 2, 6))

        strength_title = MagicFont.render("Strength", True, GRAY_LABEL_COLOR)

        if player.get_strength_characteristic() > player.get_basic_strength():
            color = GREEN_LABEL_COLOR
        elif player.get_strength_characteristic() < player.get_basic_strength():
            color = RED_LABEL_COLOR
        else:
            color = GRAY_LABEL_COLOR

        strength_value = MagicFont.render(str(player.get_strength_characteristic()), True, color)
        screen.blit(strength_title, (16, 40))
        screen.blit(strength_value, (300 - strength_value.get_rect().width, 40))


        speed_title = MagicFont.render("Speed", True, GRAY_LABEL_COLOR)

        if player.get_speed_characteristic() > player.get_basic_speed():
            color = GREEN_LABEL_COLOR
        elif player.get_speed_characteristic() < player.get_basic_speed():
            color = RED_LABEL_COLOR
        else:
            color = GRAY_LABEL_COLOR

        speed_value = MagicFont.render(str(player.get_speed_characteristic()), True, color)
        screen.blit(speed_title, (16, 65))
        screen.blit(speed_value, (300 - speed_value.get_rect().width, 65))


        intelligence_title = MagicFont.render("Intelligence", True, GRAY_LABEL_COLOR)

        if player.get_intelligence_characteristic() > player.get_basic_intelligence():
            color = GREEN_LABEL_COLOR
        elif player.get_intelligence_characteristic() < player.get_basic_intelligence():
            color = RED_LABEL_COLOR
        else:
            color = GRAY_LABEL_COLOR

        intelligence_value = MagicFont.render(str(player.get_intelligence_characteristic()), True, color)
        screen.blit(intelligence_title, (16, 90))
        screen.blit(intelligence_value, (300 - intelligence_value.get_rect().width, 90))

        self.screen = screen

class ItemCell(GUIModule):
    def __init__(self, game):        
        self.cell_pixmap = load_image("textures/gui/cell.png")
        super().__init__(self.cell_pixmap, game)

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))
        screen.blit(self.cell_pixmap, (0, 0))

        item = self.game.get_main_player().get_current_item()

        if item is not None:
            icon = pygame.transform.scale(item.get_icon(), (50, 50))

            screen.blit(icon, (12, 12))

        self.screen = screen


class MagicCell(GUIModule):
    def __init__(self, game):        
        self.cell_pixmap = load_image("textures/gui/cell.png")
        super().__init__(self.cell_pixmap, game)

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))
        screen.blit(self.cell_pixmap, (0, 0))

        magic = self.game.get_main_player().get_current_magic()

        if magic is not None:
            icon = pygame.transform.scale(magic.get_icon(), (50, 50))
            screen.blit(icon, (12, 12))

        self.screen = screen


class AttributeBar(GUIModule):
    def __init__(self, game):
        self.attribute_bar_pixmap = load_image("textures/gui/attribute_bar.png")
        super().__init__(self.attribute_bar_pixmap, game)

        self.set_context_menu_size(200, 40)

    def redraw(self):
        player = self.game.get_main_player()
        
        health = player.get_health()
        max_health = player.get_max_health()
        mana = player.get_mana()
        max_mana = player.get_max_mana()
        
        screen = pygame.Surface((200, 100), pygame.SRCALPHA)

        if health > 0 and max_health > 0:
            pygame.draw.rect(screen, (255, 0, 0),
                             [6, 6, 188 * health // max_health, 18])

        if mana > 0 and max_mana > 0:
            pygame.draw.rect(screen, (0, 0, 255),
                             [6, 56, 188 * mana // max_mana, 18])

        screen.blit(self.attribute_bar_pixmap, (0, 0))
        screen.blit(self.attribute_bar_pixmap, (0, 50))

        self.screen = screen

    def get_context_menu(self, x, y):
        if 24 < y < 56 or y < 0 or y > 100 or x < 0 or x > self.get_width():
            return None

        player = self.game.get_main_player()

        context_menu = pygame.Surface(self.context_menu_size, pygame.SRCALPHA)

        pygame.draw.rect(context_menu, (0, 0, 0), (0, 0, *self.context_menu_size))
        pygame.draw.rect(context_menu, BORDER_COLOR, (0, 0, *self.context_menu_size), 2)

        if y <= 24:
            text = MagicFont.render(f"{ceil(player.get_health())}/{ceil(player.get_max_health())}", True, LABEL_COLOR)
        elif y >= 56:
            text = MagicFont.render(f"{ceil(player.get_mana())}/{ceil(player.get_max_mana())}", True, LABEL_COLOR)

        context_menu.blit(text, (self.context_menu_size[0] // 2 - text.get_rect().width // 2, 10))

        return context_menu


class EffectsWindow(GUIModule):
    def __init__(self, game):
        self.effect_window_pixmap = load_image("textures/gui/effects_window.png")
        super().__init__(self.effect_window_pixmap, game)

        self.label = MagicFont.render("Effects", True, LABEL_COLOR)
        self.label_rect = self.label.get_rect()

        self.set_context_menu_size(500, 70)

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))
 
        screen.blit(self.effect_window_pixmap, (0, 0))
        screen.blit(self.label, (self.width // 2 - self.label_rect.width // 2, 6))

        self.all_effects = self.game.get_main_player().get_effects()

        for i, effect in enumerate(self.all_effects):
            icon = effect.get_icon()
            if icon:
                screen.blit(icon, (15, i * 25 + 40))
            title = effect.get_title()
            if title:
                label = MagicFont.render(effect.get_title(), True, LABEL_COLOR)
            else:
                label = MagicFont.render(effect.get_description(), True, GRAY_LABEL_COLOR)
            screen.blit(label, (46, i * 25 + 42))

        self.screen = screen

    def get_hovered_row(self, x, y):
        if x < 11 or x > 682 or y > 412 or y < 36:
            return None

        row = ((y - 36) // 25)
        if row >= len(self.all_effects):
            return None

        return row
        

    def get_context_menu(self, x, y):
        selected_row = self.get_hovered_row(x, y)
        if selected_row is None:
            return None

        selected_effect = self.all_effects[selected_row]
        context_menu = pygame.Surface(self.context_menu_size, pygame.SRCALPHA)

        pygame.draw.rect(context_menu, (0, 0, 0), (0, 0, *self.context_menu_size))
        pygame.draw.rect(context_menu, BORDER_COLOR, (0, 0, *self.context_menu_size), 2)

        icon = selected_effect.get_icon()
        title = selected_effect.get_title()
        description = selected_effect.get_description()

        title_pixmap = MagicFont.render(title, True, LABEL_COLOR)
        description_pixmap = MagicFont.render(description, True, LABEL_COLOR)

        context_menu.blit(title_pixmap, (self.context_menu_size[0] // 2 - title_pixmap.get_rect().width // 2, 10))

        if icon is not None:
            context_menu.blit(icon, (10, 38))

        context_menu.blit(description_pixmap, (40, 42))
        
        return context_menu


class InfoText(GUIModule):
    def __init__(self, game, text, time):
        self.pixmap = MagicFont.render(text, True, LABEL_COLOR)
        super().__init__(self.pixmap, game)

        self.time = time

    def draw(self):
        self.time -= 1
        if self.time <= 0:
            self.game.get_main_gui().delete_info()
            
        return self.pixmap
        

class GUI:
    def __init__(self, game):
        self.game = game
        
        self.inventory = Inventory(game)
        self.attribute_bar = AttributeBar(game)
        self.item_cell = ItemCell(game)
        self.effects_window = EffectsWindow(game)
        self.characteristics_window = CharacteristicsWindow(game)
        self.magic_cell = MagicCell(game)

        self.hurt = pygame.Surface((1920, 1080))
        pygame.draw.rect(self.hurt, (255, 0, 0), (0, 0, 1920, 1080))

        self.context_menu = None
        self.info = None

    def get_inventory(self):
        return self.inventory

    def get_attribute_bar(self):
        return self.attribute_bar

    def get_item_cell(self):
        return self.item_cell

    def get_effects_window(self):
        return self.effects_window

    def update_inventory(self):
        self.inventory.redraw()

    def update_attribute_bar(self):
        self.attribute_bar.redraw()

    def update_item_cell(self):
        self.item_cell.redraw()

    def update_effects_window(self):
        self.effects_window.redraw()

    def update_characteristics_window(self):
        self.characteristics_window.redraw()

    def update_magic_cell(self):
        self.magic_cell.redraw()

    def redraw_all(self):
        self.update_inventory()
        self.update_attribute_bar()
        self.update_item_cell()
        self.update_effects_window()
        self.update_characteristics_window()
        self.update_magic_cell()

    def die(self):
        d = DeathMenu()  

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.mouse_x, self.mouse_y = x, y
        if self.game.get_gui_state():
            self.context_menu = (self.inventory.get_context_menu(x - INVENTORY_POS[0],
                                                                 y - INVENTORY_POS[1]) or
                                 self.attribute_bar.get_context_menu(x - ATTRIBUTE_BAR_POS[0],
                                                                     y - ATTRIBUTE_BAR_POS[1]) or
                                 self.item_cell.get_context_menu(x - ITEM_CELL_POS[0],
                                                                 y - ITEM_CELL_POS[1]) or
                                 self.effects_window.get_context_menu(x - EFFECTS_WINDOW_POS[0],
                                                                      y - EFFECTS_WINDOW_POS[1]))
        else:
            self.context_menu = (self.attribute_bar.get_context_menu(x - ATTRIBUTE_BAR_POS[0],
                                                                     y - ATTRIBUTE_BAR_POS[1]) or
                                 self.item_cell.get_context_menu(x - ITEM_CELL_POS[0],
                                                                 y - ITEM_CELL_POS[1]))

    def get_health_indicator(self, obj):
        if Entity not in obj.__class__.__mro__:
            return None

        health, max_health = obj.get_health(), obj.get_max_health()
        w = obj.width
        h = w // 10

        hp = pygame.Surface((w, h))
        hp.fill((200, 0, 0))

        if health <= 0 or max_health <= 0:
            return hp

        pygame.draw.rect(hp, (50, 255, 50), (0, 0, w * health // max_health, h))
        return hp
        
    
    def draw(self):
        health = self.game.get_main_player().get_health()
        max_health = self.game.get_main_player().get_max_health()
        if health / max_health < 0.1:
            koef = health / (max_health * 0.1)
            self.hurt.set_alpha(255 * (1 - koef) // 1)
        else:
            self.hurt.set_alpha(0)

        self.game.screen.blit(self.hurt, (0, 0))
            
        indicators = self.attribute_bar.draw()
        self.game.screen.blit(indicators, ATTRIBUTE_BAR_POS)

        if self.info:
            info = self.info.draw()
            if self.info and info:
                self.game.screen.blit(info, (1890 - self.info.width, 1060 - self.info.height))
        
        if self.game.get_gui_state():
            inventory = self.inventory.draw()
            self.game.screen.blit(inventory, INVENTORY_POS)

            effects = self.effects_window.draw()
            self.game.screen.blit(effects, (EFFECTS_WINDOW_POS))

            characteristics = self.characteristics_window.draw()
            self.game.screen.blit(characteristics, CHARACTERISTICS_WINDOW_POS)
        else:
            cell = self.item_cell.draw()
            self.game.screen.blit(cell, ITEM_CELL_POS)

            magic_cell = self.magic_cell.draw()
            self.game.screen.blit(magic_cell, MAGIC_CELL_POS)

        if self.context_menu is not None:
            self.game.screen.blit(self.context_menu, (self.mouse_x - self.context_menu.get_rect().width // 2,
                                                      self.mouse_y - self.context_menu.get_rect().height - 10))

    def add_info(self, text, time):
        self.info = InfoText(self.game, text, time)

    def delete_info(self):
        self.info = None


class MusicModule:
    def __init__(self, game):
        self.game = game

        self.music_path = "music/"
        self.music_names = ["adventure_begins",
                            "hello_world",
                            "lonely_sola",
                            "lovely_caves",
                            "the_battle_is_going_on",
                            "greed"]
        random.shuffle(self.music_names)
        self.sound_paths = map(lambda x: self.music_path + x + ".mp3", self.music_names)
        self.sounds = cycle(self.sound_paths)

        self.silence_time = 3600
        self.current_time = 0

    def change_music(self, music_name):
        self.current_time = 0
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def update(self):
        if pygame.mixer.music.get_busy():
            return

        self.current_time += 1
        if self.current_time >= self.silence_time:
            self.change_music(next(self.sounds))


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SRCALPHA)
        self.pixmap = load_image("textures/gui/main_menu.png")
        
        self.playbutton = load_image("textures/gui/playbutton.png")
        self.playbutton_hover = load_image("textures/gui/playbutton_hover.png")

        self.exitbutton = load_image("textures/gui/exitbutton.png")
        self.exitbutton_hover = load_image("textures/gui/exitbutton_hover.png")

        self.mouse_pos = pygame.mouse.get_pos()

        self.playbutton_pos = (575, 600)
        self.exitbutton_pos = (575, 800)

        pygame.mixer.music.load("music/main_theme.mp3")
        pygame.mixer.music.set_volume(0.5)

        self.run()

    def run(self):
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        res = self.click()
                        if res is False:
                            pygame.quit()
                            return
                        elif res is True:
                            self.screen.fill((0, 0, 0))
                            pygame.mixer.music.stop()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.draw()
            clock.tick(FPS)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.pixmap, (0, 0))

        if (self.playbutton_pos[0] <= self.mouse_pos[0] <= self.playbutton_pos[0] + self.playbutton.get_rect().width and
                self.playbutton_pos[1] <= self.mouse_pos[1] <= self.playbutton_pos[1] + self.playbutton.get_rect().height):
            self.screen.blit(self.playbutton_hover, self.playbutton_pos)
        else:
            self.screen.blit(self.playbutton, self.playbutton_pos)

        if (self.exitbutton_pos[0] <= self.mouse_pos[0] <= self.exitbutton_pos[0] + self.exitbutton.get_rect().width and
                self.exitbutton_pos[1] <= self.mouse_pos[1] <= self.exitbutton_pos[1] + self.exitbutton.get_rect().height):
            self.screen.blit(self.exitbutton_hover, self.exitbutton_pos)
        else:
            self.screen.blit(self.exitbutton, self.exitbutton_pos)

        pygame.display.flip()

    def click(self):
        if (self.playbutton_pos[0] <= self.mouse_pos[0] <= self.playbutton_pos[0] + self.playbutton.get_rect().width and
                self.playbutton_pos[1] <= self.mouse_pos[1] <= self.playbutton_pos[1] + self.playbutton.get_rect().height):
            return True

        if (self.exitbutton_pos[0] <= self.mouse_pos[0] <= self.exitbutton_pos[0] + self.exitbutton.get_rect().width and
                self.exitbutton_pos[1] <= self.mouse_pos[1] <= self.exitbutton_pos[1] + self.exitbutton.get_rect().height):
            return False        
        

class DeathMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SRCALPHA)
        self.pixmap = load_image("textures/gui/death_menu.png")

        self.exitbutton = load_image("textures/gui/exitbutton_red.png")
        self.exitbutton_hover = load_image("textures/gui/exitbutton_red_hover.png")

        self.d = load_image("textures/gui/death_d.png")
        self.e = load_image("textures/gui/death_e.png")
        self.a = load_image("textures/gui/death_a.png")
        self.t = load_image("textures/gui/death_t.png")
        self.h = load_image("textures/gui/death_h.png")

        self.mouse_pos = pygame.mouse.get_pos()

        self.exitbutton_pos = (575, 750)

        pygame.mixer.music.stop()

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        res = self.click()
                        if res is False:
                            pygame.quit()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.draw()
            clock.tick(FPS)

    def draw(self):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.d, (164 + randint(-15, 15), 150 + randint(-15, 15)))
        self.screen.blit(self.e, (528 + randint(-15, 15), 150 + randint(-15, 15)))
        self.screen.blit(self.a, (842 + randint(-15, 15), 150 + randint(-15, 15)))
        self.screen.blit(self.t, (1166 + randint(-15, 15), 150 + randint(-15, 15)))
        self.screen.blit(self.h, (1480 + randint(-15, 15), 150 + randint(-15, 15)))

        if (self.exitbutton_pos[0] <= self.mouse_pos[0] <= self.exitbutton_pos[0] + self.exitbutton.get_rect().width and
                self.exitbutton_pos[1] <= self.mouse_pos[1] <= self.exitbutton_pos[1] + self.exitbutton.get_rect().height):
            self.screen.blit(self.exitbutton_hover, self.exitbutton_pos)
        else:
            self.screen.blit(self.exitbutton, self.exitbutton_pos)

        pygame.display.flip()

    def click(self):
        if (self.exitbutton_pos[0] <= self.mouse_pos[0] <= self.exitbutton_pos[0] + self.exitbutton.get_rect().width and
                self.exitbutton_pos[1] <= self.mouse_pos[1] <= self.exitbutton_pos[1] + self.exitbutton.get_rect().height):
            return False
