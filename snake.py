import pygame
import random
import sys

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 15
GRID_COLOR_1 = (156, 238, 255)
GRID_COLOR_2 = (0, 210, 255)
TEXT_COLOR = (0,0,0)
FOOD_COLOR = (255, 3, 47)
RESET_SLEEP_TIME = 2000
FPS = 13

pygame.font.init()
FONT = pygame.font.Font('C:/Users/aatut/Documents/Code/PythonProjektit/Snakegamedirectory/snakefont.ttf', 40)

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

class Snake():
    
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 0, 0)
        self.score = 1
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, direction):
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction
    
    def move(self, food):
        current = self.get_head_position()
        x, y = self.direction
        new = (current[0] + x * BLOCK_SIZE, current[1] + y * BLOCK_SIZE) 
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset(food)
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        if self.positions[0] == food.position:
            self.score += 1
            self.length += 1
            food.position = food.randomize_position()
        if not 0 - BLOCK_SIZE < self.positions[0][0] < SCREEN_WIDTH:
            self.reset(food)
        elif not 0 - BLOCK_SIZE < self.positions[0][1] < SCREEN_HEIGHT:
            self.reset(food)

    def reset(self, food):
        pygame.time.wait(RESET_SLEEP_TIME)
        food.position = food.randomize_position()
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 1

    def draw(self, screen):
        for position in self.positions:
            x, y = position
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, self.color, rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.turn(UP)
                if event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                if event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                if event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
 

class Food():

    def __init__(self):
        self.color = FOOD_COLOR
        self.position = (random.randrange(0, SCREEN_WIDTH-BLOCK_SIZE, BLOCK_SIZE), 
        random.randrange(0, SCREEN_HEIGHT-BLOCK_SIZE, BLOCK_SIZE))
    
    def randomize_position(self):
        return (random.randrange(0, SCREEN_WIDTH-BLOCK_SIZE, BLOCK_SIZE), 
        random.randrange(0, SCREEN_HEIGHT-BLOCK_SIZE, BLOCK_SIZE))

    def draw(self, screen):
        x, y = self.position
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        
def draw_grid(screen):
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        if y == 0 or y % (BLOCK_SIZE*2) == 0:
            for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                if x == 0 or x % (BLOCK_SIZE*2) == 0:
                    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, GRID_COLOR_1, rect)
                else:
                    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, GRID_COLOR_2, rect)
        else:
            for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                if x == 0 or x % (BLOCK_SIZE*2) == 0:
                    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, GRID_COLOR_2, rect)
                else:
                    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, GRID_COLOR_1, rect)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')

    snake = Snake()
    food = Food()

    while True:
        clock.tick(FPS)
        draw_grid(screen)

        snake.handle_keys()
        
        snake.move(food)
        snake.draw(screen)

        food.draw(screen)

        score_text = str(snake.score)
        score_surface = FONT.render(f'Score: {score_text}', True, TEXT_COLOR)
        screen.blit(score_surface, (BLOCK_SIZE*2 , BLOCK_SIZE*2))

        pygame.display.update()

if __name__ == '__main__':
    main()
