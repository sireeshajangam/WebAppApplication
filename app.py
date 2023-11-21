from flask import Flask, render_template, request, redirect
import mysql.connector
import boto3
import botocore
import json

app = Flask(__name__)

DATABASES = {}  # Define DATABASES at the module level

try:
    # Create a Secrets Manager client
    secrets_manager_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')

    secret_name = 'DBCredentials1'
    get_secret_value_response = secrets_manager_client.get_secret_value(SecretId=secret_name)

    secret_values = json.loads(get_secret_value_response['SecretString'])

    # Define the DATABASES dictionary using the retrieved secret values
    DATABASES = {
        'default': {
            'host': secret_values.get('MYSQL_DB_HOST', ''),
            'database': secret_values.get('MYSQL_DB_NAME', ''),
            'user': secret_values.get('MYSQL_DB_USER', ''),
            'password': secret_values.get('MYSQL_DB_PASSWORD', ''),
        }
    }

    # Ensure the 'create_guestbook_table()' function comes after the try-except block
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

    create_guestbook_table()

except (botocore.exceptions.ClientError, KeyError) as e:
    print(f"Error fetching secrets: {e}")

# Routes and other functions
# ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
