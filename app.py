from flask import Flask, jsonify, render_template, request, flash, redirect, session
import sys
import requests
import random
import string
from flask_session import Session
from sessionConfig import *
from databaseFunctions import *
from emailConfig import *
from APIConfigHelpers import *
from user_agents import parse


app = Flask(__name__)
# A secret key funciona para o Flask para deixar uma sessão segura e poder lembrar todos os request
# e mensagens acionadas em cada sessão. Apenas podem ser modificados dados de uma sessão com a secret key
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
app.config['SECRET_KEY'] = '27f09c6a065869155e37ed8e7830865a6046ec7d425c2f5c'

# Configurando a sessão
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_DIR'] = 'sessions'

# Configurando email service
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
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


# LOGIN AND REGISTER #
def generateRecoverPasswordCode():
    # choose from all uppercase letter
    letters = string.ascii_uppercase
    code = ''.join(random.choice(letters) for i in range(5))
    return code


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
                addCodeRecoverCookie(email, code, True)
                return render_template('forgot-password.html', code_sent=True, code=code)
            else:
                return render_template('forgot-password.html', code_sent=False, code=None)

    return render_template('forgot-password.html', code_sent=False, code=None)


@app.route('/set-password', methods=['GET', 'POST'])
def setPassword():
    if request.method == 'POST':
        password = request.form['password']
        confirmPassword = request.form['confirm-password']
        email = session.get("email")
        match_passwords = (password == confirmPassword)

        if not password:
            flash('Password is required!', 'message-error')
            return render_template('set-new-password.html')
        elif not confirmPassword:
            flash('Confirmation of password is required!', 'message-error')
            return render_template('set-new-password.html')
        elif not match_passwords:
            flash('The passwords must be the same', 'message-error')
            return render_template('set-new-password.html')
        else:
            if updatePassword(email, password):
                flash('Your password has been changed', 'message-success')
                if not session.get("username"):
                    return render_template('login.html')
                else:
                    if session["recover"]:
                        session["recover"] = False

                    # TODO retornar para a tela de detalhes da conta do usuário
                    return render_template('index.html')
            else:
                flash('Something went wrong. Please, try again', 'message-error')
                return render_template('set-new-password.html')

    return render_template('set-new-password.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        match_passwords = (password == confirm_password)

        if not email:
            flash('Email is required!', 'message-error')
        elif not username:
            flash('Username is required!', 'message-error')
        elif not password:
            flash('Password is required!', 'message-error')
        elif not confirm_password:
            flash('Confirmed Password is required!', 'message-error')
        elif not match_passwords:
            flash('The passwords must be the same', 'message-error')
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


# BEST GAMES #
@app.route('/top-games')
def top_games():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    limit = request.args.get('limit', default=20, type=int)
    url = 'https://api.igdb.com/v4/games'
    data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where rating_count > {rating_count}; sort rating desc; limit {limit};'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        newJson = imageConfig(response, 'cover')
        newJson = getFavorites(newJson)
        newJson = getWishlist(newJson)
        return render_template('top-games.html', newJson=newJson)


# SEARCH #
@app.route('/search')
def search():
    rating_count = request.args.get('rating_count', default=1, type=int)
    rating = request.args.get('rating', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    name = request.args.get('query')
    if not name:
        name = request.args.get('name')
    url = 'https://api.igdb.com/v4/games'
    data = f'search "{name}"; fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where rating > {rating} & rating_count > {rating_count}; limit {limit};'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        newJson = imageConfig(response, 'cover')
        return render_template('search.html', newJson=newJson, name=name)


# FAVORITES #
@app.route('/favorites')
def favorites():
    if not session.get("username"):
        return redirect('/login')
    else:
        favorites = getFavoritesDB()
        string = ",".join([str(x[0]) for x in favorites])
        url = 'https://api.igdb.com/v4/games'
        data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where id = ({string});limit 500;'
        headers = HEADERS
        response = requests.post(url, headers=headers, data=data)
        newJson = []
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            newJson = getWishlist(newJson)
        return render_template('favorites.html', newJson=newJson, forceUpdate=True)


@app.route('/add-favorite', methods=['POST'])
def addFavorite():
    if request.method == 'POST':
        game_id = request.form['game_id']
        user_id = session.get("id")
        addFavoriteDB(user_id, game_id)
        return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/remove-favorite', methods=['POST'])
def removeFavorite():
    if request.method == 'POST':
        game_id = request.form['game_id']
        user_id = session.get("id")
        removeFavoriteDB(user_id, game_id)
        return jsonify({'success': True})
    return jsonify({'success': False})


# WISHLIST #
@app.route('/wishlist')
def wishlist():
    if not session.get("username"):
        return redirect('/login')
    else:
        wishlist = getWishlistDB()
        string = ",".join([str(x[0]) for x in wishlist])
        url = 'https://api.igdb.com/v4/games'
        data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url; where id = ({string}); limit 500;'
        headers = HEADERS
        response = requests.post(url, headers=headers, data=data)
        newJson = []
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            newJson = getWishlist(newJson)
        return render_template('wishlist.html', newJson=newJson, forceUpdate=True)


@app.route('/add-wishlist', methods=['POST'])
def addWishlist():
    if request.method == 'POST':
        game_id = request.form['game_id']
        user_id = session.get("id")
        addWishlistDB(user_id, game_id)

        return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/remove-wishlist', methods=['POST'])
def removeWishlist():
    if request.method == 'POST':
        game_id = request.form['game_id']
        user_id = session.get("id")
        removeWishlistDB(user_id, game_id)
        return jsonify({'success': True})
    return jsonify({'success': False})


# DETAILS #
@app.route('/details/<int:game_id>')
def game_details(game_id):
    user_agent_string = request.headers.get('User-Agent')
    is_mobile = False
    if user_agent_string:
        user_agent = parse(user_agent_string)
        is_mobile = user_agent.is_mobile
    url = 'https://api.igdb.com/v4/games'
    data = f'fields rating, name,rating_count, cover.url, platforms.name, platforms.platform_logo.url, artworks.url; where id = {game_id};'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        newJson = imageConfig(response, 'cover')
        newJson = imageConfig(newJson, 'artworks')
        return render_template('details.html', newJson=newJson, is_mobile=is_mobile)


# HOME #
@app.route('/')
def index():
    return render_template('index.html')


# 404 #
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
