from app import app
from db import db
from sqlalchemy import text
from flask import session
from datetime import datetime

def createcomment(post_id, username, content):

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user_id = result.fetchone()[0]

    if content.isspace() == True:
        session["errormessage"] = "Comment can't be blank"
        return 0
    
    if len(content) < 1:
        session["errormessage"] = "Comment should be atleast 1 character long"
        return 0
    
    now = datetime.now()
    date = now.strftime("%m/%d/%Y, %H:%M:%S")

    sql = "INSERT INTO comments(post_id, user_id, username, description, date) VALUES (:post_id, :user_id, :username, :description, :date)"
    db.session.execute(text(sql), {"post_id":post_id, "user_id":user_id, "username":username, "description":content, "date":date})
    db.session.commit()

    return

def postcomments(id):
    sql = "SELECT id, username, description, date FROM comments WHERE post_id=:post_id"
    result = db.session.execute(text(sql), {"post_id":id})
    return result.fetchall()
