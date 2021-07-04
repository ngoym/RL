import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("arial.ttf", 25)

Point = namedtuple('Point',['x','y'])

class DIR(Enum):
    """ Directions """
    RIGHT = 1
    LEFT  = 2
    UP    = 3
    DOWN  = 4
class constants():
    BLOCK_SZ = 20
    SMALL_SZ = 12
    SPEED    = 10
    WHITE    = (255, 255, 255)
    RED      = (200, 0, 0)
    BLUE     = (0, 0, 255)
    BRI_BLUE = (0, 100, 255)
    BLACK    = (0,0,0)

constants = constants()
class snake():
    """ Main game class """
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h 

        # init pygame display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # game state
        self.direction = DIR.RIGHT
        self.cur_dir   = self.direction
        # init snake
        self.head  = Point(self.w//2, self.h//2)
        self.snake = [
            self.head,
            Point(self.head.x - constants.BLOCK_SZ, self.head.y),
            Point(self.head.x - 2*constants.BLOCK_SZ, self.head.y)
            ] 
        self.score = 0
        self.food = None
        self._add_food()
    
    def _add_food(self):
        # We want x and y to be multiples of BLOCK_SZ
        x = random.randint(0, (self.w - constants.BLOCK_SZ) // constants.BLOCK_SZ) * constants.BLOCK_SZ 
        y = random.randint(0, (self.h - constants.BLOCK_SZ) // constants.BLOCK_SZ) * constants.BLOCK_SZ
        self.food = Point(x,y)
        if self.food in self.snake:
            self._add_food()

    def _update_ui(self):
        """ Update UI """
        self.display.fill(constants.BLACK)
        # draw snake
        for point in self.snake:
            pygame.draw.rect(self.display, constants.BRI_BLUE, pygame.Rect(point.x, point.y, constants.BLOCK_SZ, constants.BLOCK_SZ))
            pygame.draw.rect(self.display, constants.BRI_BLUE, pygame.Rect(point.x+4, point.y+4, constants.SMALL_SZ, constants.SMALL_SZ))
        
        pygame.draw.rect(self.display, constants.RED, pygame.Rect(self.food.x, self.food.y, constants.BLOCK_SZ, constants.BLOCK_SZ))
        score_text = font.render("Score: {}".format(self.score), True,  constants.WHITE)
        self.display.blit(score_text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        """ Move snake """
        x = self.head.x 
        y = self.head.y 

        if direction == DIR.RIGHT:
            x += constants.BLOCK_SZ
        elif direction == DIR.LEFT:
            x -= constants.BLOCK_SZ
        elif direction == DIR.DOWN:
            y += constants.BLOCK_SZ
        elif direction == DIR.UP:
            y -= constants.BLOCK_SZ

        self.head = Point(x,y)

    def _game_over(self):
        """ Check if the snake hits a boundary or folds onto itself """
        game_over = False
        if self.head in self.snake[1:]: # head is position 0 in the list
            game_over = True
        if self.head.x > self.w - constants.BLOCK_SZ or self.head.x < 0 or \
            self.head.y < 0 or self.head.y > self.h - constants.BLOCK_SZ:
            game_over = True 
        return game_over

    def play(self):
        """ Actual game play """
        # Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != DIR.RIGHT:
                        self.direction = DIR.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != DIR.LEFT:
                        self.direction = DIR.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction != DIR.DOWN:
                        self.direction = DIR.UP
                if event.key == pygame.K_DOWN:
                    if self.direction != DIR.UP:
                        self.direction = DIR.DOWN

        # Move the snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        # check if game over
        if self._game_over():
            game_over = True 
            return game_over, self.score
        # place food or move
        if self.head == self.food:
            self.score += 1
            self._add_food()
        else:
            self.snake.pop()
        # update UI
        self._update_ui()
        self.clock.tick(constants.SPEED)

        game_over = False
        return game_over, self.score

if __name__ == "__main__":
    game = snake()

    while True:
        # Break if game over
        game_over, score = game.play()
        if game_over:
            break
    # Print final score at exit
    print("Final score: ", score)
    pygame.quit()