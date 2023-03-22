from app import app
from db import db
import users
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
    users.check_login(username, password)
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
    result = users.make_account(username, password)
    if result == 0:
        return redirect("/makeaccount")
    return redirect ("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")