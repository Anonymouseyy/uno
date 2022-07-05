import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

game_start = False
current_player = 0

# Generate Uno Deck
colors = ['r', 'g', 'b', 'y']
actions = ['s', 'r', 'd2']
uno_deck = ['w', 'w', 'w', 'w', 'w4', 'w4', 'w4', 'w4']
for color in colors:
    for i in range(10):
        if i == 0:
            uno_deck.append(f'{color}0')
        else:
            uno_deck.append(f'{color}{i}')
            uno_deck.append(f'{color}{i}')

    for j in actions:
        uno_deck.append(f'{color}{j}')
        uno_deck.append(f'{color}{j}')
hands = []
current_card = None


def handle_client(conn, addr, player):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'[{addr}] {msg}')
            conn.send('Msg received'.encode(FORMAT))

    conn.close()


def start():
    global game_start, current_player
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while not game_start:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, current_player))
        thread.start()
        x = threading.activeCount() - 1
        print(f'[ACTIVE CONNECTIONS] {x}')
        current_player += 1

        if x == 2:
            game_start = True

    print(f'[Stopped Listening] Server has stopped listening on {SERVER}')


print('[STARTING] server is starting...')
start()