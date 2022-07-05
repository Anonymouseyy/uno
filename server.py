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
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
        current_player += 1

        if threading.activeCount() - 1 == 2:
            game_start = True

    print(f'[Stopped Listening] Server has stopped listening on {SERVER}')


print('[STARTING] server is starting...')
start()