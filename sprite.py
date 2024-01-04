from enum import Enum

import pygame.draw
from enum import IntEnum

# Color defined
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (224, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)

# Pygame define
WINDOW_SIZE = (1280, 720)
ROOM_SIZE = 48
FPS = 1
TITLE = "WUMPUS WORLD"
BGCOLOR = BLACK
BG = pygame.image.load("assets/background.png")
BG = pygame.transform.scale(BG, WINDOW_SIZE)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class DIRECTION(IntEnum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image = pygame.transform.scale(image, (scale, scale))
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        # sprite
        self.game = game
        self.groups = game.player_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        player_down = pygame.image.load('assets/down.png').convert_alpha()
        player_down = pygame.transform.scale(player_down, (ROOM_SIZE, ROOM_SIZE))
        player_up = pygame.image.load('assets/up.png').convert_alpha()
        player_up = pygame.transform.scale(player_up, (ROOM_SIZE, ROOM_SIZE))
        player_left = pygame.image.load('assets/left.png').convert_alpha()
        player_left = pygame.transform.scale(player_left, (ROOM_SIZE, ROOM_SIZE))
        player_right = pygame.image.load('assets/right.png').convert_alpha()
        player_right = pygame.transform.scale(player_right, (ROOM_SIZE, ROOM_SIZE))

        player_shoot_left = pygame.image.load('assets/shoot_left.png').convert_alpha()
        player_shoot_left = pygame.transform.scale(player_shoot_left, (ROOM_SIZE, ROOM_SIZE))
        player_shoot_right = pygame.image.load('assets/shoot_right.png').convert_alpha()
        player_shoot_right = pygame.transform.scale(player_shoot_right, (ROOM_SIZE, ROOM_SIZE))
        player_shoot_up = pygame.image.load('assets/shoot_up.png').convert_alpha()
        player_shoot_up = pygame.transform.scale(player_shoot_up, (ROOM_SIZE, ROOM_SIZE))
        player_shoot_down = pygame.image.load('assets/shoot_down.png').convert_alpha()
        player_shoot_down = pygame.transform.scale(player_shoot_down, (ROOM_SIZE, ROOM_SIZE))

        player_grab = pygame.image.load('assets/grab.png').convert_alpha()
        self.player_grab = pygame.transform.scale(player_grab, (ROOM_SIZE, ROOM_SIZE))

        self.player_shoot = [player_shoot_right, player_shoot_left, player_shoot_up, player_shoot_down]

        self.player_move = [player_right, player_left, player_up, player_down]
        self.image = self.player_move[direction]
        self.rect = self.image.get_rect()

        # logic
        self.x = x
        self.y = y
        self.direction = direction
        self.offset_x = game.offset_x
        self.offset_y = game.offset_y
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, direction):
        self.direction = direction



    def update(self, is_shoot, is_grab):
        self.rect.x = self.x * ROOM_SIZE + self.offset_x
        self.rect.y = self.y * ROOM_SIZE + self.offset_y

        if is_grab:
            self.image = self.player_grab
        else:
            if self.direction == DIRECTION.DOWN:
                if is_shoot:
                    self.image = self.player_shoot[3]
                else:
                    self.image = self.player_move[3]

            elif self.direction == DIRECTION.UP:
                if is_shoot:
                    self.image = self.player_shoot[2]
                else:
                    self.image = self.player_move[2]
            elif self.direction == DIRECTION.LEFT:
                if is_shoot:
                    self.image = self.player_shoot[1]
                else:
                    self.image = self.player_move[1]
            else:
                if is_shoot:
                    self.image = self.player_shoot[0]
                else:
                    self.image = self.player_move[0]

class Wumpus(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.wumpus_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/wumpus.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y


class Pit(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.pit_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/pit.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y


class Stench(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.stench_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/stench.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y


class Breeze(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.breeze_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/breeze.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y


class Treasure(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.treasure_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/treasure-chest.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + game.offset_x
        self.rect.y = y * ROOM_SIZE + game.offset_y


class ExitRoom(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.exit_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('assets/exit.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE/2, ROOM_SIZE/2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x * ROOM_SIZE + game.offset_x
        self.rect.centery = y * ROOM_SIZE + game.offset_y
