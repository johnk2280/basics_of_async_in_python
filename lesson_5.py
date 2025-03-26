from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR


def server() -> None:
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5001))
    server_sock.listen()

    while True:
        client_sock, addr = server_sock.accept()
        print(f'Connection from: {addr}')
        client(client_sock)


def client(client_sock: socket) -> None:
    while True:
        request = client_sock.recv(4096)

        if not request:
            break

        response = 'Hello world\n'.encode()
        client_sock.send(response)

    print('outside inner loop')
    client_sock.close()


if __name__ == '__main__':
    server()
