import random
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

    def is_irrelevant(self, other):
        if self is Direction.NORTH or self is Direction.SOUTH:
            return other is Direction.NORTH or other is Direction.SOUTH
        else:
            return other is Direction.WEST or other is Direction.EAST


class Snake(Disp):
    INIT_LEN = 3

    def __init__(self, game, consumer):
        self.game = game
        self.grid = game.grid
        self.tiles = []
        self.direction = Direction.EAST
        self.consumer = consumer
        self.score = 0

        for i in range(self.INIT_LEN):
            self.grid[0][i] = SnakeTile()
            self.tiles.append((i, 0))

    def cur_pos(self):
        return self.tiles[-1]

    def increment_score(self):
        self.score += 1
        self.consumer.send_json({ "score": self.score })

    def discard_moves(self):
        while not self.consumer.input_queue.empty():
            next_dir = self.consumer.input_queue.queue[0]
            if self.direction.is_irrelevant(next_dir):
                self.consumer.input_queue.get()
            else:
                return

    def process_moves(self):
        self.discard_moves()

        if not self.consumer.input_queue.empty():
            self.direction = self.consumer.input_queue.get()

    def move(self):
        self.process_moves()
        direction = self.direction

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
            else:               # Eating food:
                self.increment_score()
                self.game.add_food()

            return False



class SnakeGame(Disp):
    MOVE_TIME = 0.3
    WIDTH = 10
    HEIGHT = 15

    def __init__(self, consumer):
        self.grid = [ [ EmptyTile()
                        for x in range(self.WIDTH) ]
                      for y in range(self.HEIGHT) ]

        self.snakes = []
        self.add_food()
        self.snake = Snake(self, consumer)

        self.cur_t = 0

    def add_food(self):
        empties = 0
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if isinstance(self.grid[j][i], EmptyTile):
                    empties += 1

        index = random.randrange(empties)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if isinstance(self.grid[j][i], EmptyTile):
                    index -= 1
                    if index == 0:
                        self.grid[j][i] = FoodTile()

    def execute_move(self):
        return self.snake.move()

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
    def __init__(self, consumer):
        self.game = SnakeGame(consumer)
        self.consumer = consumer

    def tick(self, ctrl, delta):
        if self.game.tick(ctrl, delta):
            self.game = SnakeGame(self.consumer)

    def render(self, ctrl):
        self.game.render(ctrl)
