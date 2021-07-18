import pygame
import random
from enum import Enum
from collections import namedtuple

BLOCK_SIZE = 20
SPEED = 10

#rgb colors
COLOR_WHITE = (255,255,255)
COLOR_RED = (200,0,0)
COLOR_BLUE_LIGHT = (0,0,255)
COLOR_BLUE_DARK = (0,100,255)
COLOR_BLACK = (0,0,0)

Point = namedtuple('Point', 'x, y')

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
class SnakeGame:

    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h

        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        #init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def play_step(self):
        #collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT    
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                elif event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                
        #move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)

        #check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()

        else:
            self.snake.pop()

        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        #return game over and score
        return game_over, self.score

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _is_collision(self):
        #hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        #hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(COLOR_BLACK)
        
        #draw snake
        for point in self.snake:
            pygame.draw.rect(self.display, COLOR_BLUE_LIGHT, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, COLOR_BLUE_DARK, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE*0.6, BLOCK_SIZE*0.6))

        #draw food
        pygame.draw.rect(self.display, COLOR_RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        #draw score
        text = font.render("Score: " + str(self.score), True, COLOR_WHITE)
        self.display.blit(text, [0,0])

        pygame.display.flip()


if __name__ == '__main__':
        game = SnakeGame()

        #game loop
        while True:
            game_over, score = game.play_step()

            #break if game over
            if game_over == True:
                break

        print('Final score', score)

        pygame.quit()