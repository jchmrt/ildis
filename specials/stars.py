import random
from ildis.ildis import Disp

import math

def gc(x, gamma=2.1):
    return min(255, max(0, round(math.pow(float(x) / 255.0, gamma) * 255.0)))

def rcol(x):
    return min(255, max(0, round(x)))


class Star(Disp):
    def __init__(self):
        def tocol(x):
            return min(255, max(0, round(x * 255)))
            
        self.x = 0
        self.y = random.randrange(0, 10)
        self.speed = 10 + (25 - math.pow(random.random() * 5, 2))


        value = 0.3 + random.random() * 0.7
        color = random.random()
        self.r = tocol(color * value * 1.3)
        self.g = tocol(0.05 * value)
        self.b = tocol(-0.1 + (1 - color) * 0.8 * value)

    def tick(self, delta):
        self.x += self.speed * delta

    def done(self):
        return round(self.x) >= 15

    def render(self, ctrl):
        base_x = math.floor(self.x)
        dist = self.x - base_x
        next_x = base_x + 1

        ctrl.set_pixel(base_x, self.y,
                       rcol(self.r * (1 - dist)),
                       rcol(self.g * (1 - dist)),
                       rcol(self.b * (1 - dist)))

        if next_x < 15:
            ctrl.set_pixel(base_x, self.y,
                           rcol(self.r * dist),
                           rcol(self.g * dist),
                           rcol(self.b * dist))
                       
            


class Stars (Disp):
    def __init__(self):
        self.stars = []
        self.back_col = [0,0,0]

    def tick(self, ctrl, delta):
        if random.random() < 0.04 and len(self.stars) < 50:
            self.stars.append(Star())
        if random.random() < 0.008 and len(self.stars) < 50:
            for i in range(random.randrange(5) + 1):
                self.stars.append(Star())

        avg_color = [0,0,0]
        to_remove = []
        for i, star in enumerate(self.stars):
            star.tick(delta)
            if star.done():
                avg_color[0] += star.r
                avg_color[1] += star.g
                avg_color[2] += max(0, star.b) 

                to_remove.append(i)

        for i in range(3):
            self.back_col[i] *= 0.964
            self.back_col[i] += avg_color[i] / 1.5

        removed = 0
        for i in to_remove:
            del self.stars[i - removed]
            removed += 1
        

    def render(self, ctrl):
        ctrl.fill(gc(self.back_col[0]),
                  gc(self.back_col[1]),
                  gc(self.back_col[2], 1.8))
        
        for star in self.stars:
            star.render(ctrl)

        ctrl.render()
        
