from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api', methods=['POST'])
def api():
    # Get the JSON data from the request
    data = request.get_json()
    # Process the data as needed
    response = {
        'status': 'success',
        'data': data
    }
    # Return a JSON response
    return jsonify(response)

# Proxy
@app.route('/proxy', methods=['POST'])
def proxy():
    # Get the JSON data from the request
    data = request.get_json()
    # Forward the request to the /api endpoint
    new_request = requests.post('http://127.0.0.1:8080/api', json=data)
    # Return the response from the /api endpoint
    return new_request.json()

if __name__ == "__main__":
    app.run(port=8080)