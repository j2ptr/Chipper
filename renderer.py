from pygame import display, HWSURFACE, DOUBLEBUF, Color, draw
import math

SCREEN_DEPTH = 8

PIXEL_COLORS = {
    0: Color(0, 0, 0, 255),
    1: Color(255, 255, 255, 255)
}

class Renderer:
    def __init__(self, scale):
        self.cols = 32
        self.rows = 64
        self.scale = scale
        self.displayArr = [0] * (self.cols * self.rows)
        self.surface = None

    def initDisplay(self):
        display.init()
        self.surface = display.set_mode(
            ((self.rows * self.scale),
            (self.cols * self.scale)),
            HWSURFACE | DOUBLEBUF,
            SCREEN_DEPTH)
        display.set_caption('CHIP-8')
        self.clear()
        display.flip
        
    def setPixel(self, x, y):
        if (x > self.cols):
            x -= self.cols
        elif (x < 0):
            x += self.cols
        
        if (y > self.rows):
            y -= self.rows
        elif (y < 0):
            y += self.rows

        pixelLoc = x + (y * self.cols)

        self.displayArr[pixelLoc] ^= 1

        return ~self.displayArr[pixelLoc]

    def clear(self):
        self.displayArr = [0] * (self.cols * self.rows)

    def render(self):
        i = 0
        ip = 0

        for i in range(len(self.displayArr)):
            xBase = (i % self.cols) * self.scale
            yBase = math.floor(i / self.cols) * self.scale
            if (self.displayArr[i] == 1):
                c = PIXEL_COLORS[1]
            else:
                c = PIXEL_COLORS[0]
            draw.rect(self.surface, c, (xBase, yBase, self.scale, self.scale))
        display.flip()

    def testRender(self):
        self.setPixel(5, 2)

