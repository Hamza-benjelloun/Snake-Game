import pygame, random
from matplotlib import pyplot as plt

pygame.init()

WIN_DIMENSION = 480

BKGCOLOUR = (141, 168, 32)
FONT = pygame.font.SysFont(None, 25)

GRIDSIZE = 20
WALL_DIMENSION = WIN_DIMENSION + GRIDSIZE
GRID_DIMENSION = WIN_DIMENSION / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake():
    def __init__(self):
        self.score = 0
        self.length = 3
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.colour = (0, 0, 0)

    def get_head_position(self):
        return self.coordinates[0]

    def turn(self, point):
        if (point[0] * - 1, point[1] * - 1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        new = (((current[0] + (x * GRIDSIZE)) % WALL_DIMENSION), (current[1] + (y * GRIDSIZE)) % WALL_DIMENSION)
        if new in self.coordinates[0:]:
            self.reset()
        else:
            self.coordinates.insert(0, new)
            if len(self.coordinates) > self.length:
                self.coordinates.pop()

    def reset(self):
        scores = []
        scores.append(self.score)
        print(scores)
        self.length = 3
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        

    def draw(self, surface):
        for p in self.coordinates:
            snake = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.colour, snake)


class Apple():
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.colour = (0, 0, 0)

    def randomize_position(self):
        self.position = (random.randint(0, GRID_DIMENSION-1) * GRIDSIZE, random.randint(0, GRID_DIMENSION-1)*GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect(
            (self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.colour, r)


SNAKE = Snake()
APPLE = Apple()


def collide():
    x = SNAKE.get_head_position()[0]
    y = SNAKE.get_head_position()[1]
    if x > WIN_DIMENSION - GRIDSIZE or x < 0 or y > WIN_DIMENSION - GRIDSIZE or y < 0:
        SNAKE.reset()

def eat():
    if SNAKE.get_head_position() == APPLE.position:
        SNAKE.length += 1
        SNAKE.score += 1
        APPLE.randomize_position()


def draw_grid(surface):
    pygame.draw.rect(surface, BKGCOLOUR, pygame.Rect(0, 0, WIN_DIMENSION, WIN_DIMENSION))
    x = 0
    y = 0
    for l in range(WIN_DIMENSION):
        x = x + GRIDSIZE
        y = y + GRIDSIZE
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, WIN_DIMENSION))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (WIN_DIMENSION, y))


def redraw_window():
    surface = pygame.Surface((WIN.get_size()))
    surface = surface.convert()
    draw_grid(surface)
    SNAKE.draw(surface)
    APPLE.draw(surface)
    scoreboard = FONT.render("Score {0}".format(SNAKE.score), 1, (0, 0, 0))
    surface.blit(scoreboard, (1, 1))
    WIN.blit(surface, (0, 0))
    pygame.display.flip()
    pygame.display.update()


def main():
    pygame.init()
    global WIN
    WIN = pygame.display.set_mode((WIN_DIMENSION, WIN_DIMENSION))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()
    fps = 10

    run = True
    while run == True:
        clock.tick(fps)
        redraw_window()
        SNAKE.move()
        collide()
        eat()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    SNAKE.turn(UP)
                elif event.key == pygame.K_DOWN:
                    SNAKE.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    SNAKE.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    SNAKE.turn(RIGHT)

    pygame.quit()


if __name__ == "__main__":
    main()
