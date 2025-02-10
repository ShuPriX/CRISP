from asyncio import Server
from curses import reset_prog_mode
import socket
import threading
import sqlite3
from wsgiref.simple_server import server_version

def modify_request(request):
    # Example modification: Change User-Agent header
    modified_request = request.replace("User-Agent: Mozilla", "User-Agent: BurpClone")
    return modified_request

def modify_response(response):
    # Example: Modify the response content
    response = response.replace("Server: Apache", "Server: CustomProxy")  # Modify IP for testing purposes
   
    return response

def handle_client_request(client_socket):
    
    database = sqlite3.connect('Captured_requests.db')
    cursor = database.cursor()
    
    print("Received request:")
    request = b''
    
    client_socket.setblocking(False)
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            request += data
            print(data.decode('utf-8'), end='')
        except BlockingIOError:
            break
    
    # Modify the request before forwarding
    modified_request = modify_request(request.decode('utf-8'))
    host, port = extract_host_port_from_request(modified_request)
    
    # Forward the modified request to the destination
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((host, port))
    destination_socket.sendall(modified_request.encode('utf-8'))
    print("Request forwarded to the destination")
    
    response = b""
    while True:
        data = destination_socket.recv(1024)
        if not response:
            break
        
        response += data
        # Modify the response before sending it to the client
    modified_response = modify_response(response.decode('utf-8'))
    client_socket.sendall(modified_response.encode('utf-8'))
    
    cursor.execute('INSERT INTO all_requests VALUES (CURRENT_TIMESTAMP, ?, ?)', 
                   (modified_request, modified_response))
    database.commit()    
        
    
    destination_socket.close()
    client_socket.close()
    cursor.close()
    database.close()

def extract_host_port_from_request(request):
    host_string_start = request.find('Host: ') + len('Host: ')
    host_string_end = request.find('\r\n', host_string_start)
    host_string = request[host_string_start:host_string_end]
    port = 80
    if ':' in host_string:
        host, port = host_string.split(':')
        port = int(port)
    else:
        host = host_string
    return host, port

def start_proxy_server(port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(20)
    print(f"Proxy server running on port {port}...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy_server()