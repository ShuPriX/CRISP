from http import server
import socket
import threading
import sqlite3
import signal
import sys
import time
import subprocess

intercept_enabled = False

def setup_database():
    database = sqlite3.connect('Captured_requests.db')
    cursor = database.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS all_requests (Request_Number FLOAT, Request TEXT, Response TEXT)')
    database.close()

def edit_request(data):
    with open('intercepted_request.txt', 'w') as file:
        file.write(data)
    subprocess.run(['notepad.exe', 'intercepted_request.txt'])
    with open('intercepted_request.txt', 'r') as file:
        return file.read()

def handle_client_request(client_socket):
    global intercept_enabled
    database = sqlite3.connect('Captured_requests.db')
    cursor = database.cursor()
    
    request_data = b''
    client_socket.setblocking(False)
    while True:
        try:
            data = client_socket.recv(2048)
            if not data:
                break
            request_data += data
        except:
            break
    
    request_str = request_data.decode(errors='ignore')
    
    if intercept_enabled:
        print("Intercepted request, waiting for modification...")
        request_str = edit_request(request_str)
    
    host, port = extract_host_port_from_request(request_data)
    
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((host, port))
    destination_socket.sendall(request_str.encode())
    
    response_data = b''
    destination_socket.settimeout(10.0)
    while True:
        try:
            data = destination_socket.recv(2048)
            if len(data) > 0:
                response_data += data
                client_socket.sendall(data)
            else:
                break
        except:
            break
    
    cursor.execute('INSERT INTO all_requests VALUES (?, ?, ?)', (time.time(), request_str, response_data.decode(errors='ignore')))
    database.commit()
    cursor.close()
    database.close()
    
    destination_socket.close()
    client_socket.close()

def extract_host_port_from_request(request):
    try:
        headers = request.split(b'\r\n')
        for header in headers:
            if header.startswith(b'Host: '):
                host = header.split(b' ')[1].decode()
                if ':' in host:
                    return host.split(':')[0], int(host.split(':')[1])
                return host, 80
    except:
        pass
    return 'localhost', 80

def start_proxy_server():
    signal.signal(signal.SIGINT, shutdown_server)
    setup_database()
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(20)
    print(f"Proxy server listening on port {port}...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()

def shutdown_server(signal, frame):
    print('Shutting down server...')
    server.close()
    sys.exit(0)

if __name__ == "__main__":
    start_proxy_server()
