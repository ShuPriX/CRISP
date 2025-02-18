import socket
import threading
import sys
import signal
import sqlite3
from http import server

intercepted_requests = []

def handle_client_request(client_socket):
    request = client_socket.recv(1024)
    print(f"Received request: {request.decode('utf-8')}")
    
    # Parse the HTTP request
    request_lines = request.decode('utf-8').split('\r\n')
    if len(request_lines) > 0:
        first_line = request_lines[0].split(' ')
        if len(first_line) >= 3:
            method, path, version = first_line
            if method == 'GET':
                # Handle GET request
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from the proxy server!"
                client_socket.send(response.encode('utf-8'))
            else:
                # Handle other methods
                response = f"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nMethod {method} not allowed."
                client_socket.send(response.encode('utf-8'))
            
            # Store the request in the database
            store_request_in_db(method, path, version, request.decode('utf-8'))
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request."
            client_socket.send(response.encode('utf-8'))
    client_socket.close()

def store_request_in_db(method, path, version, request):
    try:
        # Connect to the SQLite database
        database = sqlite3.connect('./Captured_requests.db')
        cursor = database.cursor()
        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS all_requests (
                            Request_Number INTEGER PRIMARY KEY AUTOINCREMENT,
                            Method TEXT,
                            Path TEXT,
                            Version TEXT,
                            Request TEXT)''')
        # Insert the request into the table
        cursor.execute('INSERT INTO all_requests (Method, Path, Version, Request) VALUES (?, ?, ?, ?)',
                       (method, path, version, request))
        # Commit the transaction and close the database connection
        database.commit()
        database.close()
    except Exception as e:
        print(f"Error storing request in database: {e}")

def intercept_request(request_id, modified_request):
    try:
        # Connect to the SQLite database
        database = sqlite3.connect('./Captured_requests.db')
        cursor = database.cursor()
        # Update the request in the table
        cursor.execute('UPDATE all_requests SET Request = ? WHERE Request_Number = ?', (modified_request, request_id))
        # Commit the transaction and close the database connection
        database.commit()
        database.close()
    except Exception as e:
        print(f"Error intercepting request in database: {e}")

def start_proxy_server(port=8888):
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
    signal.signal(signal.SIGINT, shutdown_server)
    start_proxy_server()
