import struct
import threading
import time
import logging
import os

class Controller(threading.Thread):
    WIDTH = 15
    HEIGHT = 10
    active_il = None
    daemon=True

    def __init__(self, queue, lock):
        super(Controller, self).__init__()

        self.queue = queue
        self.lock = lock

        self.fifo = os.open("/home/pi/leddie/socket", os.O_WRONLY)
        self.logger = logging.getLogger(__name__)
        self.previous_time = time.monotonic()

    def set_pixel(self, x, y, r, g, b):
        os.write(self.fifo,
                 struct.pack("BBBBBB", 0, x, y, r, g, b))

    def fill(self, r, g, b):
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                self.set_pixel(i, j, r, g, b)

    def render(self):
        os.write(self.fifo, struct.pack("B", 2))

    def set_brightness(self, b):
        os.write(self.fifo, struct.pack("BB", 3, b))

    def render_all(self):
        if self.active_il:
            self.active_il.render(self)
            self.render()

    def tick(self):
        current_time = time.monotonic()
        if self.active_il:
            self.active_il.tick(self, current_time - self.previous_time)

        self.previous_time = current_time
        time.sleep(1 / 100)

    def process(self, item):
        try:
            if not item:
                self.fill(0, 0, 0)
                self.render()
                self.active_il = None
            else:
                self.active_il = item
                self.previous_time = time.monotonic()

        except:
            self.logger.warning("Error processing controller command")
        
    def run(self):
        while True:
            with self.lock:
                if not self.queue.empty():
                    self.process(self.queue.get())

            self.render_all()
            self.tick()
