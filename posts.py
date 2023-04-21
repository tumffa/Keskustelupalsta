from app import app
from db import db
from topics import get_topic_id
from sqlalchemy import text
from flask import session
from datetime import datetime
import pytz

def topicposts(id):
    sql = "SELECT name, description, id, username, date FROM posts WHERE topic_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchall()

def create_post(topic_id, username, name, description):
    sql = "SELECT name FROM topics WHERE id=:id"
    result = db.session.execute(text(sql), {"id":topic_id})
    topic_name = result.fetchone()[0]

    if len(name) < 1:
        session["errormessage"] = "Post title has to be atlseast 1 character long"
        return topic_name
    
    if len(name) > 250:
        session["errormessage"] = "Post title can't be longer than 250 characters"
        return topic_name

    if len(description) > 4000:
        session["errormessage"] = "Max 4000 characters"
        return topic_name

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user_id = result.fetchone()[0]

    time = pytz.timezone("Europe/Helsinki")
    now = datetime.now(time)
    date = now.strftime("%m/%d/%Y, %H:%M:%S")

    sql = "INSERT INTO posts (topic_id, user_id, username, name, description, date) VALUES (:topic_id, :user_id, :username, :name, :description, :date)"
    db.session.execute(text(sql), {"topic_id":topic_id, "user_id":user_id, "username":username, "name":name, "description":description, "date":date})
    db.session.commit()
    return topic_name

def get_post(id):
    sql = "SELECT id, name, description, user_id, date FROM posts WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    result = result.fetchone()
    user_id = result[3]
    sql = "SELECT username FROM users WHERE id=:user_id"
    name = db.session.execute(text(sql), {"user_id":user_id})
    return (result, name.fetchone()[0])

def delete_post(id):
    sql = "SELECT username FROM posts WHERE id=:id"
    name = db.session.execute(text(sql), {"id":id}).fetchone()[0]
    if session["username"] != name:
        return 0
    sql = "DELETE FROM posts WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return