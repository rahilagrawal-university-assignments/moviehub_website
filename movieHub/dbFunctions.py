from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbMake import Movie, Cinema, Showtime, Plays, Time

engine = create_engine('sqlite:///movies.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def movieQuery(name):
    if name is None:
        return session.query(Movie).all()

    return session.query(Movie).filter_by(name=name).all()

