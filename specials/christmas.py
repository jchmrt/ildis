import math

class GreenRed:
    def __init__(self, brightness=1.0):
        self.t = 0.0
        self.brightness = brightness

    def tick(self, ctrl, delta):
        self.t = self.t + 0.8

    def render(self, ctrl):
        for x in range(ctrl.WIDTH):
            for y in range(ctrl.HEIGHT):
                brightness = self.brightness

                phase = math.sin(x * 0.9 + y * 1.1 + self.t * 0.16)

                if phase > 0.8:
                    phase = 1
                elif phase < -0.8:
                    phase = -1
                else:
                    phase = phase * 1.25


                red = ((math.pow(phase, 1) + 1) / 2) * 1.4
                green = 1 - red

                ctrl.set_pixel(x, y,
                               round(red * 255 * brightness),
                               round(green * 255 * brightness),
                               0)

