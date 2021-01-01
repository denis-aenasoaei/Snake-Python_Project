import GLOBALS as g
import pygame
from Snake import Snake
from Food import Food
import json
from copy import deepcopy

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

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((g.screen_width, g.screen_height), flags=pygame.SCALED, depth=32, vsync=True)

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()

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


    def drawGrid(self):
        for y in range(0, int(self.settings['gridSize'])):
            for x in range(0, int(self.settings['gridSize'])):
                if self.grid[x][y] == -1:
                    if (x+y) % 2 == 0:
                        r = pygame.Rect((x*g.block_width, y*g.block_height), (g.block_width, g.block_height))
                        pygame.draw.rect(self.surface, (93, 216, 228), r)
                    else:
                        rr = pygame.Rect((x * g.block_width, y * g.block_height), (g.block_width, g.block_height))
                        pygame.draw.rect(self.surface, (84, 194, 205), rr)
                elif self.grid[x][y] == g.WALL:
                    rr = pygame.Rect((x * g.block_width, y * g.block_height), (g.block_width, g.block_height))
                    pygame.draw.rect(self.surface, (0, 0, 0), rr)

    def runGame(self):
        self.drawGrid()
        self.food.randomize_position(self.grid)
        myfont = pygame.font.SysFont("monospace", 16)
        self.snake.draw(self.surface)
        while True:
            self.clock.tick(10)
            self.snake.handle_keys()
            self.drawGrid()
            if not self.snake.move(self.grid):
                self.grid = deepcopy(self.baseGrid)
                self.snake.initializeSnakeOnGrid(self.grid)
                if self.score > self.maxScore:
                    self.maxScore = self.score

                self.score = 0

            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.score += 1
                self.food.randomize_position(self.grid)
            self.snake.draw(self.surface)
            self.food.draw(self.surface)
            self.screen.blit(self.surface, (0, 0))
            text = myfont.render("Score {0}".format(self.score), True, (0, 0, 0))
            self.screen.blit(text, (5, 10))
            pygame.display.update()


game = Game("settings.json")
game.runGame()
'''
settings = {}
settings['gridSize'] = 20
settings['startSize'] = 3
settings['walls'] = [[2,1],[3,2],[3,3],[5,1],[5,2],[18,5]]
with open('settings.json', 'w') as f:
    json.dump(settings, f)
'''