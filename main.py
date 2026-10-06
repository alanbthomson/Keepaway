import os
from typing import List
from enum import Enum
import pygame
import pygame.freetype
from object import Object
from player import Player
from enemy import Enemy
import defines
import random

# pygame setup
pygame.init()

# window setup
pygame.display.set_icon(defines.APP_ICON)
pygame.display.set_caption("Keepaway")

# screen setup
import render

# game state
class State(Enum):
    LIGHT = 1,
    DARK = 2,
    DIMMING = 3,
    GAMEOVER = 4,
    PAUSE = 5
GAME_STATE: State = State.LIGHT
running: bool = True

# points
score: int = 0

# level setup
collidables : List[Object] = []
level = pygame.image.load(os.path.join('assets', 'maps', random.choice(os.listdir(os.path.join('assets', 'maps',)))))
# pygame.image.load(os.path.join('assets', 'maps', 'level1.png'))
for row in range(0, 16):
    for col in range(0, 9):
        if(level.get_at((row, col)) == defines.AIR_COLOR):
            continue
        if(level.get_at((row, col)) == defines.GROUND_COLOR):
            collidables.append(Object(defines.BLOCK_SIZE, defines.BLOCK_SIZE, defines.GROUND_LIGHT_IMG, defines.GROUND_DARK_IMG, *(defines.index_to_postition(row, col))))
        if(level.get_at((row, col)) == defines.WALL_COLOR):
            collidables.append(Object(defines.BLOCK_SIZE, defines.BLOCK_SIZE, defines.WALL_LIGHT_IMG, defines.WALL_DARK_IMG, *(defines.index_to_postition(row, col))))

# player / enemy setup
player: Player = Player(defines.PLAYER_WIDTH, defines.PLAYER_HEIGHT, defines.PLAYER_SPRITE, *(100, 10))
enemy: Enemy = Enemy(defines.ENEMY_WIDTH, defines.ENEMY_HEIGHT, defines.ENEMY_SPRITE_LIGHT, defines.ENEMY_SPRITE_DARK, *(10, 10))

# pass objects to render
render = render.Render(collidables, player, enemy, score)

# clock
clock = pygame.time.Clock()
dim_timer = 0
blink_timer = 0
dt : int = 0

# main game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            running = False

    if(defines.DEBUG_MODE):
        print(GAME_STATE)

    keys = pygame.key.get_pressed()
    old_state = State.LIGHT
    if(keys[pygame.K_p]):
        if(GAME_STATE != State.PAUSE):
            old_state = GAME_STATE
            GAME_STATE = State.PAUSE
        else:
            GAME_STATE = old_state

    if GAME_STATE == State.PAUSE:
        continue

    # gameover logic
    if GAME_STATE == State.GAMEOVER:
        continue

    # run score counter
    score = int(pygame.time.get_ticks() / 1000)

    # run tick on player / enemy
    player.on_update(dt, collidables)
    enemy.on_update(dt, player)

    # check loss condition
    if(player.rect.colliderect(enemy.rect)):
        render.draw_score(score)
        render.draw_lose()
        GAME_STATE = State.GAMEOVER

    dt = clock.tick(60) // 1000
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    # do rendering
    # start in light
    if GAME_STATE == State.LIGHT:
        render.draw_light(score)

        GAME_STATE = State.DIMMING
        dim_timer = pygame.time.get_ticks()
        continue

    if GAME_STATE == State.DIMMING:
        # give alpha to render
        x = abs(1 - (dim_timer + defines.DIM_TIME - pygame.time.get_ticks()) / (defines.DIM_TIME))
        render.draw_dimming(x, score)
        # if dimming timer is over, move to dark
        if (pygame.time.get_ticks() > dim_timer + defines.DIM_TIME):
            GAME_STATE = State.DARK
            blink_timer = pygame.time.get_ticks()
            continue

    if GAME_STATE == State.DARK:
        render.draw_dark(score)
        # if last blink was long enough ago, move to light
        if (pygame.time.get_ticks() > blink_timer + defines.BLINK_TIME):
            GAME_STATE = State.LIGHT
            continue


pygame.quit()
