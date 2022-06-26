from channels.generic.websocket import JsonWebsocketConsumer

from django.apps import apps
from snake.snake_2 import SnakeGame, Direction
from snake.models import SnakeScore

import queue
import logging

logger = logging.getLogger(__name__)
snake_game = None

class SnakeConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.input_queue = queue.Queue()
        self.snake = None

        self.accept()


    def disconnect(self, close_code):
        if self.snake:
            self.snake.disconnect()

    def set_snake(self, snake):
        self.snake = snake

    def receive_json(self, content):
        if content["msg"] == "dir":
            self.receive_direction(content)
        elif content["msg"] == "new":
            self.receive_new_game(content)
        else:
            logger.error("Unrecognized message from client")

            
    def initialize_snake_game(self):
        global snake_game
        snake_game = SnakeGame()

    def game_over(self):
        score_key = None

        try:
            score_key = SnakeScore.add_score(self.snake.score,
                                             self.user_name,
                                             self.user_hallway)

        except Exception as e:
            logger.error("Could not save high score %s %s %s %s",
                         e,
                         self.snake.score,
                         self.user_name,
                         self.user_hallway)

        self.send_json({ "msg": "game_over",
                         "score_key": score_key })


        self.snake = None
        self.close()

    def receive_new_game(self, content):
        global snake_game

        if not snake_game:
            self.initialize_snake_game()

        try:
            self.user_name = content["name"]
            self.user_hallway = content["hall"]
        except:
            logger.error("new game message not correct")

        ilcon = apps.get_app_config('ilcon').ilcon
        ilcon.send(snake_game)

        snake_game.connect_snake(self)


    def receive_direction(self, content):
        direction = content['direction']

        if direction == "n":
            direction = Direction.NORTH
        elif direction == "s":
            direction = Direction.SOUTH
        elif direction == "e":
            direction = Direction.EAST
        elif direction == "w":
            direction = Direction.WEST
        else:
            return

        if self.input_queue.qsize() < 20:
            self.input_queue.put(direction)
