import pygame

class Speaker:
    def __init__(self):
        pygame.mixer.music.load('440.wav')

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()