from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Replace these values with your MySQL details
db_config = {
    'host': 'rds-db.cptyiwp2zznq.us-east-1.rds.amazonaws.com',
    'user': 'foo',
    'password': 'IpA%hmRgq?M-60?u&[~KqbMq&1%y',
    'database': 'mydb'
}

# Create a 'guestbook' table in MySQL with columns 'id', 'name', 'message', and 'timestamp'

@app.route('/')
def index():
    messages = get_messages()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        name = request.form['name']
        message_text = request.form['message']
        add_message_to_db(name, message_text)
        return redirect('/')
    return render_template('add_message.html')

def get_messages():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guestbook ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_message_to_db(name, message_text):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guestbook (name, message) VALUES (%s, %s)", (name, message_text))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
