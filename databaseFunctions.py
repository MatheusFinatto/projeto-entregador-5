from flask import flash
import sqlite3
from sessionConfig import *

def get_db_connection():
    conn = sqlite3.connect('database.db')
    # conn.row_factory = sqlite3.Row
    return conn


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


def searchUser(email, password):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", [email, password])
        user = cur.fetchone()
        configureSessionUser(user)
        
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        flash('Email address or Password are incorrect!', 'message-error')
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
