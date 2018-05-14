from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from login import loginUser
import sqlite3
from server import app
from sqlite3 import Error
from imdb import IMDb
from dbFunctions import *

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    
    nowShowing = movieQuery(None, True)
    comingSoon = movieQuery(None, False)
    return render_template("index.html", nowShowing=nowShowing[0:5], comingSoon=comingSoon[0:5])


# @app.route('/movie', methods=["GET" , "POST"])
# def movie():
#     ia = IMDb()
#     imdb_id = request.args.get("id")
    
#     movie = ia.get_movie(imdb_id)
#     ia.update(movie)
    
#     cinema_ids = playsQuery(imdb_id)
#     cinemaList = []
#     timesObj = []
#     for i in cinema_ids:
#         cinemaList.append(cinemaQuery(i.cinema_id))
#         timesObj.append(timeQuery(i.cinema_id, imdb_id))

#     times = []
#     for obj in timesObj:
#         for i in obj:
#             times.append(showtimesQuery(i.showtime_id))

#     return render_template("movie.html", movie=movie, cinemas=cinemaList, times=times)


@app.route('/login', methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
        username = str(request.form["username"])
        password = str(request.form["password"])

        if loginUser(username, password):
            return redirect(url_for("index"))

    return render_template("login.html")
'''
Created by : Rahil Agrawal
Modified by : Aditya Karia
Created At : 11/5/18
Mock Functions for testing links
Can be modified by Backend Devs
'''
@app.route('/payment', methods=["GET" , "POST"])
def payment():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
        numChild = request.form["child"]
        numStudent = request.form["student"]
        numAdult = request.form["adult"]
        numPensioner = request.form["pensioner"]
        name = request.form["name"]
        number = request.form["number"]
        expiry = request.form["expiry_date"]
        ccv = request.form["CCV"]
        return render_template("payment_successful.html")
    return render_template("payment.html")

@app.route('/movies', methods=["GET" , "POST"])
def movies():
    movies = movieQuery(None, None)
    genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
                "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror", "Music", "Musical", 
                "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", "Thriller", "War", "Western"]
    
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
        genresSelected = request.form.getlist("genre")
        
        updateMovies = []
        for movie in movies:
            for i in movie.genres.split():
                print(i)
                if i in genresSelected and movie not in updateMovies:
                    updateMovies.append(movie)
        print(updateMovies)
        return render_template("movies.html", movies=updateMovies, genres=genres)

   
    return render_template("movies.html", movies=movies, genres=genres)

@app.route('/moviedetail', methods=["GET" , "POST"])
def moviedetail():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    ia = IMDb()
    imdb_id = request.args.get("id")

    movie = ia.get_movie(imdb_id)
    ia.update(movie)
    
    # cinema_ids = playsQuery(imdb_id)
    # cinemaList = []
    # timesObj = []
    # for i in cinema_ids:
    #     cinemaList.append(cinemaQuery(i.cinema_id))
    #     timesObj.append(timeQuery(i.cinema_id, imdb_id))

    # times = []
    # for obj in timesObj:
    #     for i in obj:
    #         times.append(showtimesQuery(i.showtime_id))
    return render_template("moviedetail.html", movie=movie, cinemas=cinemaList, times=times)

@app.route('/signup', methods=["GET" , "POST"])
def signup():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
        username = str(request.form["username"])
        password = str(request.form["password"])

        if newUser(username, password):
            return redirect(url_for("index"))
    return render_template("signup.html")

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if request.form["searchText"]:
            searchText = request.form["searchText"]
            return redirect(url_for('search', searchText=searchText))
    searchText = request.args.get("searchText")
    movies = searchQuery(searchText)
    return render_template("search.html", searchText=searchText, movies=movies)

