from flask import session
from flask_session import Session

def configureSessionUser(user):
    session["id"] = user[0]
    session["email"] = user[1]
    session["username"] = user[2]
    return None


def clearSession():
    for info in session:
        # Limpa todos os dados da sessão
        session[info] = None
    return None