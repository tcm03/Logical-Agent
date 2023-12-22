from enum import Enum

import pygame.draw

# Color defined
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (224,255,255)
RED = (255, 0, 0)
GREEN = (34,139,34)
BLUE = (0, 0, 255)
GREY = (169,169,169)

# Pygame define
WINDOW_SIZE = (1280, 720)
ROOM_SIZE = 48
FPS = 1
TITLE = "WUMPUS WORLD"
BGCOLOR = BLACK
BG = pygame.image.load("assets/background.png")
BG = pygame.transform.scale(BG, WINDOW_SIZE)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

class DIRECTION(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Player(pygame.sprite.Sprite):
    def __init__(self, offset_x, offset_y, x=0, y=0, direction=DIRECTION.RIGHT):
        # sprite
        pygame.sprite.Sprite.__init__(self)
        player_down = pygame.image.load('assets/down.png').convert_alpha()
        player_down = pygame.transform.scale(player_down, (ROOM_SIZE, ROOM_SIZE))
        player_up = pygame.image.load('assets/up.png').convert_alpha()
        player_up = pygame.transform.scale(player_up, (ROOM_SIZE, ROOM_SIZE))
        player_left = pygame.image.load('assets/left.png').convert_alpha()
        player_left = pygame.transform.scale(player_left, (ROOM_SIZE, ROOM_SIZE))
        player_right = pygame.image.load('assets/right.png').convert_alpha()
        player_right = pygame.transform.scale(player_right, (ROOM_SIZE, ROOM_SIZE))
        self.player_move = [player_right, player_left, player_up, player_down]
        self.image = self.player_move[0]
        self.rect = self.image.get_rect()

        self.arrow_hit_sound = pygame.mixer.Sound("assets/arrow_hit.mp3")
        self.arrow_miss_sound = pygame.mixer.Sound("assets/arrow_miss.mp3")
        self.grab_sound = pygame.mixer.Sound("assets/grab.mp3")
        # logic
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.direction = direction

    def rotate(self, direction):
        self.direction = direction

    def move_to(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def shoot(self, is_hit):
        if is_hit:
            self.arrow_hit_sound.play()
        else:
            self.arrow_miss_sound.play()

    def grab(self):
        self.grab_sound.play()

    def update(self):
        self.rect.x = self.x * ROOM_SIZE + self.offset_x
        self.rect.y = self.y * ROOM_SIZE + self.offset_y
        if self.direction == DIRECTION.DOWN:
            self.image = self.player_move[3]
        elif self.direction == DIRECTION.UP:
            self.image = self.player_move[2]
        elif self.direction == DIRECTION.LEFT:
            self.image = self.player_move[1]
        else:
            self.image = self.player_move[0]


class Wumpus(pygame.sprite.Sprite):
    def __init__(self, x, y, offset_x, offset_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/wumpus.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + offset_x
        self.rect.y = y * ROOM_SIZE + offset_y


class Pit(pygame.sprite.Sprite):
    def __init__(self, x, y, offset_x, offset_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pit.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + offset_x
        self.rect.y = y * ROOM_SIZE + offset_y


class Stench(pygame.sprite.Sprite):
    def __init__(self, x, y, offset_x, offset_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/stench.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + offset_x
        self.rect.y = y * ROOM_SIZE + offset_y

class Breeze(pygame.sprite.Sprite):
    def __init__(self, x, y, offset_x, offset_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/breeze.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + offset_x
        self.rect.y = y * ROOM_SIZE + offset_y

class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y, offset_x, offset_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/treasure-chest.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ROOM_SIZE, ROOM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * ROOM_SIZE + offset_x
        self.rect.y = y * ROOM_SIZE + offset_y