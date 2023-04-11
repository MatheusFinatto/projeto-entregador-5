from flask import session
from flask_session import Session

def configureAuthSessionUser(user):
    session["id"] = user[0]
    session["email"] = user[1]
    session["username"] = user[2]
    session["profile_img"] = user[5]
    session["created"] = user[9]
    session["recover"] = False

def configureSessionUser(user, recover=False):
    session["id"] = user[0]
    session["email"] = user[1]
    session["username"] = user[2]
    session["profile_img"] = user[5]
    session["created"] = user[9]
    session["recover"] = recover


def addCodeRecoverCookie(email, code, recover=False):
    session["email"] = email
    session["code"] = code
    session["recover"] = recover


def clearSession():
    for info in session:
        # Limpa todos os dados da sessão
        session[info] = None
    return None