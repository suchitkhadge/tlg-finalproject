#!/usr/bin/env python3

import stats
from flask import Flask
from flask import session
from flask import make_response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.secret_key = "any random string"

# create a limiter object from Limiter
# limits are being performed by tracking the
# REMOTE ADDRESS of the clients
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# entry point for our users
# login.html points to /home
@app.route("/")
def signin():
    if "username" in session:
        user = session["username"]
        return render_template("index.html", userID = user)
    else:
        return render_template("signin.html")

@app.route("/logout")
def signout():
    session.pop("username", None)
    return render_template("signin.html")

# set the cookie and send it back to the user
@app.route("/home", methods = ["POST", "GET"])
def setcookie():
    # if user generates a POST to our API
    if request.method == "POST":
        if request.form.get("nm"): # if nm was assigned via the POST
        #if request.form["nm"] <-- this also works, but returns ERROR if no nm
            user = request.form.get("nm") # grab the value of nm from the POST
            session["username"] = user
        else: # if a user sent a post without nm then assign value defaultuser
            user = "defaultuser"
        
        # Note that cookies are set on response objects.
        # Since you normally just return strings
        # Flask will convert them into response objects for you
        resp = make_response(render_template("index.html", userID = user))
        # add a cookie to our response object
                        #cookievar #value
        resp.set_cookie("userID", user)

        # return our response object includes our cookie
        return resp
        
    if request.method == "GET": # if the user sends a GET
        return redirect(url_for("index")) # redirect to index

def getcookie():
    # attempt to read the value of userID from user cookie
    name = request.cookies.get("userID") # preferred method
    
    # name = request.cookies["userID"] # <-- this works but returns error
                                       # if value userID is not in cookie
    
    # return HTML embedded with name (value of userID read from cookie) 
    return render_template("index.html", userID = name)

# Get the result for the particular date and render in HTML
@app.route("/<game_date>")
def success(game_date):
    name = request.cookies.get("userID")
    if game_date in stats.quiz:
        #return json.dumps(stats.quiz[game_date])
        return render_template("index.html", games = stats.quiz[game_date], game_date = game_date, userID = name) 
    elif game_date == "all":
        return render_template("index.html", data = stats.quiz)
    else:
        return render_template("index.html", games = stats.quiz["no_game"])

@app.route("/login", methods = ["POST", "GET"])
def login():
    # POST would likely come from a user interacting with index.html
    if request.method == "POST":
        if request.form.get("nm"): # if nm was assigned via the POST
            user_input = request.form.get("nm") # grab the value of nm from the POST
        else: # if a user sent a post without nm then assign value defaultuser
            user_input = "all"
    # GET would likely come from a user interacting with a browser
    elif request.method == "GET":
        if request.args.get("nm"): # if nm was assigned as a parameter=value
            user_input = request.args.get("nm") # pull nm from localhost:5060/login?nm=larry
        else: # if nm was not passed...
            user_input = "all" # ...then no results shown
    return redirect(url_for("success", game_date = user_input)) # pass back to /success with val for name

#Get all data in JSON format
@app.route("/getdata/alldata") # user can land at "/"
@limiter.limit("10 per day")
def index():
    # jsonify returns legal JSON
    return jsonify(stats.quiz)

#Get the game data for the particular date in JSON format
@app.route("/getdata/<user_date>") # user can land at "/"
@limiter.limit("10 per day")
def get_data(user_date):
    if user_date in stats.quiz:
        # jsonify returns legal JSON
        return jsonify(stats.quiz[user_date])
    else:
        return "No FIFA games found. Please choose another value. "

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224)
