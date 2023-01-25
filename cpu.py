import sys
import pygame
import numpy
import math
import random

numpy.set_printoptions(threshold=sys.maxsize)

class CPU:
    def __init__(self, renderer, keyboard, speaker):
        self.renderer = renderer
        self.keyboard = keyboard
        self.speaker = speaker

        self.memory = numpy.zeros(4096, numpy.uint8)
        self.v = numpy.zeros(16, numpy.uint8)
        self.i = 0

        self.delayTimer = 0
        self.soundTimer = 0

        self.pc = 0x200
        self.stack = []
        self.paused = False
        self.speed = 10

    def loadSpritesIntoMemory(self):
        i = 0x0
        s = numpy.uint8

        sprites = numpy.array([
            0xF0, 0x90, 0x90, 0x90, 0xF0,
            0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0,
            0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10,
            0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0,
            0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0,
            0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0,
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0,
            0xF0, 0x80, 0xF0, 0x80, 0x80 
        ], numpy.uint8)

        while i < len(sprites):
            for s in sprites:
                self.memory[i] = s
                i += 1

    def loadProgramIntoMemory(self, program):
        loc = 0
        while loc < (len(program)):
            for n in program:
                self.memory[0x200 + loc] = n
                loc += 1

    def loadRom(self, filename):
        romdata = open(filename, 'rb').read()
        self.loadProgramIntoMemory(romdata)

    def cycle(self):
        i = 0
        while i < self.speed:
            i += 1
            if (self.paused != True):
                opcode = (self.memory[self.pc]) << 8 | self.memory[self.pc + 1]

        if self.paused != True:
            self.updateTimers()

        self.playSound()
        self.renderer.render()

    def updateTimers(self):
        if self.delayTimer > 0:
            self.delayTimer -= 1
        
        if self.soundTimer > 0:
            self.soundTimer -= 1

    def playSound(self):
        if self.soundTimer > 0:
            self.speaker.play()
        else:
            self.speaker.stop()

    def executeInstruction(self, opcode):
        self.pc += 2
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x0F00) >> 4

        instruction = opcode & 0xF000

        if instruction == 0x0000:
            pass

            if opcode == 0x00E0:
                self.renderer.clear()

            elif opcode == 0x00EE:
                self.pc = self.stack.pop()

        elif instruction == 0x1000:
            self.pc = (opcode & 0xFFF)

        elif instruction == 0x2000:
            self.stack.append(self.pc)
            self.pc = (opcode & 0xFFF)

        elif instruction == 0x3000:
            if (self.v[x] == (opcode & 0xFF)):
                self.pc += 2

        elif instruction == 0x4000:
            if (self.v[x] != (opcode & 0xFF)):
                self.pc += 2

        elif instruction == 0x5000:
            if (self.v[x] == self.v[y]):
                self.pc += 2

        elif instruction == 0x6000:
            self.v[x] = (opcode & 0xFF)

        elif instruction == 0x7000:
            self.v[x] += (opcode & 0xFF)

        elif instruction == 0x8000:
            if (opcode & 0xF) == 0x0:
                self.v[x] = self.v[y]

            elif (opcode & 0xF) == 0x1:
                self.v[x] |= self.v[y]

            elif (opcode & 0xF) == 0x2:
                self.v[x] &= self.v[y]

            elif (opcode & 0xF) == 0x3:
                self.v[x] ^= self.v[y]

            elif (opcode & 0xF) == 0x4:
                sum = (self.v[x] + self.v[y])
                self.v[0xF] = 0 
                if (sum > 0xFF):
                    self.v[0xF] = 1
                self.v[x] = sum

            elif (opcode & 0xF) == 0x5:
                self.v[0xF] = 0
                if self.v[x] > self.v[y]:
                    self.v[0xF] = 1
                self.v[x] -= self.v[y]

            elif (opcode & 0xF) == 0x6:
                self.v[0xF] = (self.v[x] & 0x1)
                self.v[x] >>= 1

            elif (opcode & 0xF) == 0x7:
                self.v[0xF] = 0
                if self.v[y] > self.v[x]:
                    self.v[0xF] = 1
                self.v[x] = self.v[y] - self.v[x]

            elif (opcode & 0xF) == 0xE:
                self.v[0xF] = (self.v[x] & 0x80)
                self.v[x] <<= 1

        elif instruction == 0x9000:
            if (self.v[x] != self.v[y]):
                self.pc += 2

        elif instruction == 0xA000:
            self.i = (opcode & 0xFFF)

        elif instruction == 0xB000:
            self.pc = (opcode & 0xFFF) + self.v[0]

        elif instruction == 0xC000:
            rand = math.floor(random.randrange(0, 0xFF))
            self.v[x] = rand & (opcode & 0xFF)

        elif instruction == 0xD000:
            width = 8
            height = (opcode & 0xF)
            row = 0
            col = 0
            self.v[0xF] = 0
            while row < height:
                sprite = self.memory[self.i + row]
                row += 1
                while col < width:
                    if ((sprite & 0x80) > 0):
                        if (self.renderer.setPixel(self.v[x] + col, self.v[y] + row)):
                            self.v[0xF] = 1
                    col += 1
                    sprite <<= 1

        elif instruction == 0xE000:
            if (opcode & 0xFF) == 0x9E:
                if self.keyboard.isKeyPressed(self.v[x]):
                    self.pc += 2

            elif (opcode & 0xFF) == 0xA1:
                if not (self.keyboard.isKeyPressed(self.v[x])):
                    self.pc += 2

        elif instruction == 0xF000:
            if (opcode & 0xFF) == 0x07:
                self.v[x] = self.delayTimer

            elif (opcode & 0xFF) == 0x0A:
                while self.keyboard.onNextKeyPressed == None:
                    self.paused = True
                if self.keyboard.onNextKeyPressed != None:
                    self.v[x] = self.keyboard.onNextKeyPressed
                    self.paused = False

            elif (opcode & 0xFF) == 0x15:
                self.delayTimer = self.v[x]

            elif (opcode & 0xFF) == 0x18:
                self.soundTimer = self.v[x]

            elif (opcode & 0xFF) == 0x1E:
                self.i += self.v[x]

            elif (opcode & 0xFF) == 0x29:
                self.i = self.v[x] * 5

            elif (opcode & 0xFF) == 0x33:
                self.memory[self.i] = int(self.v[x] / 100)
                self.memory[self.i + 1] = int((self.v[x] % 100) / 10)
                self.memory[self.i + 2] = int(self.v[x] % 10)

            elif (opcode & 0xFF) == 0x55:
                registerIndex = 0
                while registerIndex <= x:
                    self.memory[self.i + registerIndex] = self.v[registerIndex]
                    registerIndex += 1

            elif (opcode & 0xFF) == 0x65:
                registerIndex = 0
                while registerIndex <= x:
                    self.v[registerIndex] = self.memory[self.i + registerIndex]
                    registerIndex += 1

