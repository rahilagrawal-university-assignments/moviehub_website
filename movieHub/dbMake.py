from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie"
    imdb_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    poster = Column(String(250), nullable=True)

class Cinema(Base):
    __tablename__ = "cinema"
    cinema_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Plays(Base):
    __tablename__ = "plays"
    plays_id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey("cinema.cinema_id"), nullable=False)
    imdb_id = Column(Integer, ForeignKey("movie.imdb_id"), nullable=False)

class Showtime(Base):
    __tablename__ = "showtime"
    showtime_id = Column(Integer, primary_key=True)
    time = Column(String(100), nullable=False)

class Time(Base):
    __tablename__ = "time"
    time_id = Column(Integer, primary_key=True)
    showtime_id = Column(Integer, ForeignKey("showtime.showtime_id"), nullable=False)
    cinema_id = Column(Integer, ForeignKey("cinema.cinema_id"), nullable=False)
    imdb_id = Column(Integer, ForeignKey("movie.imdb_id"), nullable=False)

def addMovie(session, name, poster):
    new_movie = Movie(name=name, poster=poster)
    session.add(new_movie)
    session.commit()

def addCinema(session, name):
    new_cinema = Cinema(name=name)
    session.add(new_cinema)
    session.commit()

def addPlays(session, imdb_id, cinema_id):
    new_plays = Plays(imdb_id=imdb_id, cinema_id=cinema_id)
    session.add(new_plays)
    session.commit()

def addShowtime(session, time):
    new_showtime = Showtime(time=time)
    session.add(new_showtime)
    session.commit()

def addTime(session, imdb_id, cinema_id, showtime_id):
    new_time = Time(imdb_id=imdb_id, cinema_id=cinema_id, showtime_id=showtime_id)
    session.add(new_time)
    session.commit()

engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

session = DBSession()


addMovie(session, "Avengers: Infinity War", "http://image.tmdb.org/t/p/w154/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg")
addMovie(session, "Rampage", "http://image.tmdb.org/t/p/w154/30oXQKwibh0uANGMs0Sytw3uN22.jpg")
addMovie(session, "A Quiet Place", "http://image.tmdb.org/t/p/w154/mrepRTUhNKU70PFf7LNQypbkH00.jpg")
addMovie(session, "Ready Player One", "http://image.tmdb.org/t/p/w154/pU1ULUq8D3iRxl1fdX2lZIzdHuI.jpg")
addMovie(session, "I Feel Pretty", "http://image.tmdb.org/t/p/w154/bZe6x2fKtwVDsAvZQ9fnIJznBrc.jpg")

addCinema(session, "Events Parramatta")

results = session.query(Movie).filter_by(name="Avengers: Infinity War").all()

movie = results[0]
# or u can use a for loop like this:
# for row in results:
#   do something with row eg, row.imdb_id, row.name

results = session.query(Cinema).filter_by(name="Events Parramatta").all()

cinema = results[0]

addPlays(session, movie.imdb_id, cinema.cinema_id)

addShowtime(session, "10.00 am")

results = session.query(Showtime).filter_by(time="10.00 am").all()

shows = results[0]

addTime(session, movie.imdb_id, cinema.cinema_id, shows.showtime_id)
