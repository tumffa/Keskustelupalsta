from app import app
from db import db
from sqlalchemy import text
from flask import session
from datetime import datetime
import pytz

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
    
    if len(content) > 3000:
        session["errormessage"] = "Max 3000 characters"
        return 0
    
    time = pytz.timezone("Europe/Helsinki")
    now = datetime.now(time)
    date = now.strftime("%m/%d/%Y, %H:%M:%S")

    sql = "INSERT INTO comments(post_id, user_id, username, description, date) VALUES (:post_id, :user_id, :username, :description, :date)"
    db.session.execute(text(sql), {"post_id":post_id, "user_id":user_id, "username":username, "description":content, "date":date})
    db.session.commit()

    return

def postcomments(id):
    list = []

    sql = "SELECT id, username, description, date FROM comments WHERE post_id=:post_id"
    result = db.session.execute(text(sql), {"post_id":id}).fetchall()

    for comment in result:
        sql = "SELECT id, username, respondsto, description, date FROM responses WHERE comment_id=:comment_id"
        responses = db.session.execute(text(sql), {"comment_id":comment.id}).fetchall()
        list.append((comment, responses))

    return list


def createresponse(comment_id, username, content):

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user_id = result.fetchone()[0]

    if content.isspace() == True:
        session["errormessage"] = "Comment can't be blank"
        return 0
    
    if len(content) < 1:
        session["errormessage"] = "Comment should be atleast 1 character long"
        return 0
    
    if len(content) > 2000:
        session["errormessage"] = "Max 2000 characters"
        return 0
    
    time = pytz.timezone("Europe/Helsinki")
    now = datetime.now(time)
    date = now.strftime("%m/%d/%Y, %H:%M:%S")

    sql = "INSERT INTO responses(comment_id, user_id, username, description, date) VALUES (:comment_id, :user_id, :username, :description, :date)"
    db.session.execute(text(sql), {"comment_id":comment_id, "user_id":user_id, "username":username, "description":content, "date":date})
    db.session.commit()
    return

def get_comment(id):
    sql = "SELECT id, description, username, date FROM comments WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchone()

def comment_and_responses(id):
    sql = "SELECT id, description, username, date FROM comments WHERE id=:id"
    comment = db.session.execute(text(sql), {"id":id}).fetchone()
    sql = "SELECT id, username, respondsto, description, date FROM responses WHERE comment_id=:comment_id"
    responses = db.session.execute(text(sql), {"comment_id":id}).fetchall()
    return (comment, responses)

def delete_comment(id):
    sql = "SELECT username FROM comments WHERE id=:id"
    name = db.session.execute(text(sql), {"id":id}).fetchone()[0]
    if session["username"] != name:
        return 0
    sql = "DELETE FROM comments WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return

def delete_response(id):
    sql = "SELECT username FROM responses WHERE id=:id"
    name = db.session.execute(text(sql), {"id":id}).fetchone()[0]
    if session["username"] != name:
        return 0
    sql = "DELETE FROM responses WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return