import math

def helper(t, main, tmod, p):
    inter = math.sin(main + t / 20.0 * tmod)
    return math.pow(inter, p)

class Waves:
    def __init__(self):
        self.t = 0.0

    def tick(self, ctrl, delta):
        self.t = self.t + 1.6

    def render(self, ctrl):
        for x in range(ctrl.WIDTH):
            for y in range(ctrl.HEIGHT):
                brightness = 1.0
                r = helper(self.t, (x + y * 1.2) / 2.0, 1.0, 2) * 255.0 * brightness; 
                g = helper(self.t, (x + y * 0.7) / 1.8, 1.2, 2) * 100.0 * brightness; 
                b = helper(self.t, y / 20.0 - x / 50.0, 0.15, 32) * 100.0 * brightness;
    
                ctrl.set_pixel(x, y, round(r), round(g), round(b))
    
        ctrl.render()
    
        
