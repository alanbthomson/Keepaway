import pygame
import defines
from typing import List
from object import Object
from pygame.locals import *

vec = pygame.Vector2

class Player(Object):
    move_speed: int = 40
    jump_cooldown: int = 1

    # player_pos : pygame.Vector2 = pygame.Vector2(render.screen_int.get_width() / 2, render.screen_int.get_height() / 2)
    player_pos : pygame.Vector2 = pygame.Vector2(defines.INTERNAL_RESOLUTION[0] // 2, defines.INTERNAL_RESOLUTION[1] // 2)

    def __init__(self, width : int, height : int, sprite: pygame.Surface, pos_x: int, pos_y: int):
        super().__init__(width, height, sprite, sprite, pos_x, pos_y)

        self.pos = vec(pos_x, pos_y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.can_jump: bool = False
        self.facing_left: bool = False

    def on_update(self, dt: int, objects: List[Object]):
        # input
        keys = pygame.key.get_pressed()


        # collision
        # get collided objects
        collision_indices = self.rect.collidelistall(objects)
        if collision_indices:
            # if(defines.DEBUG_MODE):
            #     print(collision_indices)
            for i in collision_indices:
                # handle bottom
                if(objects[i].rect.collidepoint(self.rect.midbottom)):
                    self.pos.y = objects[i].rect.top + 1
                    self.vel.y = 0
                    self.can_jump = True
                # handle top
                if(objects[i].rect.collidepoint(self.rect.midtop)):
                    self.pos.y = objects[i].rect.bottom + defines.PLAYER_HEIGHT
                    self.vel.y = 0
                # handle left
                if(objects[i].rect.collidepoint(self.rect.midleft)):
                    self.pos.x = objects[i].rect.right + (defines.PLAYER_WIDTH // 2)
                    self.vel.x = 0
                    self.can_jump = True
                # handle right
                if(objects[i].rect.collidepoint(self.rect.midright)):
                    self.pos.x = objects[i].rect.left - (defines.PLAYER_WIDTH // 2)
                    self.vel.x = 0
                    self.can_jump = True

        # screen collisions
        # handle left
        if(self.rect.left <= 0):
            self.pos.x = 0 + (defines.PLAYER_WIDTH // 2)
            self.vel.x = 0
        # handle right
        if(self.rect.right >= defines.INTERNAL_RESOLUTION[0]):
            self.pos.x = defines.INTERNAL_RESOLUTION[0] - (defines.PLAYER_WIDTH // 2)
            self.vel.x = 0

        # movement
        self.move(keys)

        self.facing_left = (self.vel.x < 0)

        super().on_update(dt)

    def move(self, keys):
        # do gravity
        self.acc = vec(0, defines.GRAV)

        # horizonal movement
        if keys[pygame.K_a]:
            self.acc.x = -defines.ACC
        if keys[pygame.K_d]:
            self.acc.x = defines.ACC
        if keys[pygame.K_SPACE] and self.can_jump:
            self.vel.y = -defines.JUMP
            self.can_jump = False

        self.acc.x += self.vel.x * defines.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # set new pos
        self.rect.midbottom = self.pos
