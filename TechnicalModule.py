import pygame
from LocationModule import *
from Constants import *


class Drawer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.get_screen()

        self.drawdelta_x = 0
        self.drawdelta_y = 0
        
        self.set_location()      

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

    def draw(self, objects):
        self.main_surface.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))
        self.main_surface.blit(self.location.draw(), (0, 0))
        for obj in objects:
            draw_surface = obj.draw()
            if draw_surface:
                self.main_surface.blit(draw_surface, (obj.left, obj.top))

        self.screen.blit(self.main_surface, (-self.drawdelta_x, -self.drawdelta_y))
        self.game.get_main_gui().draw()
        
        pygame.display.flip()

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

    def handle_keys(self, keys):
        if keys[pygame.K_a]:
            self.game.get_main_player().deltax(-1)
        if keys[pygame.K_d]:
            self.game.get_main_player().deltax(1)
        if keys[pygame.K_w]:
            self.game.get_main_player().deltay(-1)
        if keys[pygame.K_s]:
            self.game.get_main_player().deltay(1)
        
        if keys[pygame.K_e] and not self.last_keys[pygame.K_e]:
            self.game.get_main_player().use_current_item()
        if keys[pygame.K_TAB] and not self.last_keys[pygame.K_TAB]:
            self.game.toggle_gui()


class GUIModule:
    def __init__(self, pixmap, game):
        self.game = game
        
        self.pixmap = pixmap
        self.rect = self.pixmap.get_rect()
        
        self.width = self.rect.width
        self.height = self.rect.height

        self.screen = None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def redraw(self):
        pass

    def draw(self):
        return self.screen


class Inventory(GUIModule):
    def __init__(self, game):
        self.cells_pixmap = load_image("textures/gui/inventory.png")
        super().__init__(self.cells_pixmap, game)

        self.label = MagicFont.render("Inventory", True, LABEL_COLOR)
        self.label_rect = self.label.get_rect()

        self.redraw()

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))

        screen.blit(self.cells_pixmap, (0, 0))
        screen.blit(self.label, (self.width // 2 - self.label_rect.width // 2, 6))

        self.screen = screen


class ItemCell(GUIModule):
    def __init__(self, game):        
        self.cell_pixmap = load_image("textures/gui/cell.png")
        super().__init__(self.cell_pixmap, game)

        self.redraw()

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))
        screen.blit(self.cell_pixmap, (0, 0))

        self.screen = screen


class AttributeBar(GUIModule):
    def __init__(self, game):
        self.attribute_bar_pixmap = load_image("textures/gui/attribute_bar.png")
        super().__init__(self.attribute_bar_pixmap, game)

        self.redraw()

    def redraw(self):
        player = self.game.get_main_player()
        screen = pygame.Surface((200, 100), pygame.SRCALPHA)

        pygame.draw.rect(screen, (255, 0, 0),
                         [6, 6, 188 * player.get_health() // player.get_max_health(), 18])

        pygame.draw.rect(screen, (0, 0, 255),
                         [6, 56, 188 * player.get_mana() // player.get_max_mana(), 18])

        screen.blit(self.attribute_bar_pixmap, (0, 0))
        screen.blit(self.attribute_bar_pixmap, (0, 50))

        self.screen = screen


class EffectsWindow(GUIModule):
    def __init__(self, game):
        self.effect_window_pixmap = load_image("textures/gui/effects_window.png")
        super().__init__(self.effect_window_pixmap, game)

        self.label = MagicFont.render("Effects", True, LABEL_COLOR)
        self.label_rect = self.label.get_rect()

        self.redraw()

    def redraw(self):
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(screen, (0, 0, 0, 127), (0, 0, self.width, self.height))
 
        screen.blit(self.effect_window_pixmap, (0, 0))
        screen.blit(self.label, (self.width // 2 - self.label_rect.width // 2, 6))

        for i, effect in enumerate(self.game.get_main_player().get_effects()):
            icon = effect.get_icon()
            if icon:
                screen.blit(icon, (15, i * 25 + 40))
            label = MagicFont.render(effect.get_title(), True, LABEL_COLOR)
            screen.blit(label, (46, i * 25 + 42))

        self.screen = screen
        


class GUI:
    def __init__(self, game):
        self.game = game
        
        self.inventory = Inventory(game)
        self.attribute_bar = AttributeBar(game)
        self.item_cell = ItemCell(game)
        self.effects_window = EffectsWindow(game)

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
    
    def draw(self):
        indicators = self.attribute_bar.draw()
        self.game.screen.blit(indicators, (30, 30))
        
        if self.game.get_gui_state():
            inventory = self.inventory.draw()
            self.game.screen.blit(inventory, (30, SCREEN_SIZE[1] - 30 - self.inventory.get_height()))

            effects = self.effects_window.draw()
            self.game.screen.blit(effects, (30, SCREEN_SIZE[1] - 30 - self.inventory.get_height() - 30 - self.effects_window.get_height()))
            
        else:
            cell = self.item_cell.draw()
            self.game.screen.blit(cell, (30, SCREEN_SIZE[1] - 30 - self.item_cell.get_height()))
                
