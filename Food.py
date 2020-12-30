import pygame
import random
import GLOBALS as g

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)

    def randomize_position(self, grid):
        while 1:
            self.position = (random.randint(0, g.grid_size-1), random.randint(0, g.grid_size-1))
            if grid[self.position[0]][self.position[1]] != g.PLAYER:
                break

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * g.block_width, self.position[1] * g.block_height), (g.block_width, g.block_height))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)