import math

def gc(x, gamma=2.4):
    return round(math.pow(float(x) / 255.0, gamma) * 255.0);


class Ilimg:
    def __init__(self, pixels):
        self.pixels = pixels
        self.rendered = False

    def tick(self, ctrl, delta):
        pass

    def render(self, ctrl):
        if not self.rendered:
            for i in range(ctrl.WIDTH):
                for j in range(ctrl.HEIGHT):
                    try:
                        pix = self.pixels[i, j]
                        ctrl.set_pixel(i, j,
                                       gc(pix[0], 2.0),
                                       gc(pix[1], 2.8),
                                       gc(pix[2], 2.8))
                    except:
                        pass

            self.rendered = True
