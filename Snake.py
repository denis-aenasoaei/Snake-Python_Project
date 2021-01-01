import pygame
import sys
import GLOBALS as g

class Snake:
    def __init__(self, grid, initialSize):
        self.initialSize = initialSize
        self.length = initialSize
        self.positions = []

        self.initializeSnakeOnGrid(grid)

        self.direction = g.right
        self.color = (17, 24, 47)

    def initializeSnakeOnGrid(self, grid):
        for i in range(self.initialSize):
            self.positions.append(((len(grid) // 2) - i, (len(grid) // 2)))
            grid[self.positions[i][0]][self.positions[i][1]] = g.PLAYER

    def get_head_position(self):
        return self.positions[0]

    def turn(self, dir):
        if self.length > 1 and (dir[0] * -1, dir[1] * -1) == self.direction:
            return
        else:
            self.direction = dir

    def move(self, grid):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)

        if not(0 <= new[0] < len(grid)) or not(0 <= new[1] < len(grid)) or grid[new[0]][new[1]] != g.EMPTY:
            self.reset()
            return 0
        else:
            self.positions.insert(0, new)
            grid[new[0]][new[1]] = g.PLAYER
            if len(self.positions) > self.length:
                tail = self.positions.pop()
                grid[tail[0]][tail[1]] = g.EMPTY
        return 1

    def reset(self):
        self.length = self.initialSize
        self.positions = []
        self.direction = g.right

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] * g.block_width, p[1] * g.block_height), (g.block_width, g.block_height))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(g.up)
                elif event.key == pygame.K_DOWN:
                    self.turn(g.down)
                elif event.key == pygame.K_LEFT:
                    self.turn(g.left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(g.right)
                break
