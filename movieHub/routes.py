from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from login import _dbselect, check_password, check_user
import sqlite3
from server import app
from sqlite3 import Error
from imdb import IMDb

@app.route('/', methods=["GET", "POST"])
def index():
    ia = IMDb()
    movies = ia.search_movie('Avengers: Infinity War')
    print(movies)
    return render_template("index.html", movies=movies)
