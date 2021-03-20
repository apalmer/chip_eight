import pygame

class Keyboard():
    def __init__(self):
        pass
    
    def wait_for_key(self):
        key_pressed = False
        while not key_pressed:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN: 
                keys_pressed = pygame.key.get_pressed()
                key_pressed = True
        return keys_pressed
    