from flask import Flask, render_template, jsonify, request, url_for, flash, redirect, session
import sys
import requests
import random
import string
from flask_session import Session
from sessionConfig import *
from databaseFunctions import *
from emailConfig import *

app = Flask(__name__)
# A secret key funciona para o Flask para deixar uma sessão segura e poder lembrar todos os request
# e mensagens acionadas em cada sessão. Apenas podem ser modificados dados de uma sessão com a secret key
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
app.config['SECRET_KEY'] = '27f09c6a065869155e37ed8e7830865a6046ec7d425c2f5c'

# Configurando a sessão
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Configurando email service
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '94e6efcfb7801a'
app.config['MAIL_PASSWORD'] = '07b5faafdb617e'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

Session(app)


HEADERS = {
    'Client-ID': 'tvpgyurlv8vc88kd9dzum9s0ldlbf2',
    'Authorization': 'Bearer f1fzl61lle5vii2zwca6x2ghswne5z',
    'Content-Type': 'application/json',
}


def generateRecoverPasswordCode():
    # choose from all uppercase letter
    letters = string.ascii_uppercase
    code = ''.join(random.choice(letters) for i in range(5))
    return code


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email:
            flash('Email is required!', 'message-error')
        elif not password:
            flash('Password is required!', 'message-error')
        else:
            # Tenta encontrar o usuario na base de dados
            if searchUser(email, password):
                return redirect('/landing')
            else:
                return render_template('login.html')
    else:
        if session.get("username"):
            return redirect('landing')

    return render_template('login.html')


@app.route('/logout')
def logout():
    clearSession()
    return redirect('/login')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form['email']

        if not email:
            flash('Email is required!', 'message-error')
        else:
            code = generateRecoverPasswordCode()

            if setUserPasswordRecoverCode(code, email):
                sendRecoverCode(code, email, mail)
                return render_template('forgot-password.html', code_sent=True, code=code)
            else:
                return render_template('forgot-password.html')

    return render_template('forgot-password.html', code_sent=False, code=None)


@app.route('/set-new-password', methods=['GET', 'POST'])
def setNewPassword():
    return render_template('set-new-password.html')

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
                return redirect('/login')
            else:
                flash('Your account could not be created!', 'message-error')

    return render_template('register.html')


@app.route('/landing')
def landing():
    if not session.get("username"):
        flash('You shall not pass!', 'message-error')
        return redirect('/login')
    return render_template('landing.html')


@app.route('/top-games')
def top_games():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    limit = request.args.get('limit', default=20, type=int)
    url = 'https://api.igdb.com/v4/games'
    data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where rating_count > {rating_count}; sort rating desc; limit {limit};'
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


@app.route('/search')
def search():
    name = request.args.get('query')
    print(name)
    url = 'https://api.igdb.com/v4/games'
    data = f'search "{name}"; fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    newJson = []
    if response.ok:
        print(response.json())
        newJson = {"data": response.json().copy()}
        for i in range(len(response.json())):
            if 'cover' in newJson["data"][i]:
                newJson["data"][i]['cover']["url"] = response.json(
                )[i]['cover']["url"].replace("t_thumb", "t_1080p")

        return render_template('search.html', newJson=newJson, name=name)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
