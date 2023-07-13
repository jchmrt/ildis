import logging

from PIL import Image as image
from django.conf import settings

from ildis.ildis import Disp

class FlashText(Disp):
    """Display text by flashing one letter at a time.
    """

    def __init__(self,
                 text,
                 color=(255, 255, 255),
                 border_color=(100, 100, 100),
                 background=None,
                 repeat=True):
        self.logger = logging.getLogger(__name__)
        self.text = text
        self.color = color
        self.border_color = border_color
        self.background = background
        self.repeat = repeat

        self.chars = [ ord(c) for c in text ]
        self.char_arrs = self.init_arrs(self.chars)
        self.cur_char = 0
        self.t = 0

        self.time_per_letter = 0.62
        self.pause_time = 0.14


    def init_arrs(self, chars):
        arrs = []

        for char in chars:
            arrs.append(self.get_char_arr(char))

        return arrs

    def get_char_arr(self, char):
        try:
            img = self.load(char)
            pix = img.load()
            arr = []

            for i in range(img.width):
                arr.append([ pix[i, j] for j in range(img.height) ])

            return arr
        except:
            self.logger.warn("Character not found: " + str(char))

    def load(self, char):
        return image.open(str(settings.BASE_DIR) +
                          '/iltext/bitfont-new/' +
                          str(char) +
                          ".pbm")

    def tick(self, ctrl, delta):
        if self.background:
            self.background.tick(ctrl, delta)

        self.t = self.t + delta
        if self.t >= self.time_per_letter:
            self.t = 0.0
            self.cur_char += 1

            if self.cur_char >= len(self.char_arrs):
                self.cur_char = 0
                self.done = True


    def draw_background(self, ctrl):
        if self.background:
            self.background.render(ctrl)
        else:
            ctrl.fill(0, 0, 0)

    def draw_border(self, ctrl):
        c = self.border_color

        for i in range(ctrl.WIDTH):
            ctrl.set_pixel(i, 0, c[0], c[1], c[2])
            ctrl.set_pixel(i, ctrl.HEIGHT-1, c[0], c[1], c[2])

        for j in range(ctrl.HEIGHT):
            ctrl.set_pixel(0, j, c[0], c[1], c[2])
            ctrl.set_pixel(ctrl.WIDTH-1, j, c[0], c[1], c[2])


    def render(self, ctrl):
        self.draw_background(ctrl)
        self.draw_border(ctrl)

        cur_char_arr = self.char_arrs[self.cur_char]

        w = len(cur_char_arr)
        h = len(cur_char_arr[0])

        if self.t > self.pause_time:
            for i in range(w):
                for j in range(h):
                    try:
                        if cur_char_arr[i][j] == 255:
                            ctrl.set_pixel(i-3, j-1,
                                           self.color[0],
                                           self.color[1],
                                           self.color[2])
                    except:
                        pass
                    
