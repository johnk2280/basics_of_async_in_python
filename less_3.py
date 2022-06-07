import selectors
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR

selector = selectors.DefaultSelector()


def server() -> None:
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5001))
    server_sock.listen()

    selector.register(
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection,
    )


def accept_connection(sock: socket) -> None:
    client_sock, addr = sock.accept()
    print(f'Connection from: {addr}')

    selector.register(
        fileobj=client_sock,
        events=selectors.EVENT_READ,
        data=send_message,
    )


def send_message(client_sock: socket) -> None:
    request = client_sock.recv(1024)
    print(f'received a request: {request.decode()} from: {client_sock}')
    if request:
        response = 'Hello from johnk_server\n'.encode()
        client_sock.send(response)
    else:
        selector.unregister(client_sock)
        client_sock.close()


def event_loop() -> None:
    while True:
        events = selector.select()  # return: [(key: namedtuple, events)]
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)
            # [(SelectorKey(fileobj=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 5001)>, fd=5, events=1, data=<function accept_connection at 0x7f7c1c0c0c10>), 1)]


if __name__ == '__main__':
    server()
    event_loop()
