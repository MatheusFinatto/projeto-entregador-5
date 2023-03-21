from flask import Flask, render_template, jsonify, request
import requests
import sqlite3

app = Flask(__name__)

HEADERS = {
    'Client-ID': 'tvpgyurlv8vc88kd9dzum9s0ldlbf2',
    'Authorization': 'Bearer f1fzl61lle5vii2zwca6x2ghswne5z',
    'Content-Type': 'application/json',
}


@app.route('/top-games')
def top_games():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    url = 'https://api.igdb.com/v4/games'

    data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where rating_count > {rating_count}; sort rating desc; limit 50;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    newJson = []
    if response.ok:
        # response.json() é um array de objetos (url de imagens)
        newJson = {"data": response.json().copy()}
        for i in range(len(response.json())):
            newJson["data"][i]['cover']["url"] = response.json(
            )[i]['cover']["url"].replace("t_thumb", "t_1080p")
        return render_template('top-games.html', 
        newJson=newJson)
    else:
        return jsonify({'error': 'Failed to retrieve game cover.'}), response.status_code


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return null
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return null
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
