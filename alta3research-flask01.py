#!/usr/bin/python3

import stats
import os
import jinja2
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import jsonify
from flask import json

app = Flask(__name__)

# This is a landing point for users (a start)
@app.route("/") # user can land at "/"
def main():
    return render_template("index.html")

## This is where we want to redirect users for the game result data
@app.route("/<game_date>")
def success(game_date):
    if game_date in stats.quiz:
        #return json.dumps(stats.quiz[game_date])
        return render_template("index.html", games = stats.quiz[game_date], game_date = game_date) 
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

# This is a landing point for users (a start)
@app.route("/getdata/alldata") # user can land at "/"
def index():
    # jsonify returns legal JSON
    return jsonify(stats.quiz)

@app.route("/getdata/<user_date>") # user can land at "/"
def get_data(user_date):
    if user_date in stats.quiz:
        # jsonify returns legal JSON
        return jsonify(stats.quiz[user_date])
    else:
        return "No FIFA games found. Please choose another value. "

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224) # runs the application