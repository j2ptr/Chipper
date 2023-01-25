from renderer import Renderer
import pygame
from keyboard import Keyboard
from speaker import Speaker

k = Keyboard()
t = Renderer(20)
s = Speaker()
t.initDisplay()
pygame.init()


t.testRender()
#    t.render()

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
