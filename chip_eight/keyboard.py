import pygame
from bidict import bidict

class Keyboard():
    def __init__(self):
        self.keyMap = bidict({
            49 : 0x1,
            50 : 0x2,
            51 : 0x3,
            52 : 0xc,
            113 : 0x4,
            119 : 0x5,
            101 : 0x6,
            114 : 0xd,
            97 : 0x7,
            115 : 0x8,
            100 : 0x9,
            102 : 0xe,
            122 : 0xa,
            120 : 0x0,
            99 : 0xb,
            118 : 0xf
        })
    
    def wait_for_key(self):
        key_pressed = False
        while not key_pressed:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN: 
                raw_pressed = pygame.key.get_pressed()
                key_pressed = True

        for key in self.keyMap:
            if(raw_pressed[key]):
                pressed = self.keyMap[key]
                continue

        return pressed
    
    def is_pressed(self, key):
        raw_pressed = pygame.key.get_pressed()
        real_key = self.keyMap.inverse[key]
        return raw_pressed[real_key]
    