from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

intercept_enabled = False  # Global variable to track intercept status

@app.route('/')
def home():
    return render_template('index.html', intercept=intercept_enabled)

@app.route('/toggle_intercept', methods=['POST'])
def toggle_intercept():
    global intercept_enabled
    intercept_enabled = not intercept_enabled
    return jsonify({'intercept': intercept_enabled})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
