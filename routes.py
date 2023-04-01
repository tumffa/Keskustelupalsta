from app import app
import users
import topics
import posts
import comments
from flask import render_template, request, session, redirect
from sqlalchemy import text

@app.route("/")
def index():
    try:
        if "username" in session:
            logged_in = 1
        else:
            logged_in = 0
    except:
        logged_in = 0

    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"] 
    list = topics.all_topics()
    return render_template("index.html", error=error, topics=list, logged_in=logged_in)

@app.route("/logincheck", methods=["POST"])
def logincheck():
    username = request.form["username"]
    password = request.form["password"]
    users.check_login(username, password)
    return redirect("/")

def check_user():
    try:
        if "username" not in session:
            return 0
        else:
            return
    except:
        return 0

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
    del session["csrf_token"]
    return redirect("/")

@app.route("/createtopic")
def createtopic():
    if check_user() == 0:
        return redirect("/")
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    return render_template("createtopic.html", error=error)

@app.route("/topiccheck", methods=["POST"])
def topiccheck():
    if check_user() == 0:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        session["errormessage"] = "Invalid CSRF token"
        return redirect("/createtopic")
    name = request.form["name"]
    description = request.form["description"]
    result = topics.create_topic(name, description, session["username"])
    if result == 0:
        return redirect("/createtopic")
    return redirect("/")

@app.route("/topics/<string:name>")
def topic(name):
    if check_user() == 0:
        return redirect("/")
    id = topics.get_topic_id(name)
    list = posts.topicposts(id)
    owner_name = topics.get_topic_owner(id)
    return render_template("posts.html", list=list, topicname=name, id=id, owner_name=owner_name)

@app.route("/topics/<string:name>/createpost")
def createpost(name):
    if check_user() == 0:
        return redirect("/")
    topic_id = topics.get_topic_id(name)
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    return render_template("createpost.html", topic_id=topic_id, topicname=name, error=error)

@app.route("/addpost", methods=["POST"])
def addpost():
    topic_name = request.form["topic_name"]
    page = "/topics/" + topic_name
    if check_user() == 0:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        session["errormessage"] = "Invalid CSRF token"
        return redirect(page + "/createpost")
    topic_id = request.form["topic_id"]
    name = request.form["Title"]
    description = request.form["Text"]
    username = session["username"]
    topic_name = posts.create_post(topic_id, username, name, description)
    if "errormessage" in session:
        return redirect(page + "/createpost")
    return redirect(page)


@app.route("/topics/<string:topic>/<int:id>")
def post(topic, id):
    if check_user() == 0:
        return redirect("/")
    contents = posts.get_post(id)
    answers = comments.postcomments(id)
    session["url"] = request.base_url
    post = contents[0]
    name = contents[1]
    return render_template("post.html", post=post, name=name, topicname=topic, answers=answers, topic=topic)

@app.route("/topics/<string:topic>/<int:id>/comment")
def comment(topic, id):
    if check_user() == 0:
        return redirect("/")
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
    page = post_url + "/comment"
    if check_user() == 0:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        session["errormessage"] = "Invalid CSRF token"
        return redirect(page)
    post_id = request.form["post_id"]
    content = request.form["comment"]
    username = session["username"]

    result = comments.createcomment(post_id, username, content)

    if result == 0:
        return redirect(page)
    else:
        return redirect(post_url)

@app.route("/topics/<string:topic>/<int:post_id>/<int:comment_id>/respond")
def respond(topic, post_id, comment_id):
    if check_user() == 0:
        return redirect("/")
    error = ""
    if "errormessage" in session:
        error = session["errormessage"]
        del session["errormessage"]
    post_url = request.base_url
    content = comments.comment_and_responses(comment_id)
    return render_template("respond_to_comment.html", comment_id=comment_id, comment=content[0], responses=content[1], topicname=topic, post_url=post_url, post_id=post_id, error=error)

@app.route("/addresponse", methods=["POST"])
def addresponse():
    post_url = request.form["post_url"]
    if check_user() == 0:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        session["errormessage"] = "Invalid CSRF token"
        return redirect(post_url)
    comment_id = request.form["comment_id"]
    content = request.form["response"]
    username = session["username"]

    result = comments.createresponse(comment_id, username, content)

    if result == 0:
        return redirect(post_url)
    else:
        index = len(("/" + str(comment_id) + "/respond"))
        post_url = post_url[:len(post_url) - index]
        return redirect(post_url)
    
@app.route("/delete/<string:type>/<int:id>")
def delete(type, id):
    if check_user() == 0:
        return redirect("/")
    return render_template("commitdelete.html", type=type, id=id)

@app.route("/commitdelete", methods=["POST"])
def commitdelete():
    if check_user() == 0:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        session["errormessage"] = "Invalid CSRF token"
        return "Permission denied"
    type = request.form["type"]
    id = request.form["id"]
    if type == "response":
        result = comments.delete_response(id)
    if type == "comment":
        result = comments.delete_comment(id)
    if type == "post":
        result = posts.delete_post(id)
    if type == "topic":
        result = topics.delete_topic(id)

    if result == 0:
        return "Permission denied"
    if type == "topic":
        return redirect("/")
    elif type == "post":
        length = len(session["url"])
        session["url"] = session["url"][:length - len(str(id))-1]
    return redirect(session["url"])