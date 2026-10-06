import pygame
import os

def index_to_postition(row: int, col: int) -> tuple[int, int]:
    return ((16 * row), (16 * col))

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

DISPLAY_RESOLUTION = (1280, 720)
INTERNAL_RESOLUTION = (256, 144)

# assets
WALL_LIGHT_IMG = pygame.image.load(os.path.join("assets", "images", "wall_light.png"))
WALL_DARK_IMG = pygame.image.load(os.path.join("assets", "images", "wall_dark.png"))
GROUND_LIGHT_IMG = pygame.image.load(os.path.join("assets", "images", "ground_light.png"))
GROUND_DARK_IMG = pygame.image.load(os.path.join("assets", "images", "ground_dark.png"))

PLAYER_SPRITE = pygame.image.load(os.path.join("assets", "images", "player.png"))
ENEMY_SPRITE_LIGHT = pygame.image.load(os.path.join("assets", "images", "enemy_light.png"))
ENEMY_SPRITE_DARK = pygame.image.load(os.path.join("assets", "images", "enemy_dark.png"))

# player
PLAYER_WIDTH: int = 8
PLAYER_HEIGHT: int = 12
ACC = 0.4
GRAV = 0.1
FRIC = -0.12
JUMP = 2.3

# enemy
ENEMY_WIDTH: int = 13
ENEMY_HEIGHT: int = 14
ENEMY_ACC = 2

APP_ICON = ENEMY_SPRITE_LIGHT
BLINK_TIME: int = 1800
DIM_TIME: int = 1000

BLOCK_SIZE: int = 16

GROUND_COLOR = pygame.Color(255, 0, 0)
AIR_COLOR = pygame.Color(255, 255, 255)
WALL_COLOR = pygame.Color(0, 0, 0)



DEBUG_MODE: bool = False
COLLISION_TEST_COLOR1 = pygame.Color(0, 255, 0, 100)
COLLISION_TEST_COLOR2 = pygame.Color(255, 0, 255, 100)
