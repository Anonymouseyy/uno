import time
import pygame as pg
import socket, sys, pickle

pg.init()
size = width, height = 1120, 630
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
current_card = None
opponent_cards = None
player_number = None
turn = 0


def draw_hand(cards):
    global screen
    rect_list = []
    ratio = 1.59
    max_w = 100

    if width/len(cards) >= max_w:
        w = max_w
    else:
        w = width/len(cards)

    for i, card in enumerate(cards):
        if card[0] == "w":
            color = black
        elif card[0] == "r":
            color = red
        elif card[0] == "b":
            color = blue
        elif card[0] == "g":
            color = green
        elif card[0] == "y":
            color = yellow

        if color == black:
            if len(card) == 1:
                text = mediumFont.render('W', True, white)
            else: text = mediumFont.render(f'{card[1:].capitalize()}', True, white)
            x = pg.Rect(0, 0, w-5, w * ratio-5)
        else:
            text = mediumFont.render(f'{card[1:].capitalize()}', True, black)
            x = pg.Rect(0, 0, w, w * ratio)

        text_rect = text.get_rect()
        x.center = (i*w)+w//2+5, 550
        text_rect.center = x.center
        if color == black:
            y = pg.Rect(0, 0, w, w*ratio)
            y.center = x.center
            pg.draw.rect(screen, white, y)

        pg.draw.rect(screen, color, x)
        screen.blit(text, text_rect)

        rect_list.append(x)

    return rect_list


while True:
    clock.tick(60)
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            if client:
                client.send(pickle.dumps(DISCONNECT_MESSAGE))
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
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(ADDR)
                    hand, opponent_cards, current_card, player_number = pickle.loads(client.recv(2048))
                    print(hand, opponent_cards, current_card)
                except:
                    print('Connection Failed')
                    sys.exit()
                game_started = True
    if game_started:
        try:
            client.send(pickle.dumps('GETDATA'))
            hand, opponent_cards, current_card, turn = pickle.loads(client.recv(2048))
        except socket.error as e:
            print(e)

        card_rects = draw_hand(hand)

        if turn == player_number:
            click, _, _ = pg.mouse.get_pressed()
            if click == 1:
                mouse = pg.mouse.get_pos()
                for i in card_rects:
                    if i.collidepoint(mouse):
                        try:
                            client.send(pickle.dumps([hand, current_card]))
                            hand, opponent_cards, current_card, turn = pickle.loads(client.recv(2048))
                        except socket.error as e:
                            print(e)

    pg.display.flip()
