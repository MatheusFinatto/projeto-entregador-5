from user_agents import parse
from APIConfigHelpers import *
from socialLogins import *
from emailConfig import *
from databaseFunctions import *
from sessionConfig import *
from flask_session import Session
from flask import Flask, jsonify, render_template, request, flash, redirect, session, url_for
from time import time
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.discord import make_discord_blueprint, discord
import requests
import random
import string
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '8a7418047c15f3'
app.config['MAIL_PASSWORD'] = '9823cf20679946'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

Session(app)

# Caso a API pare de responder, deve ser feito um post para POST: https://id.twitch.tv/oauth2/token?client_id=abcdefg12345&client_secret=hijklmn67890&grant_type=client_credentials
# substituindo client_id e client_secret para os dados da API da Twithc, para receber uma nova access token para colocar no Authorization do HEADERS
#
# Resposta esperada:
# {
#     "access_token": "14qxb5v1pv80sfxvj5cu2ova51yojs",
#     "expires_in": 5455989,
#     "token_type": "bearer"
# }

HEADERS = {
    'Client-ID': '96fcqym7jumwvac81mb74143m33ron',
    'Authorization': 'Bearer 14qxb5v1pv80sfxvj5cu2ova51yojs',
    'Content-Type': 'application/json',
}


# HOME #
@app.route('/')
def index():
    if not session.get('id'):
        if twitter.authorized:
            response = twitterAuth()
            if response == 'new':
                return redirect('/set-password')
            elif response == 'login':
                return redirect('/top-games')
            else:
                flash('Something went wrong. Please, try again', 'message-error')
                return redirect('/login')
        elif github.authorized:
            response = githubAuth()
            accountInfo = github.get('/user')
            if response == 'new':
                return redirect('/set-password')
            elif response == 'login':
                return redirect('/top-games')
            else:
                flash('Something went wrong. Please, try again', 'message-error')
                return redirect('/login')
        else:
            return render_template('index.html')
    return render_template('index.html')


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
            user = searchUser(email, password)
            if user:
                configureSessionUser(user)
                return redirect('/landing')
            else:
                return render_template('login.html')
    else:
        if session.get("username"):
            return redirect('landing')
    return render_template('login.html')



google_blueprint = make_google_blueprint(client_id='', client_secret='')
github_blueprint = make_github_blueprint(client_id='7be17c70865b560199c7', client_secret='7a4bee7baa0597f46549c6ea87b8af119bd46ce9')
twitter_blueprint = make_twitter_blueprint(api_key='OaP0WeCQ19FK7D5HE25oVq7is', api_secret='1AhNEgoZ6nBDAwV5uMIdsKZadwjty3KFaFXVxUWGlUtkGWXqHy')
discord_blueprint = make_discord_blueprint(client_id='', client_secret='')

app.register_blueprint(google_blueprint, url_prefix='/google_login')
app.register_blueprint(github_blueprint, url_prefix='/github_login')
app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')
app.register_blueprint(discord_blueprint, url_prefix='/discord_login')


@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    return redirect('/')


@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    return redirect('/')


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
            return render_template('set-password.html')
        elif not confirmPassword:
            flash('Confirmation of password is required!', 'message-error')
            return render_template('set-password.html')
        elif not match_passwords:
            flash('The passwords must be the same', 'message-error')
            return render_template('set-password.html')
        else:
            if updatePassword(email, password):
                flash('Your password has been changed', 'message-success')
                if not session.get("username"):
                    return render_template('login.html')
                else:
                    if session["recover"]:
                        session["recover"] = False

                    return redirect('/profile')
            else:
                flash('Something went wrong. Please, try again', 'message-error')
                return render_template('set-password.html')

    return render_template('set-password.html')


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
    data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where rating_count > {rating_count}; sort rating desc; limit {limit};'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)

    # Desabilita botões de favoritos e wishlist caso o usuário não esteja logado
    buttonStatus = "" if session.get('id') else "disabled"

    if response.ok:
        newJson = imageConfig(response, 'cover')
        newJson = getFavorites(newJson)
        newJson = getWishlist(newJson)
        newJson = timeConfig(newJson)
        return render_template('top-games.html', newJson=newJson, buttonStatus=buttonStatus)


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
    data = f'search "{name}"; fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where rating > {rating} & rating_count > {rating_count}; limit {limit};'
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
        data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where id = ({string});limit 500;'
        headers = HEADERS
        response = requests.post(url, headers=headers, data=data)
        newJson = []
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            newJson = getWishlist(newJson)
            newJson = timeConfig(newJson)
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
        data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where id = ({string}); limit 500;'
        headers = HEADERS
        response = requests.post(url, headers=headers, data=data)
        newJson = []
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            newJson = getWishlist(newJson)
            newJson = timeConfig(newJson)
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
        # Pega a avaliação do jogo ao entrar na tela de detalhes para enviar para o elemento rate.game.html
        gameRating = gameRateByUser(game_id)
        return render_template('details.html', newJson=newJson, is_mobile=is_mobile, game_id=game_id, gameRating=gameRating)


# 404 #
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Lançamentos recentes #
@app.route('/latest')
def latest():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    limit = request.args.get('limit', default=20, type=int)
    url = 'https://api.igdb.com/v4/games'
    timeInSeconds = round(time())
    data = f'fields  name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where rating != null & first_release_date != null & cover != null & first_release_date <= {timeInSeconds}; sort first_release_date desc; limit 20;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        newJson = imageConfig(response, 'cover')
        newJson = getFavorites(newJson)
        newJson = getWishlist(newJson)
        newJson = timeConfig(newJson)
        return render_template('latest.html', newJson=newJson)


# Lançamentos próximos #


@app.route('/coming-soon')
def coming_soon():
    rating_count = request.args.get('rating_count', default=1000, type=int)
    limit = request.args.get('limit', default=20, type=int)
    timeInSeconds = round(time())
    url = 'https://api.igdb.com/v4/games'
    data = f'fields  name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where  first_release_date != null & cover != null & first_release_date > {timeInSeconds}; sort first_release_date asc; limit 20;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        newJson = imageConfig(response, 'cover')
        newJson = getFavorites(newJson)
        newJson = getWishlist(newJson)
        newJson = timeConfig(newJson)
        return render_template('top-games.html', newJson=newJson)
    return render_template('coming-soon.html')


# Página do perfil do usuário
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    favorites = getFavoritesDB()
    string = ",".join([str(x[0]) for x in favorites])
    url = 'https://api.igdb.com/v4/games'
    data = f'fields name, cover.url, rating, rating_count, platforms.name, platforms.platform_logo.url, first_release_date; where id = ({string});limit 500;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    newJson = []
    print('entrou1')

    if request.method == 'POST':
        print('entrou')
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']

        if not email:
            flash('Email is required!', 'message-error')
        elif not username:
            flash('Username is required!', 'message-error')
        else:
            if updateUser(email, username, first_name, last_name):
                flash('Your account was updated!', 'message-success')
            else:
                flash('Your account could not be updated! Try again', 'message-error')

        user = getUser(email)
        updateSession(user)
    
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            return render_template('profile.html', newJson=newJson)
        
        return render_template('profile.html', newJson=[])
    
    if request.method == 'GET':
        if response.ok:
            newJson = imageConfig(response, 'cover')
            newJson = getFavorites(newJson)
            return render_template('profile.html', newJson=newJson)
        
        return render_template('profile.html', newJson=[])


@app.route('/rate-game', methods=['POST'])
def rateGame():
    if request.method == 'POST':
        print(request.form)
        print(session.get("id"))
        user_id = session.get("id")
        game_id = request.form['game_id']
        rating = float(request.form['rating'])

        if rating < 0 or rating > 5:
            flash('Rating must be between 0 and 5', 'message-error')

        if addGameRating(user_id, game_id, rating):
            return redirect(url_for('game_details', game_id=game_id))
        else:
            return "Nao salvou"


def gameRateByUser(game_id):
    user_id = session.get("id")
    
    rating = getUserRating(user_id=user_id, game_id=game_id)

    rating = float(rating[0])

    return rating


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
