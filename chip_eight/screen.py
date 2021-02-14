from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

class Screen():
    def __init__(self, columns=64, rows=32, screen_width=640, screen_height=320):
        self.rows = rows
        self.columns = columns
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pixel_scale_x = self.screen_width / self.columns
        self.pixel_scale_y = self.screen_height / self.rows
        self.pixels = [[False for y in range(0,rows)] for x in range(0,columns)]
        self.color_on = (0xFF,0xFF,0xFF)
        self.color_off = (0x00,0x00,0x00)

    def initialize(self):
        self.__screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.flip()

    def draw_sprite(self, x, y, sprite):
        flipped_pixel = False
        rectangles = []
        for b_y, byte in enumerate(sprite):
            #convert byte into a big endian list of 1s and 0s
            bits = [(byte & 2**i)>>i for i in range(7,-1,-1)]
            for b_x, val in enumerate(bits):
                pixel_x = (x + b_x) % self.columns 
                pixel_y = (y + b_y) % self.rows
                if val == 1:
                    if self.pixels[pixel_x][pixel_y] == True:
                        self.pixels[pixel_x][pixel_y] = False
                        rect = pygame.draw.rect(self.__screen, self.color_off, pygame.Rect(pixel_x * self.pixel_scale_x, pixel_y * self.pixel_scale_y, self.pixel_scale_x, self.pixel_scale_y))
                        rectangles.append(rect)
                        flipped_pixel = True
                    else:
                        self.pixels[pixel_x][pixel_y] = True
                        rect = pygame.draw.rect(self.__screen, self.color_on, pygame.Rect(pixel_x * self.pixel_scale_x, pixel_y * self.pixel_scale_y, self.pixel_scale_x, self.pixel_scale_y))
                        rectangles.append(rect)
        pygame.display.update(rectangles)
        return flipped_pixel
    
    def clear_screen(self):
        for x,column in enumerate(self.pixels):
            for y,pixel in enumerate(column):
                self.pixels[x][y] = False
        self.__screen.fill(self.color_off)