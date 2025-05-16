from select import select
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5001))
server_sock.listen()

to_monitor: list[socket] = []


def accept_connection(sock: socket) -> None:
    client_sock, addr = sock.accept()
    print(f'Connection from: {addr}')
    to_monitor.append(client_sock)


# def accept_connection(sock: socket) -> None:
#     client_sock, addr =                                                  sock.accept()
#     print(f'Connection from: {addr}')
#     to_monitor.append(client_sock)


def send_message(client_sock: socket) -> None:
    request = client_sock.recv(1024)
    print(f'received a request: {request.decode()} from: {client_sock}')
    if request:
        response = 'Hello from johnk_server\n'.encode()
        client_sock.send(response)
    else:
        client_sock.close()


def event_loop() -> None:
    while True:
        socks_to_read, _, _ = select(to_monitor, [], [])
        for sock in socks_to_read:
            if sock is server_sock:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_sock)
    event_loop()
