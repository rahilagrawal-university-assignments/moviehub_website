import requests
import json
from imdb import IMDb

# sydney city id 7820
def send_request():
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/",
            params={
                "country": "AU",
                "location": "-33.9, 151.2",
                "distance" : 50
            },
            headers={
                "X-API-Key": "jSaZYUE0VbpaOAUawsBmScBjQjXB5Vd8",
            },
        )
        json_data = response.text
        loaded_json = json.loads(json_data)
        for i in range(0, len(loaded_json["cinemas"])):
            print("%s" % (loaded_json["cinemas"][i]["name"]))
        # print('Response HTTP Status Code: {status_code}\n'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}\n'.format(
        #     content=response.content))
        # print(response.text)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

send_request()

