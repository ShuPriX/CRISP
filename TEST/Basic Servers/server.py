# python3
## Proper Socket that receives data and sends a response. In a class, object form.

import socket
import threading

class socket_server:
    isblocked = False
    isInterceptor = False

    def __init__(self, host, port, BUFFER_SIZE = 1024):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.BUFFER_SIZE = BUFFER_SIZE

    def client_handler(self, client_sock, client_addr):
        client_sock.setblocking(0)
        request = b''
        while True:
            try:
                data = client_sock.recv(self.BUFFER_SIZE)
                if data:
                    request += data
                else:
                    break
            except BlockingIOError:
                # No data available right now, continue the loop
                break
            except socket.error as e:
                print('Socket error:', e)
                break
            print('--------------------------------------------------------------')
            print(request.decode())
            print('--------------------------------------------------------------')
            client_sock.sendall(b'HTTP/1.0 200 OK\n\nHello World')
        client_sock.close()

    def start(self):
        while True:
            client_sock, client_addr = self.sock.accept()
            print('New connection from', client_addr)
            if self.isblocked:
                print('Blocking new connection from', client_addr)
                client_sock.close()
                continue
                
            threading.Thread(target=self.client_handler, args=(client_sock, client_addr)).start()

if __name__ == '__main__':
    web = socket_server('0.0.0.0', 8080)
    threading.Thread(target=web.start).start()
    web2 = socket_server('0.0.0.0', 8081)
    web2.isblocked = True
    threading.Thread(target=web2.start).start()


