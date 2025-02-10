from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.run(port=8080)

@app.POST('/api')
def api(request):
    # ....Your code here
    # return new_request





# PORXY
import requests


reuest
new_request = requests.post('127.0.0.1:8080/api/', data=request)

