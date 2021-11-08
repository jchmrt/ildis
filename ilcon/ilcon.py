import queue
import threading
import logging

from ilcon.waves import Waves
from ilcon.controller import Controller


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
