from renderer import Renderer
import pygame
from keyboard import Keyboard
from speaker import Speaker
from cpu import CPU

k = Keyboard()
t = Renderer(20)
s = Speaker()
c = CPU(t, k, s)

def main():
    t.initDisplay()
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                k.onKeyDown(str(event.key))
            elif event.type == pygame.KEYUP:
                k.onKeyUp(str(event.key))
        clock.tick(60)
        t.render()
        c.loadSpritesIntoMemory
        c.loadRom('stars.ch8')
        c.cycle

if __name__ == "__main__":
    main()

