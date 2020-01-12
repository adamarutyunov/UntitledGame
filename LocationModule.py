import pygame
from BaseModule import *
from Constants import *


class Field(GameObject):
    def __init__(self, transition, texture):
        self.transition = transition
        self.texture = texture

    def get_transition(self):
        return self.transition

    def get_texture(self):
        return self.texture

    def init_super(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def draw(self):
        pass


class GrassField(Field):
    def __init__(self):
        super().__init__(True, GrassTexture)


class NoneField(Field):
    def __init__(self):
        super().__init__(False, NoneTexture)


class Location:
    def __init__(self, game):
        self.data = []
        self.func = None
        self.game = game

        self.width = -1
        self.height = -1

        self.objects = []
        self.environment_objects = []

    def load(self, file_name):
        self.data = []
        with open(file_name) as f:
            texture = f.read().split("\n")
            self.height = 0
            for row in texture:
                if not row:
                    break
                self.width = len(row)
                self.height += 1
                row_texts = []
                for column in list(row):
                    row_texts.append(LocationCodes[column]())
                self.data.append(row_texts)
        self.screen = pygame.Surface((self.width * CELL_SIZE,
                                      self.height * CELL_SIZE))
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j].init_super(j * CELL_SIZE,
                                                 i * CELL_SIZE,
                                                 CELL_SIZE,
                                                 CELL_SIZE)
                self.spawn_environment_object(self.data[i][j])
        self.update()

    def get_size(self):
        return self.width, self.height

    def get_pixel_size(self):
        return self.screen.get_size()

    def update(self):
        self.screen = pygame.Surface((self.width * CELL_SIZE,
                                      self.height * CELL_SIZE))
        for i in range(self.width):
            for j in range(self.height):
                self.screen.blit(self.data[j][i].get_texture(),
                            (i * CELL_SIZE, j * CELL_SIZE))

    def draw(self):
        return self.screen

    def get_objects(self):
        return self.objects

    def get_environment_objects(self):
        return self.environment_objects

    def spawn_object(self, obj):
        self.objects.append(obj)

    def spawn_environment_object(self, obj):
        self.environment_objects.append(obj)

field_textures_path = "textures/fields"
GrassTexture = load_image(f"{field_textures_path}/GrassField.png")
NoneTexture = load_image(f"{field_textures_path}/NoneField.png")

LocationCodes = {
    "G": GrassField,
    " ": NoneField}

locations_path = "locations"
