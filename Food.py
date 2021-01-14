import random
import GLOBALS as g


class Food:
    """Keeps track of food in the Snake Game."""
    def __init__(self):
        """Instantiate a new food object."""
        self.position = (0, 0)

    def randomize_position(self, grid):
        """
        Randomizes the food position on the grid.
        :param grid: Two dimensional list with grid values, which will be modified to contain food at random coordinates
        """
        while 1:
            self.position = (random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1))
            if grid[self.position[0]][self.position[1]] == g.EMPTY:
                grid[self.position[0]][self.position[1]] = g.FOOD
                break
