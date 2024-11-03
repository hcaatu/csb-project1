from flask import redirect, render_template, abort, request, session
#from werkzeug.security import check_password_hash
from secrets import token_hex
from app import app
import db_access

def check_user():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
    except KeyError:
        return abort(403)
    
def clear_error_messages():
    session["passwords_differ"] = False
    session["username_in_use"] = False
    session["registration_successful"] = False

@app.route("/")
def index():
    clear_error_messages()
    messages = db_access.get_messages()
    return render_template("index.html", count=len(messages), messages=messages)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        if password != password_again:
            session["passwords_differ"] = True
            return redirect("/register")
        if db_access.register_new(username, password):
            clear_error_messages()
            session["registration_successful"] = True
            return redirect("/")
        elif not db_access.register_new(username, password):
            session["username_in_use"] = True
            return redirect("/register")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = db_access.fetch_user(username)

    if not user:
        session["invalid_user"] = True
        return redirect(request.referrer)
    else:
        # hash = user.password
        # if check_password_hash(hash, password):
        if password == user.password:
            session["user_id"] = user.id
            session["username"] = username
            session["admin"] = user.admin
            session["invalid_user"] = False
            session["csrf_token"] = token_hex(16)
        else:
            session["invalid_user"] = True
            return redirect(request.referrer)
    return redirect(request.referrer)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["admin"]
    del session["invalid_user"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/admin_page")
def admin():
    clear_error_messages()
    messages = db_access.get_messages()
    users = db_access.get_users_by_query("")
    return render_template("admin.html", messages=messages, users=users)

@app.route("/create", methods=["POST"])
def create():
    check_user()
    content = request.form["content"]
    if session["username"]:
        db_access.create_message(content, session["username"])
    return redirect("/")

@app.route("/result")
def result():
    query = request.args["query"]
    messages = db_access.fetch_messages(query)
    return render_template("result.html", messages=messages)

@app.route("/personal")
def personal(id=None):
    #check_user()
    print(session["username"])
    messages = db_access.fetch_messages_by_user(session["username"])
    print(messages)
    return render_template("personal.html", messages=messages)

@app.route("/delete_message/<int:id>", methods=["POST"])
def delete_message(id):
    db_access.delete_message(id)
    return redirect("/personal")

@app.route("/users", methods=["GET"])
def users():
    #check_user()
    if request.method == "GET":
        query = request.args["query"]
        users = db_access.get_users_by_query(query)
        count = len(users)
        return render_template("users.html", users=users, count=count)
    

@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    check_user()
    db_access.delete_user(id)
    return redirect(request.referrer)

