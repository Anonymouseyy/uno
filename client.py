import pygame as pg
import socket, sys

pg.init()
size = width, height = 1000, 600

# Colors
white = (255, 255, 255)
gray = (138, 135, 128)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

screen = pg.display.set_mode(size)
pg.display.set_caption('Uno')

# Fonts
smallFont = pg.font.Font('Roboto-Black.ttf', 14)
mediumFont = pg.font.Font('Roboto-Black.ttf', 28)
largeFont = pg.font.Font('Roboto-Black.ttf', 40)


while True:
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill(black)