import os
import openai
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

#Database creation
db = SQL("sqlite:///project.db")

#sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def account():
    return render_template("account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return render_template("error.html", error_message="PLEASE DO NOT LEAVE ANY FIELDS BLANK")
        if not db.execute("SELECT * FROM accounts WHERE email=?", email):
            return render_template("error.html", error_message="THIS EMAIL ADDRESS IS NOT REGISTERED WITH DECIPHER")
        row = db.execute("SELECT * FROM accounts WHERE email =?",email)
        if not check_password_hash(row[0]["hashed_password"], password):
            return render_template("error.html", error_message="PASSWORD IS WRONG")
        session["user_id"] = row[0]["id"]
        return redirect("/explain")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat = request.form.get('repeat')

        if not name or not email or not password or not repeat:
            return render_template("error.html", error_message="PLEASE FILL IN ALL FIELDS")
        if password != repeat:
            return render_template("error.html", error_message="PASSWORDS DO NOT MATCH")

        hashed_pass = generate_password_hash(password)
        taken = db.execute("SELECT * FROM accounts WHERE email=?",email)
        if taken:
            return render_template("error.html", error_message="EMAIL ALREADY IN USE")
        else:
            db.execute("INSERT INTO accounts(name,email,hashed_password) VALUES(?,?,?)",name,email,hashed_pass)
        return redirect("/login")

@app.route("/explain", methods=["GET","POST"])
@login_required
def explain():
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("explain.html")
    else:
        openai.api_key = "ENTER YOUR OWN OPEN AI API KEY"
        code = request.form.get("pythonCode")
        if not code:
            return render_template("error.html", error_message="Please Enter Valid Code")
        if db.execute("SELECT * FROM history WHERE code=? AND user_id=?", code, user_id) == []:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="explain what the following python code does:  " + code,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            response = (response["choices"][0]["text"])
            db.execute("INSERT INTO history (code,explained,user_id) VALUES(?,?,?);", code, response, user_id)
            return render_template("explained.html", response=response)
        else:
            return render_template("error.html", error_message="Sorry, You Have Already Entered This, Go To History To View The Explanation.")

@app.route("/history", methods=["GET","POST"])
@login_required
def history():
    user_id = session["user_id"]
    if request.method == "GET":
        info = db.execute("SELECT * FROM history WHERE user_id=?", user_id)
        return render_template("history.html", info=info)






@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")







