from app import app
from db import db
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def check_login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        session["errormessage"] = "User doesn't exist"
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            session["errormessage"] = "Wrong password"
    return

def make_account(username, password):
    hash_value = generate_password_hash(password)
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    exists = result.fetchone()
    if exists:
        session["errormessage"] = "Username already taken"
        return 0
    if len(username) < 2:
        session["errormessage"] = "Username is too short"
        return 0
    elif len(username) > 30:
        session["errormessage"] = "Username is too long"
        return 0
    if len(password) < 4:
        session["errormessage"] = "Password is too short"
        return 0
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return