import pygame
import sys

import customparser

from sprite import *
from button import *

from simple_controller import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)

        self.controller = SimpleController()

        self.score = 0
        self.current_percept = None
        self.log = []
        self.map = []

        self.load_data()

    def load_data(self):
        self.map = customparser.read_map("test_input.txt")
        customparser.infer_information(self.map)
        self.num_height = len(self.map)
        self.num_width = len(self.map[0])
        self.offset_x = (960 - self.num_width * ROOM_SIZE) // 2
        self.offset_y = (WINDOW_SIZE[1] - self.num_height * ROOM_SIZE) // 2

    def new(self):
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(offset_x=self.offset_x, offset_y=self.offset_y))
        self.wumpus_group = pygame.sprite.Group()
        self.pit_group = pygame.sprite.Group()
        self.stench_group = pygame.sprite.Group()
        self.breeze_group = pygame.sprite.Group()
        self.treasure_group = pygame.sprite.Group()


        self.draw_object()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.consume()
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game
        self.player.update()

        for ele in self.wumpus_group:
            ele.kill()

        for ele in self.pit_group:
            ele.kill()

        for ele in self.stench_group:
            ele.kill()

        for ele in self.breeze_group:
            ele.kill()

        for ele in self.treasure_group:
            ele.kill()

        self.draw_object()

    def draw_grid(self, offset_x, offset_y):
        width = self.num_width * ROOM_SIZE
        height = self.num_height * ROOM_SIZE

        for x in range(0, width, ROOM_SIZE):
            pygame.draw.line(self.screen, WHITE, (x + offset_x, offset_y), (x + offset_x, height + offset_y))
        pygame.draw.line(self.screen, WHITE, (width + offset_x, offset_y), (width + offset_x, height + offset_y))

        for y in range(0, height, ROOM_SIZE):
            pygame.draw.line(self.screen, WHITE, (offset_x, y + offset_y), (width + offset_x, y + offset_y))
        pygame.draw.line(self.screen, WHITE, (offset_x, height + offset_y), (width + offset_x, height + offset_y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid(offset_x=self.offset_x, offset_y=self.offset_y)

        self.wumpus_group.draw(self.screen)
        self.pit_group.draw(self.screen)
        self.stench_group.draw(self.screen)
        self.breeze_group.draw(self.screen)
        self.treasure_group.draw(self.screen)


        self.player.draw(self.screen)

        self.draw_notification_rect()

        self.draw_log()
        self.draw_percept()
        self.draw_text(f"Log", get_font(30), (0, 0, 255), WINDOW_SIZE[0] - 150, 60)
        self.draw_text(f"Percept", get_font(30), (0, 0, 255), WINDOW_SIZE[0] - 150, 500)
        self.draw_text(f"Score:{self.score}", get_font(30), (0, 0, 255), WINDOW_SIZE[0] - 150, 20)

        pygame.display.update()

    def draw_notification_rect(self):
        notification_surf = pygame.Surface((320, 720))
        notification_surf.fill(GREY)
        notification_rect = notification_surf.get_rect(topright=(WINDOW_SIZE[0], 0))
        self.screen.blit(notification_surf, notification_rect)

    def draw_percept(self):
        percept_surf = pygame.Surface((300, 250))
        percept_surf.fill(WHITE)
        precept_rect = percept_surf.get_rect(bottomright=(WINDOW_SIZE[0] - 10, WINDOW_SIZE[1] - 10))
        self.screen.blit(percept_surf, precept_rect)

        y_position = 530
        for p in self.current_percept:
            self.draw_text(p, get_font(20), BLACK, WINDOW_SIZE[0] - 150, y_position)
            y_position += 20

    def draw_log(self):
        log_surf = pygame.Surface((300, 350))
        log_surf.fill(WHITE)
        log_rect = log_surf.get_rect(topright=(WINDOW_SIZE[0] - 10, 40))
        self.screen.blit(log_surf, log_rect)
        y_position = 90
        for l in self.log:
            self.draw_text(l, get_font(20), BLACK, WINDOW_SIZE[0] - 150, y_position)
            y_position += 20

    def draw_object(self):
        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if "W" in tile:
                    self.wumpus_group.add(Wumpus(col, row, offset_x=self.offset_x, offset_y=self.offset_y))
                if "P" in tile:
                    self.pit_group.add(Pit(col, row, offset_x=self.offset_x, offset_y=self.offset_y))
                if "S" in tile:
                    self.pit_group.add(Stench(col, row, offset_x=self.offset_x, offset_y=self.offset_y))
                if "B" in tile:
                    self.pit_group.add(Breeze(col, row, offset_x=self.offset_x, offset_y=self.offset_y))
                if "G" in tile:
                    self.pit_group.add(Treasure(col, row, offset_x=self.offset_x, offset_y=self.offset_y))

    def draw_text(self, text, font, text_color, x, y):
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def consume(self):
        info = self.controller.get_action()
        if len(info) > 0:
            self.player.sprite.move_to(info["position"][::-1])
            self.score = info["score"]
            self.log.append(info["log"])
            self.current_percept = info["percept"]
            if info["shoot"] == 1:
                self.player.sprite.shoot(False)
            if info["grab"] == 1:
                self.player.sprite.grab()
            self.map = info["map"]
            self.player.sprite.rotate(info["direction"])

    def main_menu(self):
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(WINDOW_SIZE[0] / 2, 150))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WINDOW_SIZE[0] / 2, 350),
                                 text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WINDOW_SIZE[0] / 2, 500),
                                 text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.run()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


# create the game object
g = Game()
while True:
    g.new()
    g.main_menu()

