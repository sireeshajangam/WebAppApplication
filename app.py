from flask import Flask, render_template, request, redirect
import mysql.connector
import boto3
import json

app = Flask(__name__)

# Create a Secrets Manager client
secrets_manager_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')

# Retrieve the secret values from AWS Secrets Manager
secret_name = 'DBCredentials1'
get_secret_value_response = secrets_manager_client.get_secret_value(SecretId=secret_name)
secret_values = json.loads(get_secret_value_response['SecretString'])

# Define the DATABASES dictionary using the retrieved secret values
db_config = {
    'host': secret_values.get('host', ''),
    'database': secret_values.get('dbname', ''),
    'user': secret_values.get('username', ''),
    'password': secret_values.get('password', ''),
}

# Create a 'guestbook' table in MySQL with columns 'id', 'name', 'message', and 'timestamp'
def create_guestbook_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guestbook (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.close()

# Ensure the 'guestbook' table exists
create_guestbook_table()

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
    app.run(host='0.0.0.0', port=5000, debug=True)
