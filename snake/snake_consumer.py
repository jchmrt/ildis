from channels.generic.websocket import JsonWebsocketConsumer

from django.apps import apps
from snake.snake import SnakeGameWrapper, Direction

import queue

snake_wrapper = None

class SnakeConsumer(JsonWebsocketConsumer):
    def connect(self):
        global snake_wrapper
        snake_wrapper = SnakeGameWrapper(self)

        ilcon = apps.get_app_config('ilcon').ilcon
        ilcon.send(snake_wrapper)

        self.input_queue = queue.Queue()

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content):
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

        self.input_queue.put(direction)
