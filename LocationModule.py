import pygame
from Constants import *


class Field:
    def __init__(self, transition, texture):
        self.transition = transition
        self.texture = texture

    def get_transition(self):
        return self.transition

    def get_texture(self):
        return self.texture


class GrassField(Field):
    def __init__(self):
        super().__init__(True, GrassTexture)


class NoneField(Field):
    def __init__(self):
        super().__init__(True, NoneTexture)


class Location:
    def __init__(self):
        self.data = []
        self.func = None

        self.width = -1
        self.height = -1

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

    def get_size(self):
        return self.width, self.height

    def get_pixel_size(self):
        return self.screen.get_size()

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                self.screen.blit(self.data[j][i].get_texture(),
                            (i * CELL_SIZE, j * CELL_SIZE))
        return self.screen

field_textures_path = "textures/fields"
GrassTexture = pygame.image.load(f"{field_textures_path}/GrassField.png")
NoneTexture = pygame.image.load(f"{field_textures_path}/NoneField.png")

LocationCodes = {
    "G": GrassField,
    " ": NoneField}

locations_path = "locations"
FirstLocation = Location()
FirstLocation.load(f"{locations_path}/FirstLocation.loc")