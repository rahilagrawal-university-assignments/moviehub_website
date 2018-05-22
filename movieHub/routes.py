from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from login import loginUser
import sqlite3
from server import app
from sqlite3 import Error
import imdb
from dbFunctions import *

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    
    nowShowing = movieQuery(None, None, True)
    comingSoon = movieQuery(None, None, False)
    return render_template("indexU.html", nowShowing=nowShowing[8:14], comingSoon=comingSoon[0:6])


@app.route('/login', methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        try:
            if request.form["searchText"]:
                searchText = request.form["searchText"]
                return redirect(url_for('search', searchText=searchText))
        except:
            username = str(request.form["username"])
            password = str(request.form["password"])
            
            if loginUser(username, password):
                return redirect(url_for("index"))
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("loginU.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/payment', methods=["GET" , "POST"])
def payment():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    cinema = request.args.get("cinema")
    time = request.args.get("time")
    movie = request.args.get("movie")
    return render_template("paymentU.html", cinema=cinema, time=time, movie=movie)

@app.route('/movies', methods=["GET" , "POST"])
def movies():
    movies = movieQuery(None, None, None)
    genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
                "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror", "Music", "Musical", 
                "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", "Thriller", "War", "Western"]
    
    if request.method == "POST":
        try:
            if request.form["searchText"]:
                searchText = request.form["searchText"]
                return redirect(url_for('search', searchText=searchText))
        except:
            genresSelected = request.form.getlist("genre")
            is_showing = request.form.getlist("is_showing")
            print(is_showing)
            if is_showing:
                if is_showing[0] == "nowShowing":
                    movies = movieQuery(None, None, True)
                else:
                    movies = movieQuery(None, None, False)

            updateMovies = []
            for movie in movies:
                for i in movie.genres.split():
                    print(i)
                    if i in genresSelected and movie not in updateMovies:
                        updateMovies.append(movie)
            print(updateMovies)
            if not updateMovies:
                updateMovies = movies
            return render_template("moviesU.html", movies=updateMovies, genres=genres)

   
    return render_template("moviesU.html", movies=movies, genres=genres)

@app.route('/moviedetail', methods=["GET" , "POST"])
def moviedetail():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))

    ia = imdb.IMDb()
    imdb_id = request.args.get("id")

    moviedb = movieQuery(None, imdb_id, None)
    moviedb = moviedb[0]

    movie = ia.get_movie(imdb_id)
    ia.update(movie)
    
    cinemaList = []
    timesList = timeQuery(imdb_id)
    
    for i in timesList:
        cinema = cinemaQuery(i.cinema_id)
        if cinema[0] not in cinemaList:
            cinemaList.append(cinema[0])

    return render_template("moviedetailU.html", movie=movie, moviedb=moviedb, cinemas=cinemaList, times=timesList)

@app.route('/signup', methods=["GET" , "POST"])
def signup():
    if request.method == "POST":
        try:
            if request.form["searchText"]:
                searchText = request.form["searchText"]
                return redirect(url_for('search', searchText=searchText))
        except:
            username = str(request.form["username"])
            password = str(request.form["password"])
            firstName = str(request.form["firstName"])
            lastName = str(request.form["lastName"])
            if newUser(username, password, firstName, lastName):
                return redirect(url_for("index"))

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("signupU.html")

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    searchText = request.args.get("searchText")
    movies = searchQuery(searchText)
    if not movies:
        return render_template("searchU.html", searchText=searchText, movies=movies, not_found=1)    
    return render_template("searchU.html", searchText=searchText, movies=movies, not_found=0)

