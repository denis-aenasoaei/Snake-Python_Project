import GLOBALS as g
import pygame
from Snake import Snake
from Food import Food
import json
from copy import deepcopy
from sys import exit, argv


def end_game():
    """Closes the game and exits the program."""
    pygame.quit()
    exit()


class Game:
    """Game manager for the Snake game"""

    def __init__(self, path_to_json_settings=None):
        """
        Initializes a game object
        :param path_to_json_settings: string, optional
            Path to a json file containing game settings as follows:
                - screen_height in pixels
                - screen_width in pixels
                - grid_size, size of the board
                - start_size, initial size of the snake
                - walls, list of lists, with x and y coordinates of blocks to be blocked
        Will use default values for above variables if not provided.
        """
        self.score = 0
        self.maxScore = 0
        try:
            with open(path_to_json_settings) as f:
                self.settings = json.load(f)
        except TypeError:   # If file is not found, initialize with some basic settings
            self.settings = {"screen_height": 480, "screen_width": 480, "grid_size": 20, "start_size": 3, "walls": []}
        except FileNotFoundError:
            self.settings = {"screen_height": 480, "screen_width": 480, "grid_size": 20, "start_size": 3, "walls": []}

        # make sure that the values are set no matter what (i.e. json given as parameter, but does not have attributes)
        if "screen_height" not in self.settings:
            self.settings["screen_height"] = 480
        if "screen_width" not in self.settings:
            self.settings["screen_width"] = 480
        if "grid_size" not in self.settings:
            self.settings["grid_size"] = 20
        if "start_size" not in self.settings:
            self.settings["start_size"] = 480
        if "walls" not in self.settings:
            self.settings["walls"] = []
        if "start_size" not in self.settings:
            self.settings["start_size"] = 2

        self.settings["grid_size"] = min(80, self.settings["grid_size"])
        self.settings["screen_height"] = min(768, self.settings["screen_height"])
        self.settings["screen_width"] = min(768, self.settings["screen_width"])

        self.base_grid = self.init_grid()    # Have a basic grid so we won't reinitialize it every time the player dies
        self.grid = deepcopy(self.base_grid)
        self.snake = Snake(self.grid, self.settings['start_size'])
        self.food = Food()

        # code needed to make pygame work
        pygame.init()
        pygame.display.set_caption('Snake!')
        snake_image = pygame.image.load('snake-icon.png')
        pygame.display.set_icon(snake_image)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]),
                                              flags=pygame.SCALED, depth=32, vsync=True)
        self.block_width = self.settings["screen_width"] / self.settings["grid_size"]
        self.block_height = self.settings["screen_height"] / self.settings["grid_size"]
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.font = pygame.font.SysFont("monospace", 20)

    def init_grid(self):
        """
        Initializes a two dimensional array used as a board for the game.
        :return:
            2D List of size grid_size x grid_size of value EMPTY if the grid is not covered by a wall and value WALL otherwise.
        """
        grid = []
        for i in range(self.settings['grid_size']):
            grid.append([])
            for j in range(self.settings['grid_size']):
                if [j, i] in self.settings['walls']:
                    grid[i].append(g.WALL)
                else:
                    grid[i].append(g.EMPTY)
        return grid

    def draw_grid(self, darken=1):
        """
        Draws the grid onto the screen, based on the values of grid attribute.
        :param darken: float, optional, with value between 0 and 1
            Darkens the shade of the color by the specified amount (i.e. a value of 0.5 will make the grid 50% darker)
        """
        if not(0 < darken < 1):
            darken = 1
        for x in range(0, int(self.settings['grid_size'])):
            for y in range(0, int(self.settings['grid_size'])):
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

    def run_game(self):
        """Starts a game session."""
        self.food.randomize_position(self.grid)
        while True:
            self.clock.tick(8)
            self.handle_keys()
            if not self.snake.move(self.grid):
                if self.end_game_dialog() == 0:
                    end_game()
                else:
                    self.score = 0
                    self.grid = deepcopy(self.base_grid)
                    self.snake.initialize_snake_on_grid(self.grid)
                    self.food.randomize_position(self.grid)

            self.draw_grid()

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

    def handle_keys(self):
        """
        Handles user input, changing the snake direction based on the key pressed.
        Valid keystrokes: Up, Down, Left and Right arrows.
        """
        handled = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            elif event.type == pygame.KEYDOWN:
                if handled and event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                    pygame.event.post(event)
                    break
                if event.key == pygame.K_UP:
                    self.snake.turn(self.snake.up)
                    handled = True
                elif event.key == pygame.K_DOWN:
                    self.snake.turn(self.snake.down)
                    handled = True
                elif event.key == pygame.K_LEFT:
                    self.snake.turn(self.snake.left)
                    handled = True
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn(self.snake.right)
                    handled = True

    def end_game_dialog(self):
        """
        Initializes the menu that will appear after the player loses a round, giving an option of either keep playing
            or quitting the game.
        :return: 0, in case the player wants to quit
                 1, in case the player wants to keep playing
        """
        retry_button = pygame.Rect((self.settings["screen_width"] / 2 - 75, 170), (150, 25))
        play_again = self.font.render('Play Again!', True, (255, 250, 106))

        quit_button = pygame.Rect((self.settings["screen_width"] / 2 - 75, 250), (150, 25))
        quit_text = self.font.render('Quit!', True, (255, 250, 106))
        while True:
            self.clock.tick(10)
            self.draw_grid(0.4)  # darken shade for every block
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


if __name__ == "__main__":
    if len(argv) == 2:
        game = Game(argv[1])
    else:
        game = Game()
    game.run_game()
