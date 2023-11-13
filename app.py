from flask import Flask, render_template, send_from_directory
import json

app = Flask(__name__)

# Define route to serve static files (CSS, JS, etc.)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Define the route for the home page
@app.route('/')
def home():
    articles = load_articles()
    return render_template('index.html', articles=articles)

def load_articles():
    try:
        with open('articles.json', 'r') as file:
            articles = json.load(file)
        return articles
    except FileNotFoundError:
        return []

if __name__ == '__main__':
    app.run(debug=True, port=8000)
