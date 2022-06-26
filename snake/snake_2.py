import threading
import random
from enum import Enum

from ildis.ildis import Disp
from iltext.iltext import Iltext
from ilcon.waves import Waves

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



class Tile:
    def __init__(self):
        self.snake_1 = None
        self.snake_2 = None
        self.food = False
        self.lock = threading.RLock()

    def completely_empty(self):
        return (not self.snake_1) and (not self.snake_2) and (not self.food)

    def occupied(self):
        with self.lock:
            return self.snake_1 and not self.snake_1.is_invisible()

    def move_to_spot(self, snake):
        with self.lock:
            if self.occupied():
                return False
            else:
                if self.snake_1:
                    self.snake_2 = self.snake_1
                    self.snake_2.waiting_tiles += 1

                self.snake_1 = snake
                return True

    def leave_spot(self, snake):
        with self.lock:
            if self.snake_1 == snake:
                self.snake_1 = self.snake_2
                self.snake_2 = None

                if self.snake_1:
                    self.snake_1.activate()
            else:
                raise Exception()

    def add_food(self):
        self.food = True

    def remove_food(self):
        with self.lock:
            self.food = False
            if self.snake_1:
                self.snake_1.activate()

    def space_to_reserve(self):
        with self.lock:
            return not self.snake_1

    def reserve_spot(self, snake):
        with self.lock:
            if self.snake_1:
                self.snake_2 = snake
            else:
                self.snake_1 = snake

class SnakeState(Enum):
    WAITING = 0
    SPAWNING = 1
    PLAYING = 2

class Snake:
    COLORS = [
        ((255, 255, 0), (160, 255, 140)),
        ((0, 0, 255), (140, 228, 255)),
        ((255, 0, 0), (255, 140, 140)),
        ]

    COLOR_NAMES = [
        "green",
        "blue",
        "red"
        ]

    def __init__(self, game, snake_id, consumer):
        consumer.set_snake(self)
        self.consumer = consumer

        self.color = self.COLORS[snake_id][0]
        self.consumer.send_json(
            { "msg": "color",
              "color": self.COLORS[snake_id][1],
              "color_name" : self.COLOR_NAMES[snake_id]})



        self.snake_id = snake_id
        self.game = game
        self.spawn_time = 2
        self.invisible_time = 1
        self.state = SnakeState.SPAWNING

        self.waiting_tiles = 0
        self.cur_t = 0
        self.tiles = []
        self.MOVE_TIME = 0.3

        self.direction = Direction.EAST
        self.score = 0

        self.lock = threading.RLock()

        self.get_on_map()

    def cur_pos(self):
        return self.tiles[-1]

    def get_on_map(self):
        start_y = self.snake_id
        start_x = 0
        start_length = 3

        for i in range(start_length):
            x = start_x + i
            y = start_y
            tile = self.game.at(x, y)

            if tile.occupied():
                self.state = SnakeState.WAITING
                self.waiting_tiles += 1


            tile.reserve_spot(self)

            self.tiles.append((x, y))

    def activate(self):
        with self.lock:
            if self.state is SnakeState.WAITING:
                self.waiting_tiles -= 1
                if self.waiting_tiles == 0:
                    self.state = SnakeState.SPAWNING

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

        next_tile = self.game.at(nx, ny)

        if next_tile.occupied():
            return True
        else:
            self.game.at(nx, ny).move_to_spot(self)

            self.tiles.append((nx, ny))

            if next_tile.food:
                self.increment_score()
                self.game.add_food()
                next_tile.remove_food()
            else:
                ox, oy = self.tiles.pop(0)
                self.game.at(ox, oy).leave_spot(self)

    def is_invisible(self):
        return self.invisible_time > 0

    def tick(self, delta):
        with self.lock:
            if self.invisible_time > 0:
                self.invisible_time -= delta

            if self.state is SnakeState.WAITING:
                pass
            elif self.state is SnakeState.SPAWNING:
                if self.invisible_time <= 0:
                    self.spawn_time -= delta
                    if self.spawn_time < 0:
                        self.state = SnakeState.PLAYING
            elif self.state is SnakeState.PLAYING:
                self.play(delta)
            else:
                raise Exception("Unknown SnakeState")

    def disconnect(self):
        with self.lock:
            for (x, y) in self.tiles:
                self.game.at(x, y).leave_spot(self)

            self.game.remove_snake(self)

            self.consumer.game_over()

    def increment_score(self):
        self.score += 1
        self.consumer.send_json({ "msg": "score", "score": self.score })

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


    def play(self, delta):
        self.cur_t += delta

        if self.cur_t >= self.MOVE_TIME:
            self.cur_t = 0
            try:
                game_over = self.move()

                if game_over:
                    self.disconnect()

            except Exception as e:
                print(e)


class SnakeGame(Disp):
    WIDTH = 15
    HEIGHT = 10
    MAX_SNAKES = 3

    def __init__(self):
        self.lock = threading.RLock()
        self.grid = [ [ Tile() for x in range(self.WIDTH) ]
                      for y in range(self.HEIGHT) ]

        self.snakes = []
        self.waiting = []
        self.add_food()

        self.cur_t = 0

        msg = ("     Play multiplayer SNAKE on this window! " +
               " go to leddie.nl    Beat the high score!   " +
               "   go to leddie.nl  ")
        self.text = Iltext(msg, (100, 100, 100), Waves(0.15))

    def at(self, x, y):
        return self.grid[y][x]

    def connect_snake(self, consumer):
        with self.lock:
            if len(self.snakes) < self.MAX_SNAKES:
                self.add_snake(consumer)
            else:
                self.waiting.append(consumer)

    def find_id(self):
        ids = [0, 1, 2]
        for snake in self.snakes:
            ids.remove(snake.snake_id)

        return ids[0]

    def add_snake(self, consumer):
        snake_id = self.find_id()
        snake = Snake(self, snake_id, consumer)
        self.snakes.append(snake)

    def remove_snake(self, snake):
        with self.lock:
            self.snakes.remove(snake)

            if len(self.waiting) > 0:
                next_consumer = self.waiting.pop(0)
                self.connect_snake(next_consumer)

    def add_food(self):
        empties = 0
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.at(i, j).completely_empty():
                    empties += 1

        index = random.randrange(empties)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.at(i, j).completely_empty():
                    index -= 1
                    if index == 0:
                        self.at(i, j).add_food()
                        return

        self.add_food()


    def tick(self, ctrl, delta):
        if len(self.snakes) > 0:
            self.cur_t += delta

            for snake in self.snakes:
               snake.tick( delta)
        else:
            self.text.tick(ctrl, delta)

    def render(self, ctrl):
        if len(self.snakes) > 0:
            self.render_game(ctrl)
        else:
            self.text.render(ctrl)

    def render_game(self, ctrl):
        ctrl.fill(0, 0, 0)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                tile = self.at(i, j)
                if tile.snake_1:
                    snake = tile.snake_1
                    if snake.state is SnakeState.PLAYING:
                        ctrl.set_pixel(i, j,
                                       snake.color[0],
                                       snake.color[1],
                                       snake.color[2])
                    else:
                        period = 0.5
                        mod = abs(((self.cur_t % period) / period) - 0.5)
                        if snake.is_invisible():
                            mod *= 0.5
                        ctrl.set_pixel(i, j,
                                       snake.color[0] * mod,
                                       snake.color[1] * mod,
                                       snake.color[2] * mod)

                elif tile.food:
                    ctrl.set_pixel(i, j, 255, 255, 255)

        ctrl.render()
