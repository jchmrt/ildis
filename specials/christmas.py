from django.apps import apps

import math
import random

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


class SnowFlake:
    def __init__(self, ctrl):
        self.t = 0.0
        self.ctrl = ctrl

        self.reset_position()

        self.x = random.randrange(0, self.ctrl.WIDTH)
        self.y = random.randrange(0, self.ctrl.HEIGHT)

        self.direction = (random.randrange(0, 2) * 2) - 1

        self.speed = random.random() * 2 + 0.5
        self.color = random.random() * 120 + 80


    def reset_position(self):
        self.x = random.randrange(0, self.ctrl.WIDTH)
        self.y = 0


    def tick(self, ctrl, delta):
        self.t = self.t + delta

        if random.random() < 0.3 * delta:
            self.direction *= -1

        self.x += self.direction * delta * 0.8
        self.y += delta * self.speed

        if self.y > self.ctrl.HEIGHT + 1:
            self.reset_position()

    def render(self, ctrl):
        ctrl.set_pixel(round(self.x), round(self.y),
                       round(self.color),
                       round(self.color),
                       255)


class Snow:
    def __init__(self):
        self.t = 0.0

        self.ctrl = apps.get_app_config('ilcon').ilcon.controller

        self.flakes = []
        n_flakes = 60

        for i in range(n_flakes):
            self.flakes.append(SnowFlake(self.ctrl))


    def tick(self, ctrl, delta):
        self.t = self.t + delta

        for flake in self.flakes:
            flake.tick(ctrl, delta)

    def render(self, ctrl):
        ctrl.fill(0, 0, 0)

        for flake in self.flakes:
            flake.render(ctrl)
