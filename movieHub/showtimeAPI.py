import requests
import json
from imdb import IMDb
import datetime

# sydney city id 7820
def get_showtimes(cinema_ids , movie_ids):
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/showtimes/",
            params={
                "country" : "AU",
                "countries" : "AU",
                "movie_id" : movie_ids,
                "cinema_id" : cinema_ids
            },
            headers={
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
        return loaded_json
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

# -33.939961, 151.22966
def get_theaters(curr_location , distance_to_search):
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/",
            params={
                "country" : "AU",
                "location" : curr_location,
                "distance" : distance_to_search
            },
            headers={
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return loaded_json

def get_movie(cinema_ids):
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/movies/",
            params={
                "countries" : "AU",
                "cinema_id" : cinema_ids                
            },
            headers={
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def getMovieInfo(imdb_id):
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/movies/",
            params={
                "countries" : "AU",
                "imdb_id" : imdb_id,
                "fields" : "genres,poster_image"
            },
            headers={
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
        return loaded_json
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_imdbId(movie_ids):
    rand = "https://api.internationalshowtimes.com/v4/movies/"
    try:
        response = requests.get(
            url = rand + movie_ids,
            params = {
            },
            headers = {
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
        return loaded_json
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

