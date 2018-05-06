from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from login import _dbselect, check_password, check_user
import sqlite3
from server import app
from sqlite3 import Error
from imdb import IMDb
from dbFunctions import movieQuery

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imdb_id = request.form["id"]
        return redirect(url_for('movie', id=imdb_id))
    ia = IMDb()
    movies = movieQuery(None)
    return render_template("index.html", movies=movies)


@app.route('/movie', methods=["GET" , "POST"])
def movie():
    ia = IMDb()
    movie = ia.get_movie(request.args.get("id"))
    ia.update(movie)
    return render_template("movie.html", movie=movie)

