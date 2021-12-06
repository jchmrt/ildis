import logging

from PIL import Image as image

from django.conf import settings

class Iltext:
    def __init__(self, text):
        self.logger = logging.getLogger(__name__)

        self.text = text
        self.chars = [ ord(c) for c in text ]
        self.arr = self.init_arr()
        
        self.t = 0.0
        self.offset = 0


    def init_arr(self):
        arr = []

        for i in range(3):
            self.add_char(ord(' '), arr)

        for char in self.chars:
            self.add_char(char, arr)

        for i in range(3):
            self.add_char(ord(' '), arr)


        return arr


    def add_char(self, char, arr):
        try:
            img = self.load(char)
            pix = img.load()

            for i in range(img.width):
                arr.append([ pix[i, j] for j in range(img.height) ])

            arr.append([ 0 for j in range(img.height) ])

                
        except:
            self.logger.info("Character not found: " + str(char))


    def load(self, char):
        return image.open(str(settings.BASE_DIR) +
                          '/iltext/bitfont/' +
                          str(char) +
                          ".pbm")


    def tick(self, ctrl, delta):
        self.t = self.t + delta
        if self.t >= 0.07:
            self.t = 0.0
            self.offset = self.offset + 1

            if self.offset > len(self.arr) - 1:
                self.offset = 0

    def render(self, ctrl):
        ctrl.fill(0, 0, 0)

        for i in range(ctrl.WIDTH):
            for j in range(ctrl.HEIGHT):
                x = i + self.offset - ctrl.WIDTH
                y = j
                try:
                    if self.arr[x][y] == 255:
                        ctrl.set_pixel(i, j, 255, 255, 255)
                except:
                    pass

        ctrl.render()
