# Proxy Server

This project implements a simple proxy server that listens on port 8080 and forwards incoming requests to the appropriate destination, returning the responses to the clients. The server also allows modification of HTTP requests and responses in notepad before they are forwarded.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd proxy_server
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the proxy server, create a python virtual environment and execute the following command:

```
python proxy_server/modify_response_in_notepad.py
```

The server will start listening on `http://localhost:8080`.

now open another python virtual environment and run the following command to test the proxy server:

```
Invoke-WebRequest -Uri "http:/example.com" -Proxy "http://127.0.0.1:8080"
```
This will open notepad and show the request, you can modify the request and save it, then the server will forward the modified request to the destination.
