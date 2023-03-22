from app import app
from db import db
from topics import get_topic_id
from sqlalchemy import text
from flask import session

def topicposts(id):
    sql = "SELECT name, description FROM posts WHERE topic_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchall()

def create_post(topic_id, username, name, description):
    sql = "SELECT name FROM topics WHERE id=:id"
    result = db.session.execute(text(sql), {"id":topic_id})
    topic_name = result.fetchone()[0]

    if len(name) < 1:
        session["errormessage"] = "Post title has to be atleast 1 character long"
        return topic_name
    
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user_id = result.fetchone()[0]

    sql = "INSERT INTO posts (topic_id, user_id, name, description) VALUES (:topic_id, :user_id, :name, :description)"
    db.session.execute(text(sql), {"topic_id":topic_id, "user_id":user_id, "name":name, "description":description})
    db.session.commit()
    return topic_name