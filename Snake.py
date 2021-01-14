import GLOBALS as g


class Snake:

    """Player class for the Snake! game"""
    def __init__(self, grid, initial_size=2):
        """
        Initializes a new snake.
        :param grid: List of lists of dimension NxN, with grid values.
        :param initial_size: int, optional
            The initial size the Snake should take values between 2 and half the grid size
        """
        if not(2 < initial_size < len(grid)//2):
            initial_size = 2
        # directions the snake can take
        self.up = (0, -1)
        self.down = (0, 1)
        self.left = (-1, 0)
        self.right = (1, 0)

        self.initial_size = initial_size
        self.length = initial_size
        self.positions = []
        self.initialize_snake_on_grid(grid)
        self.direction = self.right

    def initialize_snake_on_grid(self, grid):
        """
        Places the snake onto a grid.
        :param grid: The NxN grid that will be modified to contain the Snake
        """
        for i in range(self.initial_size):
            self.positions.append(((len(grid) // 2) - i, (len(grid) // 2)))
            grid[self.positions[i][0]][self.positions[i][1]] = g.PLAYER

    def get_head_position(self):
        """
        Gets the x and y coordinates of the snake head.
        :return: Tuple of x and y board coordinates with the snake's head position
        """
        return self.positions[0]

    def turn(self, direction):
        """
        Turns the snake direction.
        :param direction: The direction to turn to.
        :return: 0, if the turn in impossible (is not a 180° turn)
                 1, otherwise
        """
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return 0
        else:
            self.direction = direction
            return 1

    def move(self, grid):
        """
        Moves the snake in the direction described by direction attribute.
        :param grid: The grid where the snake should be moved on
        :return: 0, if the new position is not possible, resulting in the snake's death
                 1, if the new position is valid
        """
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
        """Resets the snake's attributes to a base, making it ready for a new round."""
        self.length = self.initial_size
        self.positions = []
        self.direction = self.right
