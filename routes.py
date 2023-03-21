from app import app
from db import db
from flask import render_template, request, session, redirect
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"] 
    return render_template("index.html", error=error)

@app.route("/logincheck", methods=["POST"])
def logincheck():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        session["errormessage"] = "User doesn't exist"
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            session["errormessage"] = "Wrong password"
            return redirect("/")

@app.route("/makeaccount")
def makeaccount():
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"] 
    return render_template("makeaccount.html", error=error)

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    exists = result.fetchone()
    if exists:
        session["errormessage"] = "Username already taken"
        return redirect("/makeaccount")
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")