from flask import flash
import sqlite3

from sqlalchemy import Null
from helpers.sessionConfig import *


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def getFavoritesDB():
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT game_id FROM favorites")
        user = cur.fetchall()
        conn.commit()
        conn.close()

        return user
    except:
        conn.close()
        return False


def addFavoriteDB(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO favorites (user_id, game_id) VALUES (?, ?)",
                    [user_id, game_id]
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def removeFavoriteDB(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("DELETE FROM favorites WHERE user_id=? AND game_id=?",
                    [user_id, game_id]
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def getWishlistDB():
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("SELECT game_id FROM wishlist")
        user = cur.fetchall()
        conn.commit()
        conn.close()

        return user
    except:
        conn.close()
        return False


def addWishlistDB(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO wishlist (user_id, game_id) VALUES (?, ?)",
                    [user_id, game_id]
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def removeWishlistDB(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("DELETE FROM wishlist WHERE user_id=? AND game_id=?",
                    [user_id, game_id]
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def addUser(email, username, password):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                    (email, username, password)
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def updateUser(email,  username, first_name="", last_name=""):
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("UPDATE users SET email = ?, username = ?, first_name = ?, last_name = ? WHERE email = ?",
                    (email, username, first_name, last_name, email)
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def addUserAuth(email, username, password, profile_img, first_name, last_name):
    conn = get_db_connection()
    is_auth = True
    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO users (email, username, password, profile_img, first_name, last_name, is_auth) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [email, username, password, profile_img,
                        first_name, last_name, is_auth]
                    )

        conn.commit()
        conn.close()

        return True
    except:
        conn.close()
        return False


def searchUser(email, password):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?", [email, password])
        user = cur.fetchone()

        conn.commit()
        conn.close()
        return user

    except:
        conn.close()
        flash('Email address or Password are incorrect!', 'message-error')
        return False


# Usada apenas para pegar o usuário e criar a sessão para ele caso tenha logado com social login
def searchUserInfo(email):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=?", [email])
        user = cur.fetchone()

        conn.commit()
        conn.close()
        return user
    except:
        conn.close()
        flash('Something went wrong.', 'message-error')
        return False


# Usada para pegar as informações do usuário para pesquisa rápida
def getUser(email):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=?", [email])
        user = cur.fetchone()

        conn.commit()
        conn.close()
        return user

    except:
        conn.close()
        flash('Email address are incorrect!', 'message-error')
        return False


def setUserPasswordRecoverCode(recover_code, email):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", [email])
        user = cur.fetchone()

        if user:
            cur.execute("UPDATE users " +
                        "SET recover_code=? " +
                        "WHERE email=?", [recover_code, email])
            conn.commit()
            conn.close()
            return True
        else:
            flash('No account found with this email!', 'message-error')
            conn.commit()
            conn.close()
            return False

    except:
        conn.close()
        return False


def getRecoverCode(email):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT code FROM users WHERE email=?", [email])
        code = cur.fetchone()

        conn.commit()
        conn.close()
        return code

    except:
        conn.close()
        return None


def updatePassword(email, password):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users " +
                    "SET password=? " +
                    "WHERE email=?", [password, email])
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def addGameRating(user_id, game_id, rating):
    conn = get_db_connection()
    print(user_id, game_id, rating)
    try:
        cur = conn.cursor()

        if getUserRating(user_id, game_id):
            cur.execute("UPDATE ratings " +
                        "SET rate=? " +
                        "WHERE user_id=? AND game_id=?", [rating, user_id, game_id])
            conn.commit()
            conn.close()
            return True
        else:
            cur.execute("INSERT INTO ratings (user_id, game_id, rate) VALUES (?, ?, ?)",
                        [user_id, game_id, rating]
                        )
            conn.commit()
            conn.close()
            return True
    except:
        conn.close()
        return False


# Retorna a avaliação do usuário para o jogo específicado, return float
def getUserRating(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT rate FROM ratings WHERE user_id=? AND game_id=?", [
                    user_id, game_id])
        ratings = cur.fetchone()
        conn.commit()
        conn.close()
        return ratings
    except:
        conn.close()
        return False


def userHasRating(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT rate FROM ratings WHERE user_id=? AND game_id=?", [
                    user_id, game_id])
        ratings = cur.fetchone()
        conn.commit()
        conn.close()
        if (ratings):
            return True
        else:
            return False
    except:
        conn.close()
        return False


def deleteUserRating(user_id, game_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM ratings WHERE user_id=? AND game_id=?", [
                    user_id, game_id])
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False
