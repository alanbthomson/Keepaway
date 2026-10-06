import os
import pygame
import pygame.freetype
import defines
from enemy import Enemy
from object import Object
from typing import List



class Render():
    player: Object
    objects: Object

    def __init__(self, objects, player, enemy, score):
        self.objects = objects
        self.player = player
        self.enemy = enemy
        self.score = score
        self.APP_FONT = pygame.freetype.Font(os.path.join('assets', 'fonts', 'Pixel Millennium.ttf'), 16)



    # resolution config

    screen_out = pygame.display.set_mode(defines.DISPLAY_RESOLUTION)
    screen_int = pygame.Surface(defines.INTERNAL_RESOLUTION)

    # draw rect alpha helper
    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)


    def draw_score(self, score: int):
        self.APP_FONT.render_to(self.screen_int, (180, 3), "Score: {score:}".format(score=score), (255,255,255))

    def draw_lose(self):
        self.APP_FONT.render_to(self.screen_int, (90, 3), "GAME OVER", (255,255,255))
        self.draw_out()

    # flip internal screen to output screen
    def draw_out(self):
        frame = pygame.transform.scale(self.screen_int, defines.DISPLAY_RESOLUTION)
        self.screen_out.blit(frame, frame.get_rect())
        pygame.display.flip()

    def draw_player(self):
        # draw player (handle flipping)
        if(self.player.facing_left):
            self.screen_int.blit(pygame.transform.flip(self.player.sprite_light, True, False), (self.player.rect.left - 2, self.player.rect.top - 1))
        else:
            self.screen_int.blit(self.player.sprite_light, (self.player.rect.left - 2, self.player.rect.top - 1))

        # draw rect debug
        if(defines.DEBUG_MODE):
            self.draw_rect_alpha(self.screen_int, defines.COLLISION_TEST_COLOR2, self.player.rect)



    # draw all objects visible during lights on
    def draw_light(self, score):
        self.screen_int.fill("black")
        for obj in self.objects:
            self.screen_int.blit(obj.sprite_light, obj.rect.topleft)
            if(defines.DEBUG_MODE):
                self.draw_rect_alpha(self.screen_int, defines.COLLISION_TEST_COLOR1, obj.rect)

        # draw player, enemy, coins
        self.draw_player()

        # draw enemy
        self.screen_int.blit(self.enemy.sprite_light, (self.enemy.rect.left - 2, self.enemy.rect.top - 1))
        self.draw_score(score)
        self.draw_out()

    # draw all objects visible during lights off
    def draw_dark(self, score):
        self.screen_int.fill("black")
        for obj in self.objects:
            self.screen_int.blit(obj.sprite_dark, obj.rect.topleft)
            if(defines.DEBUG_MODE):
                self.draw_rect_alpha(self.screen_int, defines.COLLISION_TEST_COLOR1, obj.rect)

        # draw player, enemy, coins
        self.draw_player()

        # draw enemy
        # self.screen_int.blit(self.enemy.sprite_dark, (self.enemy.rect.left - 2, self.enemy.rect.top - 1))
        self.draw_score(score)
        self.draw_out()

    def draw_dimming(self, alpha_percent: float, score):
        # make alpha 255
        alpha = defines.clamp(int(alpha_percent * 255), 0, 255)
        self.screen_int.fill("black")

        for obj in self.objects:
            # dim obj sprites
            obj_dim: pygame.Screen = obj.sprite_dark.set_alpha(alpha)
            self.screen_int.blit(obj.sprite_light, obj.rect.topleft)
            self.screen_int.blit(obj.sprite_dark, obj.rect.topleft)
            if(defines.DEBUG_MODE):
                self.draw_rect_alpha(self.screen_int, defines.COLLISION_TEST_COLOR1, obj.rect)

        # draw player, enemy, coins
        self.draw_player()

        # draw enemy
        self.screen_int.blit(self.enemy.sprite_dark, (self.enemy.rect.left - 2, self.enemy.rect.top - 1))

        self.draw_score(score)

        frame = pygame.transform.scale(self.screen_int, defines.DISPLAY_RESOLUTION)
        self.screen_out.blit(frame, frame.get_rect())
        pygame.display.flip()
