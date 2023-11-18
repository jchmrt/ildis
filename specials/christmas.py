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


class ChristmasTree:
    def __init__(self, background=None):
        self.background = background

        self.lights = []

        for i in range(10):
            l = []
            for j in range(15):
                l.append(random.random() < 0.2)

            self.lights.append(l)


    def tick(self, ctrl, delta):
        if self.background:
            self.background.tick(ctrl, delta)

        for i in range(10):
            for j in range(15):
                if self.lights[i][j] and random.random() < delta * 0.35:
                    self.lights[i][j] = not self.lights[i][j]
                elif (not self.lights[i][j] and random.random() < delta * 0.16
                      and not self.lights[(i-1) % 10][j]
                      and not self.lights[(i+1) % 10][j]):
                    self.lights[i][j] = not self.lights[i][j]

    def render(self, ctrl):
        if self.background:
            self.background.render(ctrl)
        
        self.draw_green(ctrl)
        self.draw_trunk(ctrl)
        self.draw_star(ctrl)

    def draw_green(self, ctrl):
        for j in range(12):
            w = (j // 2) * 2
            s = round((ctrl.WIDTH - w) / 2)

            for i in range(s, s+w):
                if self.lights[i][j] and i > s and i < s+w-1:
                    ctrl.set_pixel(i, j,
                                   255, 180, 30)
                else:
                    ctrl.set_pixel(i, j,
                                   0, 60, 0)


    def draw_trunk(self, ctrl):
        for j in range(12, 15):
            for i in range(3, 7):
                ctrl.set_pixel(i, j,
                               50, 20, 2)

    def draw_star(self, ctrl):
        for j in range(0, 2):
            for i in range(4, 6):
                ctrl.set_pixel(i, j,
                               255, 255, 0)
