import math
from datetime import datetime
from dateutil.relativedelta import relativedelta

from iltext.iltext import Iltext
from ilcon.waves import Waves

class IltextBuilder:
    def __init__(self):
        self.waves = Waves(0.36)

    def create_object(self):
        text = self.create_text()

        return Iltext(text, repeat=False, background=self.waves)

class CountdownBuilder(IltextBuilder):
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.n = 0

    def create_countdown_text(self):
        rel_date = relativedelta(self.date, datetime.now())
        text = ""

        if rel_date.weeks > 0:
            text += str(rel_date.weeks) + " weeks, "

        if rel_date.days > 0:
            text += str(rel_date.days) + " days, "

        if rel_date.hours > 0:
            text += str(rel_date.hours) + " hours, "

        if rel_date.minutes > 0:
            text += str(rel_date.minutes) + " mins, "

        text += str(rel_date.seconds) + " secs"
        return text

    def create_leddie_text(self):
        return "  Go to leddie.nl to send a new years message!  "

    def create_text(self):
        self.n = self.n + 1

        if self.n % 3 == 0:
            return self.create_leddie_text()
        else:
            return self.create_countdown_text()

        
import random
import math


class Particle:
    def __init__(self, color, x, y, direction, speed):
        self.x = x
        self.y = y
        self.color = color
        self.bright = 7
        self.direction = direction
        self.speed = speed

    @property
    def done(self):
        return self.bright < 0.0005

    def tick(self, ctrl, delta):
        self.x += math.cos(self.direction) * delta * self.speed
        self.y += math.sin(self.direction) * delta * self.speed
        self.speed = self.speed * 0.98

        self.bright *= 0.95

    def render(self, ctrl):
        ctrl.set_pixel(self.x, self.y,
                       self.color[0] * self.bright,
                       self.color[1] * self.bright,
                       self.color[2] * self.bright)
    

class Firework:
    def __init__(self):
        self.x = random.randrange(15)
        self.end_y = 2 + random.randrange(5)
        self.y = 15
        self.color = self.random_color()
        self.burst = False
        self.particles = []
        self.n_particles = random.randrange(10, 25)
        self.particle_speed = 8 + random.random() * 7
        self.dim = 1
        self.rounds = random.randrange(2, 4)

    def random_color(self):
        x = 255
        colors = [
            (x, 0, 0),
            (x, x, 0),
            (0, x, 0),
            (0, x, x),
            (0, 0, x),
            (x, 0, x),
            (x, x, x),
        ]
        return colors[random.randrange(len(colors))]

    @property
    def done(self):
        return self.burst and len(self.particles) == 0
    
    def tick(self, ctrl, delta):
        if self.y > self.end_y:
            self.y -= delta * 18
            self.dim *= 0.991
        elif not self.burst:
            self.burst = True
            for r in range(self.rounds):
                for i in range(self.n_particles):
                    direction = i / self.n_particles * math.pi * 2
                    self.particles.append(
                        Particle(self.color,
                                 self.x, self.y,
                                 direction,
                                 self.particle_speed / (r+1)))
        else:
            for p in self.particles:
                p.tick(ctrl, delta)
            self.particles = [ p for p in self.particles if not p.done ]
            
        
    def render(self, ctrl):
        ctrl.fill(0, 0, 0)
        if not self.burst:
            ctrl.set_pixel(self.x, self.y,
                           self.color[0] * (1 - self.dim),
                           self.color[1] * (1 - self.dim),
                           self.color[2] * (1 - self.dim))
        
        for p in self.particles:
            p.render(ctrl)
        
        


class Fireworks:
    def __init__(self):
        self.elapsed = 0
        self.time = 25

        self.firework = Firework()

    @property
    def done(self):
        return not self.firework

    def tick(self, ctrl, delta):
        self.elapsed += delta

        if self.firework:
            self.firework.tick(ctrl, delta)

            if self.firework.done and self.elapsed < self.time:
                self.firework = Firework()
            elif self.firework.done:
                self.firework = None

    def render(self, ctrl):
        if self.firework:
            self.firework.render(ctrl)


from suggestions.models import NYSuggestion

class NYMessageBuilder(IltextBuilder):
    def  __init__(self):
        super().__init__()

        self.n = 0
    
    def get_suggestion(self):
        approved_suggestions = NYSuggestion.objects.filter(approved=True)

        return random.choice(approved_suggestions)

    def create_text(self):
        suggestion = self.get_suggestion()
        text = ("    '" + suggestion.suggestion_text + "' - " +
                suggestion.sender_name)

        if suggestion.sender_hallway:
            text += ", hall " + str(suggestion.sender_hallway)

        return text

    def create_object(self):
        if self.n == 0:
            self.n += 1
            return Fireworks()
        else:
            return super().create_object()

class ObjectsRenderer:

    def __init__(self, obj_builder):
        self.obj_builder = obj_builder
        self.cur_obj = self.obj_builder.create_object()

    def tick(self, ctrl, delta):
        self.cur_obj.tick(ctrl, delta)

        if self.cur_obj.done:
            self.cur_obj = self.obj_builder.create_object()

    def render(self, ctrl):
        self.cur_obj.render(ctrl)



class NYE:
    def seconds_to_ny(self):
        return (self.ny_date - datetime.now()).total_seconds()

    def __init__(self):
        self.ny_date = datetime(2022, 1, 1, 0, 0)
        #self.ny_date = datetime.now() + relativedelta(seconds=+6)

        countdown_builder = CountdownBuilder(self.ny_date)
        self.long_counter = ObjectsRenderer(countdown_builder)
        self.nye_messages = ObjectsRenderer(NYMessageBuilder())

    def tick(self, ctrl, delta):
        secs = math.floor(self.seconds_to_ny())

        if secs < 0:
            self.nye_messages.tick(ctrl, delta)
        elif secs < 60:
            pass
        else:
            self.long_counter.tick(ctrl, delta)

    def render(self, ctrl):
        raw_secs = self.seconds_to_ny()
        secs = math.floor(raw_secs)

        if secs < 0:
            self.nye_messages.render(ctrl)
        elif secs < 60:
            ctrl.fill(0, 0, 0)            
            render_center(ctrl, str(secs), time_to_color(raw_secs, secs))
        else:
            self.long_counter.render(ctrl)

from PIL import Image as image

from django.conf import settings

def load(char):
    return image.open(str(settings.BASE_DIR) +
                      '/iltext/bitfont/' +
                      str(ord(char)) +
                      ".pbm")

def time_to_color(raw_secs, secs):
    index = math.floor(secs) % 7
    prog = raw_secs - secs
    x = round(255 * prog)
    colors = [
        (x, 0, 0),
        (x, x, 0),
        (0, x, 0),
        (0, x, x),
        (0, 0, x),
        (x, 0, x),
        (x, x, x),
    ]
        

    return colors[index]

def render_center(ctrl, string, color=(255, 255, 255)):
    char_imgs = []
    width = 0
    for char in string:
        img = load(char)
        width = width + img.width

        char_imgs.append(img)
                

    width = width + len(char_imgs) - 1

    WIDTH = 15
    HEIGHT = 10

    pad_left = (15 - width) // 2
    offset = pad_left

    for i in range(len(char_imgs)):
        cur_img = char_imgs[i]
        cur_pix = cur_img.load()
        for x in range(cur_img.size[0]):
            for y in range(cur_img.size[1]):
                rx = x + offset
                ry = y

                if cur_pix[x, y] == 255:
                    ctrl.set_pixel(rx, ry, color[0], color[1], color[2])

        offset = offset + cur_img.size[0] + 1

    
