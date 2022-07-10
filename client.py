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
PORT = 3389
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '35.235.71.200'
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

    if len(cards) == 0:
        w = max_w
    else:
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
        x.center = (i*(w+5))+w//2+5, 550
        text_rect.center = x.center
        if color == black:
            y = pg.Rect(0, 0, w, w*ratio)
            y.center = x.center
            pg.draw.rect(screen, white, y)

        pg.draw.rect(screen, color, x)
        screen.blit(text, text_rect)

        rect_list.append(x)

    return rect_list


def draw_current_card(card):
    global screen

    if card[0] == "r" or card[:2] == "wr":
        color = red
    elif card[0] == "b" or card[:2] == "wb":
        color = blue
    elif card[0] == "g" or card[:2] == "wg":
        color = green
    elif card[0] == "y" or card[:2] == "wy":
        color = yellow

    if card[0] == 'w':
        if len(card) == 2:
            text = mediumFont.render('W', True, white)
        else:
            text = mediumFont.render(f'W4', True, white)
        x = pg.Rect(0, 0, 145, 233.5)
    else:
        text = mediumFont.render(f'{card[1:].capitalize()}', True, black)
        x = pg.Rect(0, 0, 150, 238.5)

    text_rect = text.get_rect()
    x.center = width//2, height//2
    text_rect.center = x.center
    if color == black:
        y = pg.Rect(0, 0, 150, 238.5)
        y.center = x.center
        pg.draw.rect(screen, white, y)

    pg.draw.rect(screen, color, x)
    screen.blit(text, text_rect)


def draw_opponent_hand(hand):
    global screen
    ratio = 1.59
    max_w = 100

    if hand == 0:
        w = max_w
    else:
        if width/hand >= max_w:
            w = max_w
        else:
            w = width/hand

    for i in range(hand):
        x = pg.Rect(0, 0, w-5, w*ratio-5)
        text = mediumFont.render('UNO', True, white)

        text_rect = text.get_rect()
        x.center = width-((i * (w + 5)) + w // 2 + 5), 80
        text_rect.center = x.center

        y = pg.Rect(0, 0, w, w*ratio)
        y.center = x.center

        pg.draw.rect(screen, white, y)
        pg.draw.rect(screen, black, x)
        screen.blit(text, text_rect)


def is_valid_move(card, current_card):
    if card[0] == 'w':
        return True
    elif card[0] == current_card[0]:
        return True
    elif current_card[0] == 'w':
        if card[0] == current_card[1]:
            return True
    elif card[1:] == current_card[1:]:
        return True

    return False


def choose_color(d4=False):
    picking = True
    while picking:
        global screen
        clock.tick(60)
        el = pg.event.get()
        for e in el:
            if e.type == pg.QUIT:
                if client:
                    client.send(pickle.dumps(DISCONNECT_MESSAGE))
                sys.exit()

        back_rect = pg.Rect(0, 0, width//3, height//3)
        back_rect.center = width//2, height//2
        pg.draw.rect(screen, white, back_rect)

        rect_list = []
        color_list = ['Red', 'Green', 'Blue', 'Yellow']
        for count, i in enumerate(color_list):
            color_button = pg.Rect(0, 0, (width//3)//4-10, height//3-10)
            color_button.left = back_rect.left+5+(((width//3)//4)*count)
            color_button.centery = height//2
            if i == 'Yellow':
                color = smallFont.render(i, True, black)
            else: color = smallFont.render(i, True, white)
            color_rect = color.get_rect()
            color_rect.center = color_button.center
            pg.draw.rect(screen, i, color_button)
            screen.blit(color, color_rect)
            rect_list.append(color_button)

        e, _, _ = pg.mouse.get_pressed()
        if e == 1:
            mous = pg.mouse.get_pos()
            for c, x in enumerate(rect_list):
                if x.collidepoint(mous):
                    if color_list[c] == 'Red':
                        if d4: return 'wr4'
                        return 'wr'
                    if color_list[c] == 'Blue':
                        if d4: return 'wb4'
                        return 'wb'
                    if color_list[c] == 'Yellow':
                        if d4: return 'wy4'
                        return 'wy'
                    if color_list[c] == 'Green':
                        if d4: return 'wg4'
                        return 'wg'

        pg.display.flip()


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
                    h, opponent_cards, current_card, player_number = pickle.loads(client.recv(2048))
                except:
                    print('Connection Failed')
                    sys.exit()
                game_started = True
    if game_started:
        try:
            client.send(pickle.dumps('GETDATA'))
            h, opponent_cards, current_card, turn = pickle.loads(client.recv(2048))
        except socket.error as e:
            print(e)

        card_rects = draw_hand(h)
        draw_current_card(current_card)
        draw_opponent_hand(opponent_cards)

        turn_box = pg.Rect(0, 0, width / 5, height // 4)
        if turn == player_number:
            turnt = mediumFont.render('Your Turn', True, black)
        else:
            turnt = mediumFont.render('Opponent Turn', True, black)
        turn_rect = turnt.get_rect()
        turn_box.center = width // 5, height//2
        turn_rect.center = turn_box.center
        pg.draw.rect(screen, white, turn_box)
        screen.blit(turnt, turn_rect)

        if opponent_cards == 0:
            loss_box = pg.Rect(0, 0, width / 2, height // 2)
            loss = largeFont.render('YOU LOST', True, black)
            loss_rect = loss.get_rect()
            loss_box.center = width//2, height//2
            loss_rect.center = loss_box.center
            pg.draw.rect(screen, white, loss_box)
            screen.blit(loss, loss_rect)
        elif len(h) == 0:
            win_box = pg.Rect(0, 0, width / 2, height // 2)
            win = largeFont.render('YOU WON', True, black)
            win_rect = win.get_rect()
            win_box.center = width//2, height//2
            win_rect.center = win_box.center
            pg.draw.rect(screen, white, win_box)
            screen.blit(win, win_rect)

        if turn == player_number:
            draw_box = pg.Rect(0, 0, width / 5, height // 4)
            draw = mediumFont.render('Draw Card', True, black)
            draw_rect = draw.get_rect()
            draw_box.center = width-(width // 5), height//2
            draw_rect.center = draw_box.center
            pg.draw.rect(screen, white, draw_box)
            screen.blit(draw, draw_rect)

            click, _, _ = pg.mouse.get_pressed()
            if click == 1:
                mouse = pg.mouse.get_pos()
                for count, i in enumerate(card_rects):
                    if i.collidepoint(mouse):
                        try:
                            if not is_valid_move(h[count], current_card):
                                continue

                            if h[count][0] == 'w':
                                if len(h[count]) == 2:
                                    current_card = choose_color(True)
                                else:
                                    current_card = choose_color()
                            else:
                                current_card = h[count]
                            h.remove(h[count])
                            client.send(pickle.dumps([h, current_card]))
                            h, opponent_cards, current_card, turn = pickle.loads(client.recv(2048))
                            time.sleep(0.2)
                        except socket.error as e:
                            print(e)

                if draw_box.collidepoint(mouse):
                    try:
                        client.send(pickle.dumps([h, current_card]))
                        h, opponent_cards, current_card, turn = pickle.loads(client.recv(2048))
                    except socket.error as e:
                        print(e)

    pg.display.flip()
