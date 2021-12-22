import queue
import threading
import logging

from ilcon.waves import Waves
from ilcon.controller import Controller

class Ilempty:
    def __init__(self):
        self.rendered = False

    def tick(self, ctrl, delta):
        pass

    def render(self, ctrl):
        if not self.rendered:
            for i in range(15):
                for j in range(10):
                    ctrl.set_pixel(i, j, 0, 0, 0)

            ctrl.render()
            self.rendered = True


class Ilcon:

    def __init__(self):
        self.lock = threading.Lock()
        self.queue = queue.Queue()
        self.logger = logging.getLogger(__name__)
        
        self.controller = Controller(self.queue, self.lock)
        self.controller.start()

    def send(self, item):
        with self.lock:
            self.queue.put(item)

    def clear(self):
        with self.lock:
            self.queue.put(Ilempty())

    def set_brightness(self, brightness):
        self.controller.set_brightness(brightness)
