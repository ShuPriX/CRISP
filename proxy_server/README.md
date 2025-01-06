# README.md

# Python Proxy Server

This project implements a simple proxy server that listens on port 8080 and forwards incoming requests to the appropriate destination, returning the responses to the clients.

## Requirements

- Python 3.x
- Flask (or any other required libraries listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-proxy-server
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the proxy server, execute the following command:

```
python src/proxy.py
```

The server will start listening on `http://localhost:8080`.

## Example

You can test the proxy server by sending a request to it using a web browser or a tool like `curl`:

```
Invoke-WebRequest -Uri "http:/example.com" -Proxy "http://127.0.0.1:8080"
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.