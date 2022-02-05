import random
import queue
from enum import Enum

from ildis.ildis import Disp

class EmptyTile:
    pass

class SnakeTile:
    pass

class FoodTile:
    pass

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Snake(Disp):
    INIT_LEN = 3

    def __init__(self, game):
        self.game = game
        self.grid = game.grid
        self.tiles = []
        self.direction = Direction.EAST

        for i in range(self.INIT_LEN):
            self.grid[0][i] = SnakeTile()
            self.tiles.append((i, 0))

    def cur_pos(self):
        return self.tiles[-1]


    def move(self, direction):
        self.direction = direction

        dx = 0
        dy = 0
        if direction is Direction.NORTH:
            dy = -1
        elif direction is Direction.SOUTH:
            dy = 1
        elif direction is Direction.WEST:
            dx = -1
        elif direction is Direction.EAST:
            dx = 1

        x, y = self.cur_pos()
        nx = (x + dx) % self.game.WIDTH
        ny = (y + dy) % self.game.HEIGHT

        next_tile = self.grid[ny][nx]

        if isinstance(next_tile, SnakeTile):
            return True
        else:
            self.grid[ny][nx] = SnakeTile()
            self.tiles.append((nx, ny))

            if isinstance(next_tile, EmptyTile):
                ox, oy = self.tiles.pop(0)
                self.grid[oy][ox] = EmptyTile()
            else:
                self.game.add_food()

            return False



class SnakeGame(Disp):
    WIDTH = 15
    HEIGHT = 10
    MOVE_TIME = 0.3

    def __init__(self):
        self.grid = [ [ EmptyTile()
                        for x in range(self.WIDTH) ]
                      for y in range(self.HEIGHT) ]

        self.snake = Snake(self)
        self.add_food()

        self.cur_t = 0
        self.input_queue = queue.Queue()

    def add_food(self):
        empties = 0
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if isinstance(self.grid[j][i], EmptyTile):
                    empties += 1

        index = random.randrange(empties)
        print(index)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if isinstance(self.grid[j][i], EmptyTile):
                    index -= 1
                    if index == 0:
                        self.grid[j][i] = FoodTile()

    def execute_move(self):
        direction = self.snake.direction
        if not self.input_queue.empty():
            direction = self.input_queue.get()

        return self.snake.move(direction)

    def tick(self, ctrl, delta):
        self.cur_t += delta

        if self.cur_t >= self.MOVE_TIME:
            self.cur_t = 0
            return self.execute_move()
        else:
            return False
        

    def render(self, ctrl):
        ctrl.fill(0, 0, 0)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                tile = self.grid[j][i]
                if isinstance(tile, SnakeTile):
                    ctrl.set_pixel(i, j, 255, 255, 255)
                if isinstance(tile, FoodTile):
                    ctrl.set_pixel(i, j, 0, 255, 0)

        ctrl.render()


class SnakeGameWrapper(Disp):
    def __init__(self):
        self.game = SnakeGame()

    def put(self, item):
        self.game.input_queue.put(item)

    def tick(self, ctrl, delta):
        if self.game.tick(ctrl, delta):
            self.game = SnakeGame()

    def render(self, ctrl):
        self.game.render(ctrl)
