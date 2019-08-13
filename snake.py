from random import randint
from pygame.locals import *
import pygame
import time
import sys

step = 44
player_img = "player.png"
food_img = "food.png"


class Player:
    # snake controlling
    x = [0]
    y = [0]
    direction = 0
    length = 1
    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-200)
            self.y.append(-100)
        self.x[1] = 1 * step
        self.x[2] = 2 * step

    def update(self):

        # get coord
        self.updateCount += 1
        if self.updateCount > self.updateCountMax:
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

    # movement

            if self.direction == 0:
                self.x[0] += step
            if self.direction == 1:
                self.x[0] -= step
            if self.direction == 2:
                self.y[0] -= step
            if self.direction == 3:
                self.y[0] += step

            self.updateCount = 0

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    # get pixel and displays the player image on background
    def draw(self, background, __player_img):
        for i in range(self.length):
            background.blit(__player_img, (self.x[i], self.y[i]))


class Food:
    x = 0
    y = 0

    # displays food
    def __init__(self, x, y):
        self.x = x * step
        self.y = y * step

    def draw(self, background, __food_img):
        background.blit(__food_img, (self.x, self.y))


class Collision:
    # get collision with snake and food
    # noinspection PyMethodMayBeStatic
    def is_collision(self, x_food, y_food, x_player, y_player, bsize):
        if x_food <= x_player <= x_player + bsize:
            if y_food <= y_player <= y_player + bsize:
                print("collided at: " + str(x_player) + " / " + str(y_player))
                return True
        return False


class DisplayText:
    def __init__(self, text, screen):
        font = pygame.font.SysFont("Arial", 30)
        text_bg = font.render(text, False, (0, 0, 0))
        screen.blit(text_bg, (0, 0))


class Game:
    # set up the desktop environment
    window_width = 800
    window_height = 600
    player = 0
    food = 0

    def __init__(self):
        self._running = True
        self._display_ = None
        self._player_img_ = None
        self._food_img_ = None
        self.collision = Collision()
        self.player = Player(1)
        self.food = Food(5, randint(3, 10))

    def on_init(self):
        pygame.init()
        pygame.font.init()
        print("started")
        self._display_ = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)

        pygame.display.set_caption("Snake by Benjamin")
        self._running = True

        # loads assets
        self._player_img_ = pygame.image.load(player_img).convert()
        self._food_img_ = pygame.image.load(food_img).convert()

    def on_loop(self):
        self.player.update()
        # get collision
        for i in range(0, self.player.length):
            if self.collision.is_collision(self.food.x, self.food.y, self.player.x[i], self.player.y[i], step):
                self.food.x = randint(2, 9) * step
                self.food.y = randint(2, 9) * step
                self.player.length += 1

        for k in range(2, self.player.length):
            if self.collision.is_collision(self.player.x[0], self.player.y[0], self.player.x[k], self.player.y[k], 40):
                # Here I want to add a text box with DisplayText("Lost at: Player Length", screen)
                print("Lost at: " + str(self.player.length))
                time.sleep(2)
                self.on_cleanup()
        pass

    def on_render(self):
        self._display_.fill((0, 0, 0))
        self.player.draw(self._display_, self._player_img_)
        self.food.draw(self._display_, self._food_img_)
        pygame.display.flip()

    # noinspection PyMethodMayBeStatic
    def on_cleanup(self):
        print("exited")
        pygame.quit()
        sys.exit()

    def on_exec(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            event = pygame.event.wait()

            if keys[K_RIGHT]:
                self.player.move_right()
            if keys[K_LEFT]:
                self.player.move_left()
            if keys[K_UP]:
                self.player.move_up()
            if keys[K_DOWN]:
                self.player.move_down()
            if keys[K_ESCAPE]:
                self._running = False
            if event.type == pygame.QUIT:
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        self.on_cleanup()


if __name__ == "__main__":
    game = Game()
    game.on_exec()
