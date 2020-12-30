import pygame
import sys
import random
import GLOBALS as g

class Snake:
    def __init__(self, grid):
        self.length = 2
        self.positions = []
        for i in range(g.initial_size):
            self.positions.append(((g.grid_size // 2) - i, (g.grid_size // 2)))
            grid[self.positions[i][0]][self.positions[i][1]] = g.PLAYER

        self.direction = g.right
        self.color = (17, 24, 47)
        self.score = 0

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

        if len(self.positions) > 2 and new in self.positions[2:] or not(0 <= new[0] < g.grid_size) \
                or not(0 <= new[1] < g.grid_size):
            self.reset()
            return 0
        else:
            self.positions.insert(0, new)
            grid[new[0]][new[1]] = g.PLAYER
            if len(self.positions) > self.length:
                tail = self.positions.pop()
                grid[tail[0]][tail[1]] = -1
        return 1


    def reset(self):
        self.length = g.initial_size
        self.positions = []
        for i in range(g.initial_size):
            self.positions.append(((g.grid_size // 2) - i, (g.grid_size // 2)))
        self.direction = g.right
        self.score = 0
        #add max score check

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
