import pygame

class Keyboard:
    def __init__(self):
        self.KEYMAP = {
            '49' : 0x1,
            '50' : 0x2,
            '51' : 0x3,
            '52' : 0xC,
            '113' : 0x4,
            '119' : 0x5,
            '101' : 0x6,
            '114' : 0xD,
            '97' : 0x7,
            '115' : 0x8,
            '100' : 0x9,
            '102' : 0xE,
            '122' : 0xA,
            '120' : 0x0,
            '99' : 0xB,
            '118' : 0xF
        }
        self.keysPressed = []
        self.onNextKeyPress = None

    def isKeyPressed(self, keyCode):
        return True if keyCode in self.keysPressed else False

    def onKeyDown(self, key):
        self.keysPressed.append(self.KEYMAP[key])

        if self.onNextKeyPress != None or key:
            self.onNextKeyPress = key
            self.onNextKeyPress = None

    def onKeyUp(self, key):
        self.keysPressed.remove(self.KEYMAP[key])

