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

    def get_context_menu(self, x, y):
        return None


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

        self.context_menu_size = (500, 70)

        self.redraw()

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
            label = MagicFont.render(effect.get_title(), True, LABEL_COLOR)
            screen.blit(label, (46, i * 25 + 42))

        self.screen = screen

    def get_context_menu_size(self):
        return self.context_menu_size

    def get_context_menu(self, x, y):
        if x < 11 or x > 682 or y > 412 or y < 36:
            return None

        row = ((y - 36) // 25)
        if row >= len(self.all_effects):
            return None

        selected_effect = self.all_effects[row]
        context_menu = pygame.Surface(self.context_menu_size, pygame.SRCALPHA)

        pygame.draw.rect(context_menu, (0, 0, 0), (0, 0, *self.context_menu_size))
        pygame.draw.rect(context_menu, BORDER_COLOR, (0, 0, *self.context_menu_size), 2)

        icon = selected_effect.get_icon()
        title = selected_effect.get_title()
        description = selected_effect.get_description()

        title_pixmap = MagicFont.render(title, True, LABEL_COLOR)
        description_pixmap = MagicFont.render(description, True, LABEL_COLOR)

        context_menu.blit(title_pixmap, (self.context_menu_size[0] // 2 - title_pixmap.get_rect().width // 2, 10))
        context_menu.blit(icon, (10, 38))

        context_menu.blit(description_pixmap, (40, 42))
        

        return context_menu
        


class GUI:
    def __init__(self, game):
        self.game = game
        
        self.inventory = Inventory(game)
        self.attribute_bar = AttributeBar(game)
        self.item_cell = ItemCell(game)
        self.effects_window = EffectsWindow(game)

        self.context_menu = None

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
            
        
    
    def draw(self):
        indicators = self.attribute_bar.draw()
        self.game.screen.blit(indicators, ATTRIBUTE_BAR_POS)
        
        if self.game.get_gui_state():
            inventory = self.inventory.draw()
            self.game.screen.blit(inventory, INVENTORY_POS)

            effects = self.effects_window.draw()
            self.game.screen.blit(effects, (EFFECTS_WINDOW_POS))
        else:
            cell = self.item_cell.draw()
            self.game.screen.blit(cell, ITEM_CELL_POS)

        if self.context_menu is not None:
            self.game.screen.blit(self.context_menu, (self.mouse_x - self.context_menu.get_rect().width // 2,
                                                      self.mouse_y - 120))
                
