from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbFunctions import *
import datetime

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie"
    imdb_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    poster = Column(String(250), nullable=True)
    is_showing = Column(Boolean, default=True)

class Cinema(Base):
    __tablename__ = "cinema"
    cinema_id = Column(Integer, primary_key=True , autoincrement=False)
    name = Column(String(100), nullable=False)

class Plays(Base):
    __tablename__ = "plays"
    plays_id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey("cinema.cinema_id"), nullable=False)
    imdb_id = Column(Integer, ForeignKey("movie.imdb_id"), nullable=False)

# class Showtime(Base):
#     __tablename__ = "showtime"
#     showtime_id = Column(Integer, primary_key=True)
#     time = Column(String(100), nullable=False)

class Time(Base):
    __tablename__ = "time"
    time_id = Column(Integer, primary_key=True)
    showtime = Column(String(100), nullable=False)
    cinema_id = Column(Integer, ForeignKey("cinema.cinema_id"), nullable=False)
    imdb_id = Column(Integer, ForeignKey("movie.imdb_id"), nullable=False)

class User(Base):
    __tablename__ = "users"
    username = Column(String(100), primary_key=True, autoincrement=False)
    password = Column(String(100), nullable=False)

def addMovie(session, id, name, poster, is_showing):
    new_movie = Movie(imdb_id=id, name=name, poster=poster, is_showing=is_showing)
    session.add(new_movie)
    session.commit()

def addCinema(session, name_C , id_c):
    new_cinema = Cinema(cinema_id=id_c , name=name_C)
    session.add(new_cinema)
    session.commit()

def addPlays(session, imdb_id, cinema_id):
    new_plays = Plays(imdb_id=imdb_id, cinema_id=cinema_id)
    session.add(new_plays)
    session.commit()

# def addShowtime(session, time):
#     new_showtime = Showtime(time=time)
#     session.add(new_showtime)
#     session.commit()

def addTime(session, imdb_id, cinema_id, show_time):
    new_time = Time(imdb_id=imdb_id, cinema_id=cinema_id, showtime=show_time)
    session.add(new_time)
    session.commit()

def addUser(session, username, password):
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()


# this will add all the theaters supplied using the parameteres into the session 
def addall_theaters(session ,listof_theaters):
    for i in range(0, len(listof_theaters["cinemas"])):
         # print("%s " % (listof_theaters["cinemas"][i]["name"]) , (listof_theaters["cinemas"][i]["id"]))
         addCinema(session , listof_theaters["cinemas"][i]["name"] , (listof_theaters["cinemas"][i]["id"]))

#this will add all the movies supplied into the session depending on if it is upcoming or not 
def addall_movies(session , listof_movies , includes_upcoming):
    for i in range(0, len(listof_movies["movies"])):
        addMovie(session , 
        int(get_imdbId(listof_movies["movies"][i]["id"])),
        listof_movies["movies"][i]["title"] ,
        listof_movies["movies"][i]["poster_image_thumbnail"] , includes_upcoming)

#this will add all the showtimes and the times of the movies into the session 
def addall_times(session , listof_times):
    for i in range(0 , len(listof_times)["showtimes"]):
        addTime(session , int(get_imdbId(len(listof_times["showtimes"][i]["movie_id"]))),
            int(len(listof_times["showtimes"][i]["cinema_id"]))  , len(listof_times["showtimes"][i]["start_at"]))
#goes through all the cinemas in the database and 
def addall_plays(session):
    theaters = session.query(Cinema).filter_by(id>0).all
    for Cinema in theaters:
       listof_movies =  get_movie(str(Cinema.cinema_id))
       for i in range(0,len(listof_movies["movies"])):
            addPlays(session ,int(get_imdbId(listof_movies["movies"][i]["movie_id"])) ,Cinema.cinema_id)



engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

session = DBSession()
#for upcomingdates
date = datetime.date.today() + datetime.timedelta(days=7)

#add Cinemas
#the arguments location , distance 
addall_theaters(session , get_theaters("-33.939961, 151.22966" , 5))
#add Movies 
#arguments you can add a theater_id to make it precise
addall_movies(session , get_movie("") , False);
addall_movies(session , get_all_upcoming(date))
#add showtimes
#arguments you can use cinema id or movie id aswell to make it more specific
addall_times(session , get_Showtimes("" , ""))
addall_plays(session)

#



# addMovie(session, 4154756, "Avengers: Infinity War", "http://image.tmdb.org/t/p/w154/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg", True)
# addMovie(session, 2231461, "Rampage", "http://image.tmdb.org/t/p/w154/30oXQKwibh0uANGMs0Sytw3uN22.jpg", True)
# addMovie(session, 6644200, "A Quiet Place", "http://image.tmdb.org/t/p/w154/mrepRTUhNKU70PFf7LNQypbkH00.jpg", True)
# addMovie(session, 1677720, "Ready Player One", "http://image.tmdb.org/t/p/w154/pU1ULUq8D3iRxl1fdX2lZIzdHuI.jpg", False)
# addMovie(session, 6791096, "I Feel Pretty", "http://image.tmdb.org/t/p/w154/bZe6x2fKtwVDsAvZQ9fnIJznBrc.jpg", False)

# addCinema(session, "Events Parramatta")

# results = session.query(Movie).filter_by(name="Avengers: Infinity War").all()

# movie = results[0]
# # or u can use a for loop like this:
# # for row in results:
# #   do something with row eg, row.imdb_id, row.name

# results = session.query(Cinema).filter_by(name="Events Parramatta").all()

# cinema = results[0]

# addPlays(session, movie.imdb_id, cinema.cinema_id)

# addShowtime(session, "10.00 am")

# results = session.query(Showtime).filter_by(time="10.00 am").all()

# shows = results[0]

# addTime(session, movie.imdb_id, cinema.cinema_id, shows.showtime_id)

# addUser(session, "aditya", "aditya")
