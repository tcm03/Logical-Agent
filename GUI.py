import time

import pygame
import sys

import customparser

from tkinter.filedialog import askopenfilename
from tkinter import *

from sprite import *
from button import *

from simple_controller import *

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.arrow_hit_sound = pygame.mixer.Sound("assets/arrow_hit.mp3")
        self.arrow_miss_sound = pygame.mixer.Sound("assets/arrow_miss.mp3")
        self.grab_sound = pygame.mixer.Sound("assets/grab.mp3")
        self.scream_sound = pygame.mixer.Sound("assets/screaming.mp3")

    def play_shoot(self, is_shoot, is_hit):
        if is_shoot:
            self.play_arrow()
        if is_hit:
            self.play_scream()


    def play_arrow(self):
        # self.arrow_hit_sound.play()
        self.arrow_miss_sound.play()
        pygame.time.wait(int(self.arrow_miss_sound.get_length() * 1000))

    def play_grab(self, is_grab):
        if is_grab:
            self.grab_sound.play()
            pygame.time.wait(int(self.grab_sound.get_length() * 1000))

    def play_scream(self):
        self.scream_sound.play()
        pygame.time.wait(int(self.scream_sound.get_length() * 1000))


class Game:
    def __init__(self):
        # set configuration
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.sound_effect = Sound()

        # initialize sprites
        self.wumpus_group = pygame.sprite.Group()
        self.pit_group = pygame.sprite.Group()
        self.stench_group = pygame.sprite.Group()
        self.breeze_group = pygame.sprite.Group()
        self.treasure_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.GroupSingle()
        self.player_group = pygame.sprite.GroupSingle()
        # information


        # self.load_data()

    # def initilize_game(self):

    def load_data(self, controller):
        self.controller = controller
        self.size = controller.size
        self.offset_x = (960 - self.size * ROOM_SIZE) // 2
        self.offset_y = (WINDOW_SIZE[1] - self.size * ROOM_SIZE) // 2

        self.score = 0
        self.current_percept = None
        self.action_log = []
        self.map = []
        self.player_position = (0, 0)
        self.player_direction = DIRECTION.RIGHT

        self.player = Player(self, x=self.player_position[0], y=self.player_position[1], direction=self.player_direction)

        ExitRoom(self, x=0.5, y=self.size-0.5)

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
        self.kill_object()
        self.create_object()
        self.player.update()


    def draw_grid(self):
        width = self.size * ROOM_SIZE
        height = self.size * ROOM_SIZE

        for x in range(0, width, ROOM_SIZE):
            pygame.draw.line(self.screen, WHITE, (x + self.offset_x, self.offset_y),
                             (x + self.offset_x, height + self.offset_y))
        pygame.draw.line(self.screen, WHITE, (width + self.offset_x, self.offset_y),
                         (width + self.offset_x, height + self.offset_y))

        for y in range(0, height, ROOM_SIZE):
            pygame.draw.line(self.screen, WHITE, (self.offset_x, y + self.offset_y),
                             (width + self.offset_x, y + self.offset_y))
        pygame.draw.line(self.screen, WHITE, (self.offset_x, height + self.offset_y),
                         (width + self.offset_x, height + self.offset_y))

    def draw_object(self):
        self.stench_group.draw(self.screen)
        self.breeze_group.draw(self.screen)
        self.pit_group.draw(self.screen)
        self.wumpus_group.draw(self.screen)
        self.treasure_group.draw(self.screen)
        self.exit_group.draw(self.screen)
        self.player_group.draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()


        self.draw_notification_rect()

        self.draw_log()
        self.draw_percept()
        # self.sound_effect.play_shoot(self.current_shoot[0], self.current_shoot[1])
        # self.sound_effect.play_grab(self.current_grab)

        self.draw_object()
        self.draw_text(f"Score:{self.score}", get_font(30), (0, 0, 0), WINDOW_SIZE[0] - 150, 20)
        # pygame.draw.line(self.screen, (255, 0, 0), (320, 80), (320, 100), 5)
        # pygame.draw.line(self.screen, (255, 0, 0), (60, 80), (130, 100), 5)
        pygame.display.flip()


    def draw_notification_rect(self):
        notification_surf = pygame.Surface((320, 720))
        notification_surf.fill(GREY)
        notification_rect = notification_surf.get_rect(topright=(WINDOW_SIZE[0], 0))
        self.screen.blit(notification_surf, notification_rect)

    def draw_percept(self):
        self.draw_text(f"Percept", get_font(30), (0, 0, 255), WINDOW_SIZE[0] - 160, 420)
        percept_surf = pygame.Surface((300, 180))
        percept_surf.fill(WHITE)
        precept_rect = percept_surf.get_rect(topright=(WINDOW_SIZE[0] - 10, 450))
        self.screen.blit(percept_surf, precept_rect)
        y_position = 470
        for p in self.current_percept:
            self.draw_text(p, get_font(20), BLACK, WINDOW_SIZE[0] - 10 - 150, y_position)
            y_position += 25

    def draw_log(self):
        self.draw_text(f"Log", get_font(30), (0, 0, 255), WINDOW_SIZE[0] - 160, 70)
        log_surf = pygame.Surface((300, 260))
        log_surf.fill(WHITE)
        log_rect = log_surf.get_rect(topright=(WINDOW_SIZE[0] - 10, 100))
        self.screen.blit(log_surf, log_rect)
        y_position = 120
        for l in self.action_log[-10:]:
            self.draw_text(str(l), get_font(20), BLACK, WINDOW_SIZE[0] - 10 - 150, y_position)
            y_position += 25

    def create_object(self):
        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if "W" in tile:
                    Wumpus(self, col, row)
                if "P" in tile:
                    Pit(self, col, row)
                if "S" in tile:
                    Stench(self, col, row)
                if "B" in tile:
                    Breeze(self, col, row)
                if "G" in tile:
                    Treasure(self, col, row)


    def kill_object(self):
        for sprite in self.wumpus_group:
            sprite.kill()

        for sprite in self.pit_group:
            sprite.kill()

        for sprite in self.stench_group:
            sprite.kill()

        for sprite in self.breeze_group:
            sprite.kill()

        for sprite in self.treasure_group:
            sprite.kill()

    def draw_text(self, text, font, text_color, x, y):
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.main_menu()

    def consume(self):
        info = self.controller.get_information()
        if len(info) > 0:
            player_position = info["position"][::-1]
            self.player.move_to(player_position[0], player_position[1])
            self.player.rotate(info["direction"])

            self.score = info["score"]
            self.action_log.append(info["action"])
            self.current_percept = info["percept"]
            self.current_shoot = info["shoot"]
            self.current_grab = info["grab"]
            self.map = info["map"]

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
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        root = Tk()
                        root.withdraw()
                        file_dir = askopenfilename()
                        root.destroy()
                        print(file_dir)
                        controller = SimpleController()
                        controller.solver(file_dir)
                        # print(controller.get_percept())
                        self.load_data(controller=controller)
                        self.run()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.quit()

            pygame.display.update()


# create the game object
# controller = SimpleController()
g = Game()
while True:
    g.main_menu()
