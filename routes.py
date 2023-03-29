from app import app
import users
import topics
import posts
import comments
from flask import render_template, request, session, redirect
from sqlalchemy import text

@app.route("/")
def index():
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"] 
    list = topics.all_topics()
    return render_template("index.html", error=error, topics=list)

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

@app.route("/createtopic")
def createtopic():
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    return render_template("createtopic.html", error=error)

@app.route("/topiccheck", methods=["POST"])
def topiccheck():
    name = request.form["name"]
    description = request.form["description"]
    result = topics.create_topic(name, description, session["username"])
    if result == 0:
        return redirect("/createtopic")
    return redirect("/")

@app.route("/<string:name>")
def topic(name):
    id = topics.get_topic_id(name)
    list = posts.topicposts(id)
    return render_template("posts.html", list=list, topicname=name)

@app.route("/<string:name>/createpost")
def createpost(name):
    topic_id = topics.get_topic_id(name)
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    return render_template("createpost.html", topic_id=topic_id, error=error)

@app.route("/addpost", methods=["POST"])
def addpost():
    topic_id = request.form["topic_id"]
    name = request.form["Title"]
    description = request.form["Text"]
    username = session["username"]
    topic_name = posts.create_post(topic_id, username, name, description)
    page = "/" + topic_name
    if "errormessage" in session:
        return redirect(page + "/createpost")
    return redirect(page)


@app.route("/<string:topic>/<int:id>")
def post(topic, id):
    contents = posts.get_post(id)
    answers = comments.postcomments(id)
    post = contents[0]
    name = contents[1]
    return render_template("post.html", post=post, name=name, topicname=topic, answers=answers, topic=topic)

@app.route("/<string:topic>/<int:id>/comment")
def comment(topic, id):
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    post_url = request.base_url.replace("/comment", "")
    contents = posts.get_post(id)
    post = contents[0]
    name = contents[1]
    return render_template("comment.html", post=post, name=name, topicname=topic, post_url=post_url, post_id=id, error=error)

@app.route("/addcomment", methods=["POST"])
def addcomment():
    post_url = request.form["post_url"]
    post_id = request.form["post_id"]
    content = request.form["comment"]
    username = session["username"]

    result = comments.createcomment(post_id, username, content)

    if result == 0:
        page = post_url + "/comment"
        return redirect(page)
    else:
        return redirect(post_url)