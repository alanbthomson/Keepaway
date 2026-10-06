import pygame


class Object():


    def __init__(self, width: int, height: int, light_image: pygame.Surface, dark_image: pygame.Surface, pos_x: int, pos_y: int):
        self.rect: pygame.Rect = pygame.Rect(pos_x, pos_y, width, height)
        self.sprite_light: pygame.Surface
        self.sprite_dark: pygame.Surface

        self.sprite_light = light_image
        self.sprite_dark = dark_image
        pass

    def on_update(self, dt: int):
        pass


    def on_draw_light(self):
        pass

    def on_draw_dark(self):
        pass
