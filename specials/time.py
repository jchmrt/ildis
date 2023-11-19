from datetime import datetime

from PIL import Image as image
from django.conf import settings

import pytz

cur_tz = pytz.timezone("Europe/Amsterdam")

class TimePortrait:
    def __init__(self, background=None):
        self.background = background

        self.load_digits()
        self.update_time()

    def load_digits(self):
        self.digits = []
        for i in range(0, 10):
            self.digits.append(self.load_digit(i))

    def load_digit(self, d):
        img = image.open(str(settings.BASE_DIR) +
                          '/iltext/bitfont-digits/' +
                          str(ord(str(d))) +
                          ".pbm")

        self.digit_width = img.width
        self.digit_height = img.height
        return img.load()
        
    def update_time(self):
        def nstr(n):
            return str(n).zfill(2)

        now = datetime.now(cur_tz)
        self.hour = now.hour
        self.minute = now.minute

    def tick(self, ctrl, delta):
        if self.background:
            self.background.tick(ctrl, delta)

        self.update_time()

    def render(self, ctrl):
        if self.background == None:
            ctrl.fill(0, 0, 0)
        else:
            self.background.render(ctrl)

        hour_digit_1 = self.hour // 10
        hour_digit_2 = self.hour % 10
        minute_digit_1 = self.minute // 10
        minute_digit_2 = self.minute % 10

        self.render_digit(ctrl, hour_digit_1, 0, 0)
        self.render_digit(ctrl, hour_digit_2, 5, 0)
        self.render_digit(ctrl, minute_digit_1, 0, 8)
        self.render_digit(ctrl, minute_digit_2, 5, 8)
        

    def render_digit(self, ctrl, digit, offset_x, offset_y):
        pix = self.digits[digit]

        for i in range(self.digit_width):
            for j in range(self.digit_height):
                if pix[i, j] == 255:
                    ctrl.set_pixel(
                        i + offset_x,
                        j + offset_y,
                        255,
                        255,
                        255
                    )
