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
## This is where we want to redirect users for the game result
@app.route("/<game_date>")
def success(game_date):
    if game_date in stats.quiz:
        #return json.dumps(stats.quiz[game_date][0]["score"])
        return render_template("postmaker.html", games = stats.quiz[game_date][0]) 
    elif game_date == "all":
        return json.dumps(stats.quiz)
    else:
        return json.dumps(stats.quiz["no_game"])

# This is a landing point for users (a start)
@app.route("/") # user can land at "/"
@app.route("/start") # or user can land at "/start"
def start():
    return render_template("postmaker.html") # look for templates/postmaker.html
# This is where postmaker.html POSTs data to
# A user could also browser (GET) to this location
@app.route("/login", methods = ["POST", "GET"])

def login():
    # POST would likely come from a user interacting with postmaker.html
    if request.method == "POST":
        if request.form.get("nm"): # if nm was assigned via the POST
            user = request.form.get("nm") # grab the value of nm from the POST
        else: # if a user sent a post without nm then assign value defaultuser
            user = "No world cup 2022 game was played on this date."
    # GET would likely come from a user interacting with a browser
    elif request.method == "GET":
        if request.args.get("nm"): # if nm was assigned as a parameter=value
            user = request.args.get("nm") # pull nm from localhost:5060/login?nm=larry
        else: # if nm was not passed...
            user = "defaultuser" # ...then user is just defaultuser
    return redirect(url_for("success", game_date = user)) # pass back to /success with val for name


def give_stat():
    #player level and guesses player used counter
    exit = ""
    level = 0
    guess = 0

    os.system("cls")
    ##While loop for see if user pressed 1 to exit or level is complete
    while (exit != "1" and level < len(stats.quiz) and guess <2):
        try:    
            print(stats.quiz[level].get("question"))
            i = 1
            for x in stats.quiz[level].get("choice"):
                print("\t", i, ".", x)
                i +=1
            response = input("Choose 1, 2, 3 or 4: ")
            if response.isdigit() == False:
                print("Wrong input. Please choose from the given options. ")
                continue
        except ValueError as NoCharactersAccepted:
            print("Please enter a number! ")
        
        

        #While loop to see if the user selected the correct answer
        while (guess<2):
            if response == stats.quiz[level].get("correct_answer"):
                if level == len(stats.quiz)-1:
                    level += 1
                    print("Congrats! You won the game! Level ", level, " passed!")
                    break
                level += 1
                guess = 0
                print("You guessed right. Level ", level, "passed. ")
                break
            elif guess == 1:
                guess +=1
                print("GAME OVER! TRY AGAIN!  ")
                break
            else:
                response = input("You guessed wrong!!! Last chance!! Please choose again: ")
                guess +=1
                continue
                
        
    exit = print("-----THE END----- ")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224) # runs the application