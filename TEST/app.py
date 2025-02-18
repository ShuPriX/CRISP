from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

PORT = 8888

@app.route('/', methods=['GET'])
def home():
    try:
        # Connect to the SQLite database
        database = sqlite3.connect('./Captured_requests.db')
        cursor = database.cursor()
        # Clear the database
        cursor.execute('DELETE FROM all_requests')
        database.commit()
        # Execute the query to fetch all requests
        entries = cursor.execute('select * from all_requests order by Request_Number desc').fetchall()
        # Close the database connection
        database.close()
        # Render the template with the fetched entries
        return render_template("home.html", entries=entries)
    except Exception as e:
        # Log the error and return an error message
        app.logger.error(f"Error occurred: {e}")
        return f"An error occurred: {e}", 500

@app.route('/intercept', methods=['POST'])
def intercept():
    try:
        request_id = request.form['request_id']
        modified_request = request.form['modified_request']
        # Intercept the request
        intercept_request(request_id, modified_request)
        return redirect(url_for('home'))
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return f"An error occurred: {e}", 500

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

if __name__ == "__main__":
    app.run(port=PORT)