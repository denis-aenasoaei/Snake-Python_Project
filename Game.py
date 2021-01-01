import GLOBALS as g
import pygame
from Snake import Snake
from Food import Food

class Game:
    def __init__(self, path_to_json):
        self.score = 0
        self.maxScore = 0
        self.baseGrid = self.init_grid(path_to_json)
        self.grid = self.baseGrid.copy()

    def init_grid(self, json_file):
        grid = []
        for i in range(g.grid_size):
            grid.append([])
            for j in range(g.grid_size):
                grid[i].append(-1)
        return grid


    def drawGrid(self, surface):
        # use the grid to draw the walls
        for y in range(0, int(g.grid_size)):
            for x in range(0, int(g.grid_size)):
                if (x+y) % 2 == 0:
                    r = pygame.Rect((x*g.block_width, y*g.block_height), (g.block_width, g.block_height))
                    pygame.draw.rect(surface, (93, 216, 228), r)
                else:
                    rr = pygame.Rect((x * g.block_width, y * g.block_height), (g.block_width, g.block_height))
                    pygame.draw.rect(surface, (84, 194, 205), rr)

    def runGame(self):
        snake = Snake(self.grid)
        food = Food()

        pygame.init()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((g.screen_width, g.screen_height), flags=pygame.SCALED, depth=32, vsync=True)

        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        self.drawGrid(surface)

        food.randomize_position(self.grid)
        myfont = pygame.font.SysFont("monospace", 16)
        snake.draw(surface)
        while True:
            clock.tick(10)
            snake.handle_keys()
            self.drawGrid(surface)
            if not snake.move(self.grid):
                self.grid = self.baseGrid
                # scores check
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position(self.grid)
            snake.draw(surface)
            food.draw(surface)
            screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(self.score), True, (0, 0, 0))
            screen.blit(text, (5, 10))
            pygame.display.update()


game = Game("filler")
game.runGame()