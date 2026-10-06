import pygame
import defines

from object import Object

vec = pygame.Vector2

class Enemy(Object):

    def __init__(self, width : int, height : int, sprite_light: pygame.Surface, sprite_dark: pygame.Surface, pos_x: int, pos_y: int):
        super().__init__(width, height, sprite_light, sprite_dark, pos_x, pos_y)

        self.pos = vec(pos_x, pos_y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)



    def on_update(self, dt: int, player: Object):
        self.follow_player(player)


    def follow_player(self, player: Object):

        direction_vec = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        direction_vec.normalize()

        direction_vec.scale_to_length(defines.ENEMY_ACC)
        self.rect.move_ip(direction_vec)
