# Proper Socket that receives data and sends a response. In a function form.

import socket

PORT = 8080
BUFFER_SIZE = 1024
HOST = '127.0.0.1' #localhost
# HOST = '0.0.0.0' #

custom_socket = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(custom_socket)
server_socket.bind(('127.0.0.1', 8080))

server_socket.listen(2)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established!")
    client_socket.setblocking(0)
    requsts = b''

    # JUST FOR RECEIVING DATA
    while True:
        try:
            print("Receiving data...")
            data = client_socket.recv(BUFFER_SIZE)
            print(f"Received data..")
            requsts += data
        except BlockingIOError:
            break
        except socket.error as e:
            exit(f"Error: {e}")
    
    print('--------------------------------------------------')
    print(requsts.decode())
    print('--------------------------------------------------')
    client_socket.sendall(b'HTTP/1.1 200 OK\n\nHELLO WORLD\n')
    client_socket.close()