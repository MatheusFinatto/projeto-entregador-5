from flask import Flask, render_template, jsonify, request, url_for, flash, redirect
import sys
import requests
import sqlite3

app = Flask(__name__)
# A secret key funciona para o Flask para deixar uma sessão segura e poder lembrar todos os request
# e mensagens acionadas em cada sessão. Apenas podem ser modificados dados de uma sessão com a secret key
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
app.config['SECRET_KEY'] = '27f09c6a065869155e37ed8e7830865a6046ec7d425c2f5c'

HEADERS = {
    'Client-ID': 'tvpgyurlv8vc88kd9dzum9s0ldlbf2',
    'Authorization': 'Bearer f1fzl61lle5vii2zwca6x2ghswne5z',
    'Content-Type': 'application/json',
}


@app.route('/top-games')
def top_games():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    url = 'https://api.igdb.com/v4/games'
    data = f'fields name, cover.url, rating, rating_count; where rating != null & rating_count != null & rating_count > {rating_count}; sort rating desc; limit 50;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    newJson = []
    if response.ok:
        # response.json() é um array de objetos (url de imagens)
        newJson = {"data": response.json().copy()}
        for i in range(len(response.json())):
            newJson["data"][i]['cover']["url"] = response.json(
            )[i]['cover']["url"].replace("t_thumb", "t_1080p")
        return render_template('top-games.html', newJson=newJson)
    else:
        return jsonify({'error': 'Failed to retrieve game cover.'}), response.status_code


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def addUser(email, username, password):
    conn = sqlite3.connect('database.db')
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
            (email, username, password)
        )
        
        conn.commit()
        conn.close()

        return True
    except:
        return False


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not email:
            flash('Email is required!', 'message-error')
        elif not username:
            flash('Username is required!', 'message-error')
        elif not password:
            flash('Password is required!', 'message-error')
        elif not confirm_password:
            flash('Confirmed Password is required!', 'message-error')
        else:
            if addUser(email, username, password):
                flash('Your account was created!', 'message-success')
                return redirect(url_for('.login'))
            else:
                flash('Your account could not be created!', 'message-error')
        
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
