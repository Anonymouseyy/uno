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

# Socket Variables
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.0.16'
ADDR = (SERVER, PORT)


def send_str(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while True:
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            sys.exit()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    screen.fill(black)