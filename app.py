from flask import Flask, render_template, request, redirect
import mysql.connector
import boto3
import json
##

app = Flask(__name__)


# Create a Secrets Manager client
secrets_manager_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')

# Retrieve the secret values from AWS Secrets Manager
secret_name = 'DBCredentials'
get_secret_value_response = secrets_manager_client.get_secret_value(SecretId=secret_name)

# Parse the secret JSON string to obtain key-value pairs
secret_values = json.loads(get_secret_value_response['SecretString'])

# Database configuration using retrieved secret values
DATABASES = {
    'default': {
        'host': secret_values['MYSQL_DB_HOST'],
        'database': secret_values['MYSQL_DB_NAME'],
        'user': secret_values['MYSQL_DB_USER'],
        'password': secret_values['MYSQL_DB_PASSWORD'],
    }
}

# Ensure the 'guestbook' table exists
def create_guestbook_table():
    conn = mysql.connector.connect(**DATABASES['default'])
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

# Create 'guestbook' table if not exists
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
    conn = mysql.connector.connect(**DATABASES['default'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guestbook ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_message_to_db(name, message_text):
    conn = mysql.connector.connect(**DATABASES['default'])
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guestbook (name, message) VALUES (%s, %s)", (name, message_text))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
