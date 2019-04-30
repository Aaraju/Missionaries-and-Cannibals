"""
Author  :   Deepesh Shrestha
Date    :   28 October 2018
Course  :   Artificial Intelligence
"""

from collections import deque   # library for queue functionality
import pydotplus            # import pydotplus to generate graph in dot language
import pygame           # PYGAME
import random           # import random to randomly select missionaries from the riverbanks
from PIL import Image   # import PIL to display graph

# defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (211, 211, 211)
BROWN = (111, 62, 20)

screen_width = 1000     # width of the screen
screen_height = 400     # height of the screen

pygame.init()           # initialize pygame
pygame.display.set_caption("Missionaries and Cannibals")        # title of the windows
screen = pygame.display.set_mode((screen_width, screen_height)) # set the dimension of the screen
clock = pygame.time.Clock()         # clock to toggle the FPS(frames per second)


class Environment(object):

    def __init__(self):
        # import image for missionary, cannibal and boat
        self.missionary_img = [pygame.image.load("res/man.png"), pygame.image.load("res/man.png"),
                               pygame.image.load("res/man.png")]
        self.cannibal_img = [pygame.image.load("res/devil.png"), pygame.image.load("res/devil.png"),
                             pygame.image.load("res/devil.png")]
        self.boat_img = pygame.image.load("res/boat.png")
        self.missionary_status = [1, 1, 1]  # status of missionary, 1 for on the left shore and 0 for on the right shore
        self.cannibal_status = [1, 1, 1]    # status of cannibals, same as above
        self.boat_startPositionX = 300      # where the boat will start (X coordinate)
        self.boat_startPositionY = 150      # where the boat will start (Y coordinate)

    def initialize(self):
        screen.blit(self.boat_img, (self.boat_startPositionX, self.boat_startPositionY))    # place the boat on the screen at position X and Y
        for i in range(3):  # place three missionaries and cannibals on the screen
            if self.missionary_status[i] == 1:
                screen.blit(self.missionary_img[i], (50 * i, 250))
            if self.missionary_status[i] == 0:
                screen.blit(self.missionary_img[i], (50 * i + 700, 250))
            if self.cannibal_status[i] == 1:
                screen.blit(self.cannibal_img[i], (50 * i, 150))
            if self.cannibal_status[i] == 0:
                screen.blit(self.cannibal_img[i], (50 * i + 700, 150))


class State:    # class for state of the missionary, cannibal

    def __init__(self, missionaries, cannibals, boats, m, c, action): #
        self.missionaries = missionaries    # condition of missionary on the left shore
        self.cannibals = cannibals          # condition of missionary on the right shore
        self.boats = boats                  # condition of missionary on the boat
        self.m = m                          # no of missionaries to be transported to achieve this state
        self.c = c                          # no of cannibals to be transported to achieve this state
        self.action=action                  # conjunction of the above two m and c
        self.goal_state = (0, 0, 0)         # the goal state

    def __str__(self):   # function to define the printing format fo the solution
        return "[%s %s %s] %s" % (self.missionaries, self.cannibals, self.boats,self.action)

    def get_successors(self):
        if self.boats == 1:
            print("\nThe boat is currently on the left side")
            sign = -1
        else:
            print("\nThe boat is currently on the right side")
            sign = 1
        for m in range(3):
            for c in range(3):
                missionary = self.missionaries + sign * m
                cannibal = self.cannibals + sign * c
                boat = self.boats + sign
                action = "\n%s %s" % (m, c)
                new_state = State(missionary, cannibal, boat, m, c, action)
                if 1 <= m + c <= 2 and new_state.is_valid():
                    print("The valid state is %s" % new_state)
                    yield new_state

    def is_valid(self):
        if self.missionaries < 0 or self.missionaries > 3 or self.cannibals < 0 or self.cannibals > 3 or self.boats < 0 or self.boats > 1:
            return False
        if 0 < self.missionaries < self.cannibals:
            return False
        if 3 > self.missionaries > self.cannibals:
            return False
        return True

    def is_goal(self):
        return (self.missionaries, self.cannibals, self.boats) == self.goal_state


class Node(object):

    def __init__(self, parent, state, depth):
        self.parent = parent
        self.state = state
        self.depth = depth
        self.dot = pydotplus.Node(str(self), shape='plaintext')

    def successor_node(self):
        for (successor) in self.state.get_successors():
            yield Node(parent=self, state=successor, depth=self.depth + 1)

    def get_solution(self):
        solution = []
        m = []
        c = []
        b = []
        node = self
        while node.parent is not None:
            solution.append(node.state)
            m.append(node.state.m)
            c.append(node.state.c)
            b.append(node.state.boats)
            node = node.parent
        solution.reverse()
        m.reverse()
        c.reverse()
        b.reverse()
        return solution, m, c, b

    def __str__(self):
        return self.state.__str__()


def breadth_first_search(root):
    print("Starting Node(root) : %s" % root)
    graph = pydotplus.Dot(graph_type='digraph')

    queue = deque([root])
    visited = []
    expansion = 0

    while True:
        node = queue.popleft()
        print("\n Parent Node : %s ,Currently popped node %s at depth %s" % (node.parent, node.state, node.depth))
        if str(node) in visited:
            continue
        visited.append(str(node))
        graph.add_node(node.dot)
        if node.parent:
            graph.add_edge(pydotplus.Edge(node.parent.dot, node.dot))
        if node.state.is_goal():
            graph.write_png('solution.png')
            print("\nReached Goal State at %s" % node.state)
            # print("Total no. of expansion is %d" % expansion)
            solution = node.get_solution()
            return solution

        expansion += 1

        queue.extend(node.successor_node())


def draw_terrain():
    pygame.draw.polygon(screen, GREEN, ((0, 100), (375, 100), (300, 370), (0, 370)))  # left riverbank
    pygame.draw.polygon(screen, GREEN, ((625, 100), (990, 100), (990, 370), (700, 370)))  # right riverbank
    pygame.draw.polygon(screen, BLUE, ((375, 100), (625, 100), (700, 370), (300, 370)))  # river
    pygame.draw.rect(screen, BROWN, (0, 0, 1000, 100))  # rocks
    pygame.draw.rect(screen, BLUE, (375, 0, 250, 100))  #waterfall
    pygame.draw.rect(screen, GRAY, (0, 370, 1000, 30))  # status_bar
    pygame.draw.rect(screen, GRAY, (0, 0, 10, 500))  # sidebar_left
    pygame.draw.rect(screen, GRAY, (990, 0, 10, 500))  # sidebar_right


def move_boat(self, b):
    if b == 0:  # when boat is on the left shore go to the right shore
        self.boat_startPositionX += 300
    if b == 1:  # when boat is on the right shore go to the left shore
        self.boat_startPositionX -= 300


def show_solution(self, m, c, b):
    move_boat(self, b)
    for i in range(m):
        if self.missionary_status[i] != b:
            self.missionary_status[i] = b
        else:
            c = 1
            while c:
                x = random.randint(0, 2)
                if self.missionary_status[x] != b:
                    self.missionary_status[x] = b
                    c = 0
    for i in range(c):
        if self.cannibal_status[i] != b:
            self.cannibal_status[i] = b
        else:
            c = 1
            while c:
                x = random.randint(0, 2)
                if self.cannibal_status[x] != b:
                    self.cannibal_status[x] = b
                    c = 0
    print(self.missionary_status)
    print(self.cannibal_status)
    self.initialize()


def main():
    initial_state = State(3, 3, 1, 0, 0,"")
    root = Node(None, initial_state, 0)
    print("Calculating the solution \n")
    solution, m, c, b = breadth_first_search(root)
    print(root)
    print("\n The solutions is \n")
    for i in range(len(solution)):
        print(solution[i])
    count = 0
    l = len(solution)
    self = Environment()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if count >= l:
                        pass
                    else:
                        print("Move No.%s Boat %s" % ((count + 1), b[count]))
                        show_solution(self, m[count], c[count], b[count])
                        count += 1
                if event.key == pygame.K_TAB:           # showing the graph when TAB is pressed
                    img = Image.open('solution.png')
                    img.show()
        draw_terrain()
        self.initialize()           # initalize the characters and the boat on the screen
        pygame.display.update()     # updating the screen

        clock.tick(5)               # defining the FPS

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()