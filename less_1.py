from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5001))
server_sock.listen()

while True:
    print('Before .accept() ')
    client_sock, addr = server_sock.accept()
    print(f'Connection from: {addr}')

    while True:
        request = client_sock.recv(1024)

        if not request:
            break

        response = 'Hello from johnk_server\n'.encode()
        client_sock.send(response)

    print('Outside inner while loop')
    client_sock.close()
