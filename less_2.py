import asyncio
from select import select
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from socket import socket

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
#     client_sock, addr = sock.accept()
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


async def bar():
    asyncio.sleep(1)


def func():
    return await bar()


a = {
    'b': 1,
    'c': 2,
}
c = [1, 2, 3]


class A:
    def __init__(
        self,
        a: int,
        *,
        b: str,
        c: bool,
    ):
        self.a = a
        self.b = b
        self.c = c

    def foo(self, v: list = []):
        for l in range(3):
            print('ok')
        return v


ai = A(a=1, b='2', c=True)

if __name__ == '__main__':
    to_monitor.append(server_sock)
    password = 'asdf'

    try:
        a = 1 / 0
    except Exception:
        a = 0

    try:
        a = 1 / 0
    except:
        pass

    event_loop()
