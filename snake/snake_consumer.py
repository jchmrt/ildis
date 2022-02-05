import json
from channels.generic.websocket import WebsocketConsumer

from django.apps import apps
from snake.snake import SnakeGameWrapper, Direction

snake_wrapper = None

class SnakeConsumer(WebsocketConsumer):
    def connect(self):
        global snake_wrapper
        snake_wrapper = SnakeGameWrapper()

        ilcon = apps.get_app_config('ilcon').ilcon
        ilcon.send(snake_wrapper)

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        direction = text_data_json['direction']

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

        snake_wrapper.put(direction)
