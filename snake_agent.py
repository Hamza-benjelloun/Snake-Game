# Importing libraries
from time import time
import pygame, random
import operator
from queue import Queue

# Initialization of our game
pygame.init()

# Declaration of some global Variables
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
GRAPH = {}
NB=0 # A variable to track the path that we are following
PATH_EXIST = False # To check if we found a path or not


# Snake Class
class Snake():

    # Initialization
    def __init__(self):
        self.score = 0
        self.length = 3
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]        
        self.colour = (0, 0, 0)        

    # Methode to move the snake (Change it's direction)
    def turn(self, point):
        if (point[0] * - 1, point[1] * - 1) == self.direction:
            return
        else:
            self.direction = point

    # Get head position Methode            
    def get_head_position(self):
        return self.coordinates[0]  

    # Move the snake via a direction                    
    def move(self):  

        current = self.get_head_position()
        
        x, y = self.direction
        new = (((current[0] + (x * GRIDSIZE)) % WALL_DIMENSION), (current[1] + (y * GRIDSIZE)) % WALL_DIMENSION)
        if new in self.coordinates[0:]:
            print("[+] Type of collision : body")
            self.reset()
        else:
            self.coordinates.insert(0, new)
            if len(self.coordinates) > self.length:
                self.coordinates.pop()

    # Reset the Snake game when the game is lost
    def reset(self):
        global PATH_EXIST
        global NB
        global GRAPH
        scores = []
        scores.append(self.score)
        print(scores)
        self.length = 3
        self.coordinates = [((WIN_DIMENSION / 2), (WIN_DIMENSION / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        GRAPH = create_graph(SNAKE.coordinates)
        PATH_EXIST = False 
        NB=0 
        
    # Draw the snake
    def draw(self, surface):
        for p in self.coordinates:
            snake = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.colour, snake)

# Apple Class
class Apple():

    # Initialization
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.colour = (0, 0, 0)

    # Choose a random position of the apple different from the snake coordinates
    def randomize_position(self,coordinates=[]):
        
        Xs = [item[0] for item in coordinates]
        Ys = [item[1] for item in coordinates]       
        try:   
            x_choice = random.choice([i for i in range(20,440,20) if i not in Xs])
            y_choice = random.choice([i for i in range(20,440,20) if i not in Ys])         
        except:
            x_choice = random.choice([i for i in range(20,440,20)])
            y_choice = random.choice([i for i in range(20,440,20)]) 
        
        self.position = (x_choice, y_choice)

    # Draw the apple
    def draw(self, surface):        
            
        r = pygame.Rect(
            (self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.colour, r)

# Create Snake and Apple objects
SNAKE = Snake()
APPLE = Apple()

# Initialize the path that we can fill using the Breadth-First Search 
path = []

# Here we define the global function

# Simple function to add tuple to another one (the traditional + result a concatenation)
def addition_tuple(a,b):
    return tuple(map(operator.add, a, b))

# Create a graphe of nodes with taking in consideration the snake position (coordinates as argument)
def create_graph(coordinates = []):
    UP = (0, -20)
    DOWN = (0, 20)
    LEFT = (-20, 0)
    RIGHT = (20, 0)
    graph = {}
    for x in range(0,461,20):
        for y in range(0,461,20):
            point = (x,y)
            if(x==0):
                go_right = addition_tuple(point,RIGHT)
                if(y==0):                
                    go_down = addition_tuple(point,DOWN)
                    if(go_right in coordinates):
                        if(go_down in coordinates):
                            graph[point]=[]
                        else:
                            graph[point]=[go_down]
                    elif(go_down in coordinates):
                        graph[point]=[go_down]
                    else:
                        graph[point]=[go_right,go_down]


                elif(y==460):                
                    go_up = addition_tuple(point,UP)
                    if(go_right in coordinates):
                        if(go_up in coordinates):
                            graph[point]=[]
                        else:
                            graph[point]=[go_up]
                    elif(go_up in coordinates):
                        graph[point]=[go_up]
                    else:
                        graph[point]=[go_right,go_up]
                else:
                    if(go_right in coordinates):
                        graph[point]=[]
                    else:
                        graph[point]=[go_right]
            elif(x==460):
                go_left = addition_tuple(point,LEFT)                
                if(y==0):
                    go_down = addition_tuple(point,DOWN)
                    if(go_left in coordinates):
                        if(go_down in coordinates):
                            graph[point]=[]
                        else:
                            graph[point]=[go_down]
                    elif(go_down in coordinates):
                        graph[point]=[go_down]
                    else:
                        graph[point]=[go_left,go_down]
                    graph[point]=[go_left,go_down]
                elif(y==460):
                    go_up = addition_tuple(point,UP)
                    if(go_left in coordinates):
                        if(go_up in coordinates):
                            graph[point]=[]
                        else:
                            graph[point]=[go_up]
                    elif(go_up in coordinates):
                        graph[point]=[go_up]
                    else:
                        graph[point]=[go_left,go_up]
                    graph[point]=[go_left,go_up]
                else:
                    if(go_left in coordinates):
                        graph[point]=[]
                    else:
                        graph[point]=[go_left]                    
            elif(y==0):
                go_down = addition_tuple(point,DOWN)
                if(go_down in coordinates):
                    graph[point]=[]
                else:                
                    graph[point]=[go_down]
            elif(y==460):
                go_up = addition_tuple(point,UP)
                if(go_up in coordinates):
                    graph[point]=[]
                else:                
                    graph[point]=[go_up]                
            else:
                go_up = addition_tuple(point,UP)
                go_down = addition_tuple(point,DOWN)
                go_left = addition_tuple(point,LEFT)
                go_right = addition_tuple(point,RIGHT)
                
                to_check=[go_down,go_up,go_left,go_right]
                to_add=[]

                for item in to_check:
                    if item not in coordinates:
                        to_add.append(item)
                
                graph[point]= to_add
    
    return graph

# Creating our initial graph
GRAPH = create_graph()

# The Breadth-First Search function (return optimal path to a target node)
def BFS(adj_list, start_node, target_node):
    # Set of visited nodes to prevent loops
    visited = set()
    queue = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for next_node in adj_list[current_node]:
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)
                
    # Path reconstruction
    path = []
    new_path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()

    # Converting the path to directions (UP , DOWN, LEFT , RIGHT)        
    for k in range(len(path)-1):
        new_path.append(tuple(map(lambda i, j: int((i - j)/20),path[k+1],path[k])))
    return new_path

# Check collision of snake to end the game    
def collide():
    try:
        x = SNAKE.get_head_position()[0]
        y = SNAKE.get_head_position()[1]
    except:
        print(SNAKE.get_head_position())
    
    if x > WIN_DIMENSION - GRIDSIZE or x < 0 or y > WIN_DIMENSION - GRIDSIZE or y < 0:
        print("[+] Reason collision")
        SNAKE.reset()

# Check if the snake eated the apple to increment the length
def eat():
    global PATH_EXIST
    global NB
    global GRAPH
    if SNAKE.get_head_position() == APPLE.position:
        SNAKE.length += 1
        SNAKE.score += 1
        APPLE.randomize_position(SNAKE.coordinates)
        GRAPH = create_graph(SNAKE.coordinates)
        PATH_EXIST = False 
        NB=0           

# Draw grid between rectangles
def draw_grid(surface):
    pygame.draw.rect(surface, BKGCOLOUR, pygame.Rect(0, 0, WIN_DIMENSION, WIN_DIMENSION))
    x = 0
    y = 0
    for l in range(WIN_DIMENSION):
        x = x + GRIDSIZE
        y = y + GRIDSIZE
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, WIN_DIMENSION))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (WIN_DIMENSION, y))

# Redraw window
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

# Main function to execute the code                  
def main():

    # Initialization of the game
    pygame.init()
    
    # Declaration and call of global variables
    global WIN
    global NB
    global PATH_EXIST

    # Setting the screen dimensions
    WIN = pygame.display.set_mode((WIN_DIMENSION, WIN_DIMENSION))
    # Setting the caption
    pygame.display.set_caption("Snake")
    # Clock to tick the fps (limit it)
    clock = pygame.time.Clock()
    fps = 10


    run = True
    first_retard = True
    while run == True:  
                                      
        clock.tick(fps)

        redraw_window()  

        #Check if the path exist                    
        if(PATH_EXIST==False):
            # mesuring the time of path calculation
            start = time()

            # Getting the apple position to use it as a target
            apple = APPLE.position            
            path = BFS(GRAPH,SNAKE.get_head_position(),apple)

            end = time()            
            
            # print("[v] Path found")
            # print(f"[+] Runtime of the program is {end - start}") # displaying the time of execution
            # print("[+] ",len(path),"moves")
            # print("[!] Tracking :")            
        
        # check if the path exist then check which direction to go
        if path!=[]:            
            PATH_EXIST = True            
            
        if(PATH_EXIST==True):      
            try:
                direction = path[NB]
            except:
                PATH_EXIST=False
                NB=0
                continue

            # Display the direction                        
            if(direction==UP):
                print("[!] UP")
            elif(direction==DOWN):
                print("[!] DOWN")
            elif(direction==LEFT):
                print("[!] LEFT")
            elif(direction==RIGHT):
                print("[!] RIGHT")
            else:
                print("UNKOWN :",direction) 
            # move to that direction                  
            SNAKE.turn(direction)
            NB+=1
            SNAKE.move()
        else:
            if(first_retard==True):
                for movement in [UP,LEFT,RIGHT,DOWN]:
                    x,y = addition_tuple(movement,SNAKE.get_head_position())
                    if (x,y) not in SNAKE.coordinates and x <= (WIN_DIMENSION - GRIDSIZE) and x >= 0 and y <= (WIN_DIMENSION - GRIDSIZE) and y >= 0 :
                        SNAKE.turn(movement)
                        SNAKE.move()
                        # first_retard=False
                        break
            else:
                print("[+] Waiting for the path calculation")
                
        # Check collision
        collide()
        # Check if the snake ate the apple
        eat()
        
        # Check if the user clicked on the quit icon then exit the game with quit                  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

    pygame.quit()


if __name__ == "__main__":
    main()
