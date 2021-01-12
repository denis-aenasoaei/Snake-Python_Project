import pygame
import sys
import GLOBALS as g


class Snake:
    def __init__(self, grid, initial_size):
        self.initialSize = initial_size
        self.length = initial_size
        self.positions = []
        self.initializeSnakeOnGrid(grid)
        self.direction = g.right

    def initializeSnakeOnGrid(self, grid):
        for i in range(self.initialSize):
            self.positions.append(((len(grid) // 2) - i, (len(grid) // 2)))
            grid[self.positions[i][0]][self.positions[i][1]] = g.PLAYER

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction

    def move(self, grid):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)

        if not(0 <= new[0] < len(grid)) or not(0 <= new[1] < len(grid)) or grid[new[0]][new[1]] in [g.PLAYER, g.WALL]:
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

    def handle_keys(self):
        handled = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not handled:
                if event.key == pygame.K_UP:
                    self.turn(g.up)
                    handled = True
                elif event.key == pygame.K_DOWN:
                    self.turn(g.down)
                    handled = True
                elif event.key == pygame.K_LEFT:
                    self.turn(g.left)
                    handled = True
                elif event.key == pygame.K_RIGHT:
                    self.turn(g.right)
                    handled = True
            elif handled and event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                pygame.event.post(event)
                break
