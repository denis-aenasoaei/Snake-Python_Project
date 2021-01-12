import pygame
import random
import GLOBALS as g

class Food():
    def __init__(self):
        self.position = (0,0)

    def randomize_position(self, grid):
        while 1:
            self.position = (random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1))
            if grid[self.position[0]][self.position[1]] == g.EMPTY:
                grid[self.position[0]][self.position[1]] = g.FOOD
                break