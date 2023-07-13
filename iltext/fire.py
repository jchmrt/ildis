
from ildis.ildis import Disp
import random
import math

class FireParticle(Disp):
    def __init__(self):
        self.x = random.randrange(0, 10)
        self.y = 14

        self.move_time = 0.20 + random.random() * 0.11
        self.cur_t = 0
        self.decay = 0.3 + random.random() * 0.6

        self.value = 1

    def move(self):
        rand = random.random()
        left_right_chance = 0.4

        self.y -= 1

        if rand < left_right_chance:
            self.x += 1
        elif rand < left_right_chance * 2:
            self.x -= 1

    def done(self):
        return self.value <= 0 or self.y < 0

    def tick(self, delta):
        self.cur_t += delta
        if self.cur_t > self.move_time:
            self.move()
            self.cur_t = 0

        self.value -= self.decay * delta


    COLOR_GRADIENT = [
        (0.0, (1, 0, 0)),
        (0.25, (1, 0.4 ,0.0)),
        (0.35, (1, 0.35, 0)),
        (0.75, (1, 0.24, 0)),
	(0.85, (0.6, 0, 0)),
        (1.0, (0, 0, 0)),
    ]


    def pixel(self, x, width=100, map=[], spread=1):
        def gaussian(x, a, b, c, d=0):
            return a * math.exp(-(x - b)**2 / (2 * c**2)) + d
    
        width = float(width)
        r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
        g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
        b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
        return min(1.0, r), min(1.0, g), min(1.0, b)
    

    def get_color(self):
        def gc(x, gamma=2.4):
            return round(math.pow(float(x) / 255.0, gamma) * 255.0);

        cur = 1 - self.value
        r, g, b = self.pixel(cur*100, map=self.COLOR_GRADIENT)
        return gc(r * 255), gc(g * 255), gc(b * 255)


    def render(self, ctrl):
        color = self.get_color()
        ctrl.set_pixel(self.x, self.y,
                       color[0],
                       color[1],
                       color[2])


class Fire(Disp):
    def __init__(self):
        self.particles = []
        self.to_add = 0


    def tick(self, ctrl, delta):
        self.to_add += delta * 80

        if self.to_add > 1:
            n_new = round(self.to_add)
            self.to_add = 0
            for i in range(n_new):
                self.particles.append(FireParticle())
                

        to_remove = []
        for i, particle in enumerate(self.particles):
            particle.tick(delta)
            if particle.done():
                to_remove.append(i)

        removed = 0
        for i in to_remove:
            del self.particles[i - removed]
            removed += 1

    def render(self, ctrl):
        ctrl.fill(0, 0, 0)

        for particle in self.particles:
            particle.render(ctrl)
