import socket, threading, random, pickle

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
max_players = 2
starting_cards = 7

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
current_card = random.choice(uno_deck)
uno_deck.remove(current_card)

for i in range(max_players):
    x = []
    for j in range(starting_cards):
        x.append(random.choice(uno_deck))
        uno_deck.remove(x[j])
    hands.append(x)


def handle_client(conn, addr, player):
    global current_card, hands
    print(f'[NEW CONNECTION] {addr} connected.')
    conn.send(pickle.dumps([hands[player], len(hands[player-1]), current_card]))
    connected = True
    while connected:
        try:
            data = pickle.loads(conn.recv(2048))
            if data == DISCONNECT_MESSAGE:
                break
            hands[player], current_card = data

            if not data:
                print("Disconnected")
                break
            else:
                reply = [hands[player], len(hands[player-1]), current_card]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print(f'[CONNECTION LOST] Connection has been lost or terminated with {addr}')
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

        if x == max_players:
            game_start = True

    print(f'[STOPPED LISTENING] Server has stopped listening on {SERVER}')


print('[STARTING] server is starting...')
start()