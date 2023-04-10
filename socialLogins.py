import random
import string
from flask import Flask, render_template
from flask_session import Session
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
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


def twitterAuth():
    twitterAccountInfo = twitter.get('account/verify_credentials.json')
    if twitterAccountInfo.ok:
        accountInfoJson = twitterAccountInfo.json()
        username = accountInfoJson['screen_name']
        email = ''
        if email == '':
            email = username + '@gmail.com'
        user = searchUserAuth(email)
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
                user = searchUserAuth(email)
                if not user == None:
                    configureAuthSessionUser(user)
                    return 'new'
        else:
            configureAuthSessionUser(user)
            return 'login'

    return False