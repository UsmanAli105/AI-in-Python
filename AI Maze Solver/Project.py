import pygame
from pygame.locals import *
import math
import random
import time
import copy

speed = 0
sleep_time = 0


class dimensions:
    def __init__(self, North, East, West, South):
        self.North = North
        self.South = South
        self.West = West
        self.East = East
        self.dim_array = [East, West, North, South]

    def setDimensions(self, dim_array):
        self.North = dim_array[0]
        self.South = dim_array[1]
        self.West = dim_array[2]
        self.East = dim_array[3]
        self.dim_array = dim_array

    def update_dimensions(self):
        self.dim_array = [self.East, self.West, self.North, self.South]


class coordinates:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.coord_array = [x1, y1, x2, y2]

    def get_x1(self):
        return self.x1

    def get_x2(self):
        return self.x1

    def get_y1(self):
        return self.x1

    def get_y2(self):
        return self.x1


class cell:
    def __init__(self, name, _cell_dimensions, _cell_coordinates):
        self.name = name
        self.cell_dimensions = _cell_dimensions
        self.cell_coordinates = _cell_coordinates


class Box:
    def __init__(self, _coordinates, _speed, screen):
        self._coordinates = _coordinates
        self._speed = _speed
        self.direction = 'None'
        self.screen = screen
        self.block = pygame.image.load("block.png").convert()

    def drawBox(self):
        self.screen.blit(self.block, (self._coordinates.x1, self._coordinates.y1))

    def move_up(self):
        self._coordinates.y1 -= self._speed

    def move_down(self):
        self._coordinates.y1 += self._speed

    def move_right(self):
        self._coordinates.x1 += self._speed

    def move_left(self):
        self._coordinates.x1 -= self._speed

    def Walk(self):
        if self.direction == 'U':
            self.move_up()
        elif self.direction == 'D':
            self.move_down()
        elif self.direction == 'R':
            self.move_right()
        elif self.direction == 'L':
            self.move_left()


class goal:
    def __init__(self, _coordinates, screen):
        self._coordinates = _coordinates
        self.screen = screen


class AI_agent:
    def __init__(self, _box, _goal):
        self._box = _box
        self._goal = _goal
        self.distance_x = 0
        self.distance_y = 0

    def sensor(self, _box, _goal):
        self._box = _box
        self._goal = _goal

    def calc_distance(self):
        self.distance_x = self._goal._coordinates.x1 - self._box._coordinates.x1
        self.distance_y = self._goal._coordinates.y1 - self._box._coordinates.y1

    def desirability_x(self):
        if self.distance_x != 0:
            return True
        return False

    def desirability_y(self):
        if self.distance_y != 0:
            return True
        return False

    def actuator(self):
        self.calc_distance()
        if self.desirability_x():
            if self.distance_x < 0:
                self._box.direction = 'L'
            if self.distance_x > 0:
                self._box.direction = 'R'
            return False
        elif self.desirability_y():
            if self.distance_y < 0:
                self._box.direction = 'U'
            if self.distance_y > 0:
                self._box.direction = 'D'
            return False
        return True


def set_FPS(val):
    global speed, sleep_time
    if val == 30:
        speed = 1
        sleep_time = 0.001
    if val == 60:
        speed = 0.5
        sleep_time = 0.0005
    if val == 120:
        speed = 0.25
        sleep_time = 0.001


def createDimensions(SIZE):
    cell_dimensions = []
    count = SIZE * SIZE
    for x in range(count):
        dim = [True] * 4
        dim_obj = dimensions(dim[0], dim[1], dim[2], dim[3])
        cell_dimensions.append(dim_obj)
    return cell_dimensions


def createCoordinates(SIZE, cellSize, _padding):
    cell_coordinates = []
    for y in range(SIZE):
        for x in range(SIZE):
            x1 = x * cellSize + _padding
            y1 = y * cellSize + _padding
            x2 = x * cellSize + cellSize + _padding
            y2 = y * cellSize + cellSize + _padding
            single_cell_coordinates = coordinates(x1, y1, x2, y2)
            cell_coordinates.append(single_cell_coordinates)
    return cell_coordinates


def createCellName(SIZE):
    start = 0
    cell_name = []
    count = SIZE * SIZE
    for x in range(count):
        cell_name.append(start)
        start += 1
    return cell_name


def createMaze(SIZE, cellSize, _padding):
    cell_name = createCellName(SIZE)
    cell_coordinates = createCoordinates(SIZE, cellSize, _padding)
    cell_dimensions = createDimensions(SIZE)
    totalCells = SIZE * SIZE
    Maze = []
    for y in range(totalCells):
        _cell = cell(cell_name[y], cell_dimensions[y], cell_coordinates[y])
        Maze.append(_cell)
    return Maze


def drawEast(cell_dimensions):
    x1 = cell_dimensions.x1
    y1 = cell_dimensions.y1
    x2 = cell_dimensions.x1
    y2 = cell_dimensions.y2
    return (x1, y1), (x2, y2)


def drawWest(cell_dimensions):
    x1 = cell_dimensions.x2
    y1 = cell_dimensions.y1
    x2 = cell_dimensions.x2
    y2 = cell_dimensions.y2
    return (x1, y1), (x2, y2)


def drawNorth(cell_dimensions):
    x1 = cell_dimensions.x1
    y1 = cell_dimensions.y1
    x2 = cell_dimensions.x2
    y2 = cell_dimensions.y1
    return (x1, y1), (x2, y2)


def drawSouth(cell_dimensions):
    x1 = cell_dimensions.x1
    y1 = cell_dimensions.y2
    x2 = cell_dimensions.x2
    y2 = cell_dimensions.y2
    return (x1, y1), (x2, y2)


def DrawMaze(_MAZE, _screen):
    width = 2
    color = (255, 255, 255)
    for i in range(len(_MAZE)):
        for j in range(len(_MAZE[i].cell_dimensions.dim_array)):
            if j == 0:
                if _MAZE[i].cell_dimensions.dim_array[j]:
                    start_pos, end_pos = drawEast(_MAZE[i].cell_coordinates)
                    pygame.draw.line(_screen, color, start_pos, end_pos, width)
            if j == 1:
                if _MAZE[i].cell_dimensions.dim_array[j]:
                    start_pos, end_pos = drawWest(_MAZE[i].cell_coordinates)
                    pygame.draw.line(_screen, color, start_pos, end_pos, width)
            if j == 2:
                if _MAZE[i].cell_dimensions.dim_array[j]:
                    start_pos, end_pos = drawNorth(_MAZE[i].cell_coordinates)
                    pygame.draw.line(_screen, color, start_pos, end_pos, width)
            if j == 3:
                if _MAZE[i].cell_dimensions.dim_array[j]:
                    start_pos, end_pos = drawSouth(_MAZE[i].cell_coordinates)
                    pygame.draw.line(_screen, color, start_pos, end_pos, width)


def createChildTable():
    for x in range(_count):
        left_child = -1
        right_child = -1
        top_child = -1
        bottom_child = -1
        if x % MAZE_SIZE != 0:
            left_child = x - 1
        dic[x].append(left_child)
        if (x + 1) % MAZE_SIZE != 0:
            if x != _count - 1:
                right_child = x + 1
        dic[x].append(right_child)
        if x >= MAZE_SIZE:
            top_child = x - MAZE_SIZE
        dic[x].append(top_child)
        if x < (MAZE_SIZE * (MAZE_SIZE - 1)):
            bottom_child = x + MAZE_SIZE
        dic[x].append(bottom_child)


def get_node_by_index(index):
    return MAZE[index]


def display_screen(_MAZE):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    rectangle = pygame.Rect(40, 40, 322, 322)
    my_box_x1 = 42
    my_box_y1 = 42
    my_box_x2 = my_box_x1 + 20
    my_box_y2 = my_box_y1 + 20
    my_box_cords = coordinates(my_box_x1, my_box_y1, my_box_x2, my_box_y2)
    my_box = Box(my_box_cords, speed, screen)
    solution = [0]
    goal_node = get_node_by_index(solution.pop(0))
    my_goal = goal(goal_node.cell_coordinates, screen)
    my_ai = AI_agent(my_box, my_goal)
    screen.fill((28, 28, 28))
    pygame.draw.rect(screen, (255, 255, 255), rectangle, 2)
    DrawMaze(_MAZE, screen)
    pygame.display.flip()
    running = True
    go = False
    next_node = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    go = True
                if event.key == K_1:
                    solution = BreadthFirstSearch(my_graph, 0, _count - 1)
                    print("ok")
                if event.key == K_2:
                    solution = A_star(0, _count - 1, my_graph)
                    print("ok")
                if event.key == K_3:
                    DepthFirstSearch(my_graph, 0, visited, _count - 1)
                    solution = visited
                    print("ok")
        if go:
            my_ai.sensor(my_box, my_goal)
            if my_ai.actuator():
                if len(solution) != 0:
                    next_node = solution.pop(0)
                    print(next_node, end=", ")
                goal_node = get_node_by_index(next_node)
                my_goal._coordinates = goal_node.cell_coordinates
            my_box.Walk()
            my_box.drawBox()
            pygame.draw.rect(screen, (0, 0, 0), rectangle, 2)
            DrawMaze(_MAZE, screen)
            pygame.display.flip()
            time.sleep(sleep_time)


def load_maze(graph, _dic):
    for x in range(len(graph)):
        left_child = _dic[x][0]
        right_child = _dic[x][1]
        top_child = _dic[x][2]
        bottom_child = _dic[x][3]
        curr_node = MAZE[x].cell_dimensions
        if left_child != -1:
            if left_child in graph[x]:
                curr_node.East = False
                curr_node.update_dimensions()
        if right_child != -1:
            if right_child in graph[x]:
                curr_node.West = False
                curr_node.update_dimensions()
        if top_child != -1:
            if top_child in graph[x]:
                curr_node.North = False
                curr_node.update_dimensions()
        if bottom_child != -1:
            if bottom_child in graph[x]:
                curr_node.South = False
                curr_node.update_dimensions()


def BreadthFirstSearch(graph, curr_node, node_To_BeSearched):
    frontier = []
    explored = []
    if curr_node == node_To_BeSearched:
        return explored
    frontier.append(curr_node)
    while True:
        if len(frontier) == 0:
            return False
        node = frontier.pop(0)
        explored.append(node)
        for child in graph[node]:
            if (child not in frontier) or (child not in explored):
                if child == node_To_BeSearched:
                    explored.append(node_To_BeSearched)
                    return explored
                frontier.append(child)


def DepthFirstSearch(graph, curr_node, visited_nodes, node_To_BeSearched):
    flag = False
    if curr_node not in visited_nodes:
        visited_nodes.append(curr_node)
        if curr_node == node_To_BeSearched:
            return True
        for curr_successor in graph[curr_node]:
            if flag:
                return flag
            flag = DepthFirstSearch(graph, curr_successor, visited_nodes, node_To_BeSearched)
    return flag


def filter_arr(val, arr):
    while val in arr:
        arr.remove(val)


def create_graph(temp_arr, _graph):
    for k in range(_count):
        filter_arr(-1, temp_arr[k])
        if len(temp_arr[k]) == 2:
            if temp_arr[k][0] not in _graph[k]:
                _graph[k].append(temp_arr[k][0])
            if temp_arr[k][1] not in _graph[k]:
                _graph[k].append(temp_arr[k][1])
            if k not in _graph[temp_arr[k][0]]:
                _graph[temp_arr[k][0]].append(k)
            if k not in _graph[temp_arr[k][1]]:
                _graph[temp_arr[k][1]].append(k)
        else:
            n1 = random.randint(0, 1)
            n2 = random.randint(2, len(temp_arr[k]) - 1)
            if temp_arr[k][n1] not in _graph[k]:
                _graph[k].append(temp_arr[k][n1])
            if temp_arr[k][n2] not in _graph[k]:
                _graph[k].append(temp_arr[k][n2])
            if k not in _graph[temp_arr[k][n1]]:
                _graph[temp_arr[k][n1]].append(k)
            if k not in _graph[temp_arr[k][n2]]:
                _graph[temp_arr[k][n2]].append(k)
    return _graph


dic = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    16: [],
    17: [],
    18: [],
    19: [],
    20: [],
    21: [],
    22: [],
    23: [],
    24: [],
    25: [],
    26: [],
    27: [],
    28: [],
    29: [],
    30: [],
    31: [],
    32: [],
    33: [],
    34: [],
    35: [],
    36: [],
    37: [],
    38: [],
    39: [],
    40: [],
    41: [],
    42: [],
    43: [],
    44: [],
    45: [],
    46: [],
    47: [],
    48: [],
    49: [],
    50: [],
    51: [],
    52: [],
    53: [],
    54: [],
    55: [],
    56: [],
    57: [],
    58: [],
    59: [],
    60: [],
    61: [],
    62: [],
    63: []
}

my_graph = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    16: [],
    17: [],
    18: [],
    19: [],
    20: [],
    21: [],
    22: [],
    23: [],
    24: [],
    25: [],
    26: [],
    27: [],
    28: [],
    29: [],
    30: [],
    31: [],
    32: [],
    33: [],
    34: [],
    35: [],
    36: [],
    37: [],
    38: [],
    39: [],
    40: [],
    41: [],
    42: [],
    43: [],
    44: [],
    45: [],
    46: [],
    47: [],
    48: [],
    49: [],
    50: [],
    51: [],
    52: [],
    53: [],
    54: [],
    55: [],
    56: [],
    57: [],
    58: [],
    59: [],
    60: [],
    61: [],
    62: [],
    63: []
}

saved_graph = {
    0: [1, 8],
    1: [0, 2, 9],
    2: [1, 3, 10],
    3: [2, 11],
    4: [5, 12],
    5: [4, 13, 6],
    6: [5, 14, 7],
    7: [6, 15],
    8: [0, 16, 9],
    9: [1, 8, 17],
    10: [2, 11],
    11: [3, 10, 12, 19],
    12: [4, 11, 13, 20],
    13: [5, 12, 14],
    14: [6, 13, 15],
    15: [7, 14, 23],
    16: [8, 17, 24],
    17: [16, 18, 9],
    18: [17, 19, 26],
    19: [11, 18, 20, 27],
    20: [12, 19, 21, 28],
    21: [20, 29],
    22: [23, 30],
    23: [15, 22, 31],
    24: [16, 25, 32],
    25: [24, 33, 26],
    26: [18, 25, 34, 27],
    27: [26, 19, 28],
    28: [27, 20, 29],
    29: [21, 28, 37],
    30: [22, 31, 38],
    31: [23, 30, 39],
    32: [24, 40, 33],
    33: [25, 32, 41],
    34: [26, 35],
    35: [34, 36, 43],
    36: [35, 37, 44],
    37: [36, 38, 29, 45],
    38: [30, 37, 46, 39],
    39: [31, 38, 47],
    40: [32, 41, 48],
    41: [33, 40, 42],
    42: [41, 43, 50],
    43: [35, 42, 44, 51],
    44: [36, 43, 45, 52],
    45: [44, 37, 53],
    46: [38, 47, 54],
    47: [39, 46, 55],
    48: [40, 49, 56],
    49: [48, 57],
    50: [42, 51, 58],
    51: [43, 50, 59],
    52: [44, 53, 60],
    53: [52, 54, 45, 61],
    54: [53, 55, 46, 62],
    55: [47, 54, 63],
    56: [48, 57],
    57: [49, 56, 58],
    58: [50, 57, 59],
    59: [58, 60, 51],
    60: [52, 59, 61],
    61: [60, 62, 53],
    62: [61, 63, 54],
    63: [55, 62],
}


def A_star(_source, _destination, myGraph):
    _open = []
    _close = []
    _temp = []
    _open.append(_source)
    while len(_open) > 0:
        _temp = calc_min(_temp.copy(), _open, myGraph, _destination)
        node_current = _temp[len(_temp) - 1]
        if node_current == _destination:
            _close.append(node_current)
            return _close
        for node_current_successor in myGraph[node_current]:
            current_successor_cost = calc_distance(_close) + calc_weight()
            if node_current_successor in _open:
                if calc_distance(_close) <= current_successor_cost:
                    continue
            elif node_current_successor in _close:
                if calc_distance(_close) <= current_successor_cost:
                    _open.append(node_current_successor)
                    _close.remove(node_current_successor)
            else:
                _open.append(node_current_successor)
        _close.append(node_current)
    if _close[len(_close) - 1] != _destination:
        return False


def calc_weight():
    return 20


def calc_distance(_solution):
    distance = 0
    for x in range(len(_solution) - 1):
        distance += calc_weight()
    return distance


def calc_F(_solution, _goal):
    g = calc_distance(_solution)
    h = calc_heuristics(_solution, _goal)
    f = g + h
    return f


def calc_min(_solution, _open, myGraph, _goal):
    nextNode = 0
    _f = 10000
    for child in _open:
        if len(_solution) > 0:
            if child in myGraph[_solution[len(_solution) - 1]]:
                _solution.append(child)
                curr_f = calc_F(_solution, _goal)
                if _f >= curr_f:
                    _f = curr_f
                    nextNode = child
                _solution.remove(child)
    _solution.append(nextNode)
    return _solution


def calc_euclidean_distance(start, _goal):
    x1 = start.cell_coordinates.x1
    y1 = start.cell_coordinates.y1
    x2 = _goal.cell_coordinates.x2
    y2 = _goal.cell_coordinates.y2
    _x = x2 - x1
    _y = y2 - y1
    _x = _x ** 2
    _y = _y ** 2
    _z = math.sqrt(_x + _y)
    return _z


def calc_heuristics(_solution, my_goal):
    curr_node = _solution[len(_solution) - 1]
    if my_goal not in my_graph[curr_node] and \
            calc_euclidean_distance(get_node_by_index(curr_node), get_node_by_index(my_goal)) == 20:
        return 10000
    else:
        my_start = get_node_by_index(curr_node)
        my_goal = get_node_by_index(my_goal)
        _h = calc_euclidean_distance(my_start, my_goal)
    return _h


def random_search(_my_graph, curr_node, _parent_node):
    _children = _my_graph[curr_node]
    index = random.randint(0, len(_children) - 1)
    if _children[index] == _parent_node:
        return random_search(_my_graph, curr_node, _parent_node)
    else:
        return _children[index], curr_node


def save_graph(_my_graph):
    print("saved_graph = {")
    for x in _my_graph.items():
        print(x[0], ":", x[1], ",")
    print("}")


def create_random_graph():
    dic_copy = copy.deepcopy(dic)
    create_graph(dic_copy, my_graph)


if __name__ == '__main__':
    visited = []
    MAZE_SIZE = 8
    WIDTH = HEIGHT = 400
    singleCellSize = 40
    padding = 40
    set_FPS(120)
    MAZE = createMaze(MAZE_SIZE, singleCellSize, padding)
    _count = MAZE_SIZE * MAZE_SIZE
    createChildTable()
    create_random_graph()
    # save_graph(my_graph)
    # my_graph = saved_graph
    load_maze(my_graph, dic)
    var_temp = []
    display_screen(MAZE)
