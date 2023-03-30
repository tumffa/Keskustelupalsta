from app import app
from db import db
from sqlalchemy import text
from flask import session

def all_topics():
    sql = "SELECT name, description FROM topics"
    result = db.session.execute(text(sql))
    return result.fetchall()

def create_topic(name, description, username):
    sql = "SELECT 1 FROM topics WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    exists = result.fetchone()
    if exists:
        session["errormessage"] = "Topic with this name already exists"
        return 0
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    id = result.fetchone()[0]
    sql = "INSERT INTO topics (name, description, owner_id) VALUES (:name, :description, :owner_id)"
    db.session.execute(text(sql), {"name":name, "description":description, "owner_id":id})
    db.session.commit()
    return 1

def get_topic_id(name):
    sql = "SELECT id FROM topics WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    return result.fetchone()[0]

def get_topic_owner(id):
    if id == 1:
        return ""
    sql = "SELECT owner_id FROM topics WHERE id=:id"
    owner_id = db.session.execute(text(sql), {"id":id}).fetchone()[0]
    sql ="SELECT username FROM users WHERE id=:id"
    return db.session.execute(text(sql), {"id":owner_id}).fetchone()[0]

def delete_topic(id):
    sql = "SELECT owner_id FROM topics WHERE id=:id"
    owner_id = db.session.execute(text(sql), {"id":id}).fetchone()[0]
    sql = "SELECT username FROM users WHERE id=:id"
    name = db.session.execute(text(sql), {"id":owner_id}).fetchone()[0]
    if session["username"] != name:
        return 0
    sql = "DELETE FROM topics WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return