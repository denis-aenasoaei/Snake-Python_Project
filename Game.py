import GLOBALS as g
import pygame
from Snake import Snake
from Food import Food
import json
from copy import deepcopy
from sys import exit


class Game:
    def __init__(self, path_to_json):
        self.score = 0
        self.maxScore = 0

        with open(path_to_json) as f:
            self.settings = json.load(f)

        self.baseGrid = self.init_grid()
        self.grid = deepcopy(self.baseGrid)
        self.snake = Snake(self.grid, self.settings['startSize'])
        self.food = Food()

        pygame.init()
        pygame.display.set_caption('Snake!')
        snakeImage = pygame.image.load('snake-icon.png')
        pygame.display.set_icon(snakeImage)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]),
                                              flags=pygame.SCALED, depth=32, vsync=True)
        self.block_width = self.settings["screen_width"] / self.settings["gridSize"]
        self.block_height = self.settings["screen_height"] / self.settings["gridSize"]
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.font = pygame.font.SysFont("monospace", 18)

    def init_grid(self):
        grid = []
        for i in range(self.settings['gridSize']):
            grid.append([])
            for j in range(self.settings['gridSize']):
                if [j, i] in self.settings['walls']:
                    grid[i].append(g.WALL)
                else:
                    grid[i].append(g.EMPTY)
        return grid

    def drawGrid(self, darken):
        for x in range(0, int(self.settings['gridSize'])):
            for y in range(0, int(self.settings['gridSize'])):
                if self.grid[x][y] == g.EMPTY:
                    if (x + y) % 2 == 0:
                        r = pygame.Rect((x * self.block_width, y * self.block_height),
                                        (self.block_width, self.block_width))
                        pygame.draw.rect(self.surface, (93 * darken, 216 * darken, 228 * darken), r)
                    else:
                        rr = pygame.Rect((x * self.block_width, y * self.block_width),
                                         (self.block_width, self.block_width))
                        pygame.draw.rect(self.surface, (84 * darken, 194 * darken, 205 * darken), rr)
                elif self.grid[x][y] == g.WALL:
                    rr = pygame.Rect((x * self.block_width, y * self.block_width), (self.block_width, self.block_width))
                    pygame.draw.rect(self.surface, (175 * darken, 34 * darken, 6 * darken), rr)
                elif self.grid[x][y] == g.PLAYER:
                    r = pygame.Rect((x * self.block_width, y * self.block_height),
                                    (self.block_width, self.block_height))
                    pygame.draw.rect(self.surface, (17 * darken, 24 * darken, 47 * darken), r)
                    pygame.draw.rect(self.surface, (93, 216, 228), r, 1)
                elif self.grid[x][y] == g.FOOD:
                    r = pygame.Rect((x * self.block_width, y * self.block_height),
                                    (self.block_width, self.block_height))
                    pygame.draw.rect(self.surface, (223 * darken, 163 * darken, 49 * darken), r)
                    pygame.draw.rect(self.surface, (93, 216, 228), r, 1)

    def runGame(self):
        self.food.randomize_position(self.grid)
        while True:
            self.clock.tick(10)
            self.snake.handle_keys()
            if not self.snake.move(self.grid):
                if self.endGameDialog() == 0:
                    exit()
                else:
                    self.score = 0
                    self.grid = deepcopy(self.baseGrid)
                    self.snake.initializeSnakeOnGrid(self.grid)
                    self.food.randomize_position(self.grid)

            self.drawGrid(1)

            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.score += 1
                self.food.randomize_position(self.grid)
                if self.score > self.maxScore:
                    self.maxScore = self.score

            self.screen.blit(self.surface, (0, 0))
            score = self.font.render("Score {0}".format(self.score), True, (0, 0, 0))
            self.screen.blit(score, (5, 10))
            pygame.display.update()

    def endGameDialog(self):
        retry_button = pygame.Rect((self.settings["screen_width"] / 2 - 75, 170), (150, 25))
        play_again = self.font.render('Play Again!', True, (255, 250, 106))

        quit_button = pygame.Rect((self.settings["screen_width"] / 2 - 75, 250), (150, 25))
        quit_text = self.font.render('Quit!', True, (255, 250, 106))
        while True:
            self.clock.tick(10)
            self.drawGrid(0.4)  # darken shade for every block
            pygame.draw.rect(self.surface, (0, 0, 0), retry_button)
            pygame.draw.rect(self.surface, (0, 0, 0), quit_button)
            self.screen.blit(self.surface, (0, 0))

            current_score = self.font.render("Score {0}".format(self.score), True, (6, 255, 43))
            best_score = self.font.render("Max Score {0}".format(self.maxScore), True, (6, 255, 43))

            self.screen.blit(current_score, (self.settings["screen_width"] / 4 - 50, 100))
            self.screen.blit(best_score, (self.settings["screen_width"] / 2 + 50, 100))

            self.screen.blit(play_again, (retry_button.left +
                                          (retry_button.width / 2 - play_again.get_width() / 2),
                                          retry_button.top +
                                          (retry_button.height / 2 - play_again.get_height() / 2))
                             )

            self.screen.blit(quit_text, (quit_button.left +
                                         (quit_button.width / 2 - quit_text.get_width() / 2),
                                         quit_button.top +
                                         (quit_button.height / 2 - quit_text.get_height() / 2))
                             )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if retry_button.collidepoint(mouse_pos):
                        return 1
                    if quit_button.collidepoint(mouse_pos):
                        return 0


game = Game("settings.json")
game.runGame()