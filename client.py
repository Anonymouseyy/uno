import time
import pygame as pg
import socket, sys, random

pg.init()
size = width, height = 700, 600
clock = pg.time.Clock()
text_clock = pg.time.Clock()

# Colors
white = (255, 255, 255)
gray = (138, 135, 128)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
uno_card_colors = [red, green, yellow, blue]

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
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

game_started = False
client = None
i = 0


def send_str(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while True:
    clock.tick(60)
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill(black)

    if not game_started:
        # Display title
        title = largeFont.render('Play Uno', True, white)
        title_rect = title.get_rect()
        title_rect.center = ((width / 2), 50)
        screen.blit(title, title_rect)

        # Display start button
        play_button = pg.Rect((width / 2 - width / 4), (height / 2-150), width / 2, 300)
        play = mediumFont.render('Join Room', True, black)
        play_rect = play.get_rect()
        play_rect.center = play_button.center
        pg.draw.rect(screen, white, play_button)
        screen.blit(play, play_rect)

        # Check if button is clicked
        click, _, _ = pg.mouse.get_pressed()
        if click == 1:
            mouse = pg.mouse.get_pos()
            if play_button.collidepoint(mouse):
                time.sleep(0.2)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR)
                game_started = True

    pg.display.flip()
