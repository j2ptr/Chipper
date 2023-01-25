import sys
import pygame
import numpy

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

                





c = CPU(1, 2, 3)
c.loadSpritesIntoMemory()
c.loadRom('Stars.ch8')

print(c.memory)