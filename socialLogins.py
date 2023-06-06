import random
import string
from flask import Flask, render_template
from flask_session import Session
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.discord import make_discord_blueprint, discord
from databaseFunctions import *


def generatePassword():
    # choose from all uppercase letter
    letters = string.ascii_uppercase
    password = ''.join(random.choice(letters) for i in range(8))
    return password

def splitName(name):
    name = name.split()
    first_name = ''
    last_name = ''
    count = 0
    for i in name:
        if count <= len(name) / 2:
            first_name = first_name + i + ' '
        else:
            last_name = last_name + i + ' '
        count = count + 1
    return [first_name, last_name]


def createDiscordImgLink(id, avatar):
    link = 'https://cdn.discordapp.com/avatars/' + id + '/' + avatar + '.jpg'
    print(link)
    return link


def googleAuth():
    print(google)
    googleAccountInfo = google.get("/oauth2/v1/userinfo")
    print(googleAccountInfo)
    if (googleAccountInfo.ok):
        accountInfoJson = googleAccountInfo.json()
        print(accountInfoJson)
        first_name = accountInfoJson['given_name']
        last_name = accountInfoJson['family_name']
        username = first_name + last_name
        email = ''
        if email == '':
            email = username + '@gmail.com'
        user = searchUserInfo(email)
        if user == None:
            password = generatePassword()
        profile_img = accountInfoJson['picture']
        
        # Checa se o usuário está sendo criado ou já existe
        if user == None:
            # Adiciona o usuário na base de dados
            if addUserAuth(email, username, password, profile_img, first_name, last_name):
                user = searchUserInfo(email)
                if not user == None:
                    configureAuthSessionUser(user)
                    return 'new'
        else:
            configureAuthSessionUser(user)
            return 'login'

    return False


def githubAuth():
    githubAccountInfo = github.get('/user')
    if githubAccountInfo.ok:
        accountInfoJson = githubAccountInfo.json()
        username = accountInfoJson['login']
        email = ''
        if email == '':
            email = username + '@gmail.com'
        user = searchUserInfo(email)
        if user == None:
            password = generatePassword()
        name = accountInfoJson['name']
        name = splitName(name)
        first_name = name[0]
        last_name = name[1]
        
        # Checa se o usuário está sendo criado ou já existe
        if user == None:
            # Adiciona o usuário na base de dados
            if addUserAuth(email, username, password, '', first_name, last_name):
                user = searchUserInfo(email)
                if not user == None:
                    configureAuthSessionUser(user)
                    return 'new'
        else:
            configureAuthSessionUser(user)
            return 'login'

    return False


def twitterAuth():
    twitterAccountInfo = twitter.get('account/verify_credentials.json')
    if twitterAccountInfo.ok:
        accountInfoJson = twitterAccountInfo.json()
        username = accountInfoJson['screen_name']
        email = ''
        if email == '':
            email = username + '@gmail.com'
        user = searchUserInfo(email)
        if user == None:
            password = generatePassword()
        name = accountInfoJson['name']
        name = splitName(name)
        first_name = name[0]
        last_name = name[1]

        # Checa se o usuário está sendo criado ou já existe
        if user == None:
            # Adiciona o usuário na base de dados
            if addUserAuth(email, username, password, '', first_name, last_name):
                user = searchUserInfo(email)
                if not user == None:
                    configureAuthSessionUser(user)
                    return 'new'
        else:
            configureAuthSessionUser(user)
            return 'login'

    return False


def discordAuth():
    discordAccountInfo = discord.get("/api/users/@me")
    if (discordAccountInfo.ok):
        accountInfoJson = discordAccountInfo.json()
        first_name = ''
        last_name = ''
        username = accountInfoJson['username']
        email = accountInfoJson['email']
        user = searchUserInfo(email)
        if user == None:
            password = generatePassword()
        profile_img = createDiscordImgLink(accountInfoJson['id'], accountInfoJson['avatar'])
        
        # Checa se o usuário está sendo criado ou já existe
        if user == None:
            # Adiciona o usuário na base de dados
            if addUserAuth(email, username, password, profile_img, first_name, last_name):
                user = searchUserInfo(email)
                if not user == None:
                    configureAuthSessionUser(user)
                    return 'new'
        else:
            configureAuthSessionUser(user)
            return 'login'

    return False