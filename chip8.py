from renderer import Renderer
import pygame
from keyboard import Keyboard
from speaker import Speaker
from cpu import CPU

pygame.init()
k = Keyboard()
t = Renderer(20)
t.initDisplay()
s = Speaker()
c = CPU(t, k, s)
clock = pygame.time.Clock()
c.loadSpritesIntoMemory
c.loadRom('pong.ch8')

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                k.onKeyDown(str(event.key))
            elif event.type == pygame.KEYUP:
                k.onKeyUp(str(event.key))
        clock.tick(60)
        #print(c.memory)
        #print(c.pc)
        #print(c.v)
        c.cycle()

if __name__ == "__main__":
    main()

