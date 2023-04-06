from flask import session
from flask_session import Session

def configureSessionUser(user):
    session["id"] = user[0]
    session["email"] = user[1]
    session["username"] = user[2]
    session["profile_img"] = user[5]
    session["created"] = user[9]


def addCodeRecoverCookie(email, code, recover=False):
    session["email"] = email
    session["code"] = code
    if recover:
        session["recover"] = True


def clearSession():
    for info in session:
        # Limpa todos os dados da sessão
        session[info] = None
    return None