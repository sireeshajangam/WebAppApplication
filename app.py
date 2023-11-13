# File: app.py
import os

name = os.getenv('NAME', 'DefaultName')
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace these values with your database connection details
db_config = {
    'host': 'rds-db.cptyiwp2zznq.us-east-1.rds.amazonaws.com',
    'user': 'foo',
    'password': 'IpA%hmRgq?M-60?u&[~KqbMq&1%y',
    'database': 'mydb',
}

# Define the route for the home page
@app.route('/')
def home():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Retrieve and display all users
    select_users_query = "SELECT * FROM users"
    cursor.execute(select_users_query)
    users = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return render_template('index.html', users=users)

# Define the route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Get user data from the form
    username = request.form['username']
    email = request.form['email']

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert the new user
    insert_user_query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    user_data = (username, email)
    cursor.execute(insert_user_query, user_data)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)
