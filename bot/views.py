import json
import threading
import urllib
import uuid
import apiai as apiai
from django.utils.termcolors import background
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bot.models import UserPrefs
from movie_suggestion import suggestor

ACCESS_TOKEN = "EAAS3evVdTA4BABt7fQZARCQA8Qz0jrO3YObjc5sgACTZC6XhdaJpkVsRB59b5lrpfIB1TZA1bkHGiARJagyZA4SAEajanRimbl1RC5WeAmnvQrmX4t6I6R5ghZCNc9duZALdagDuKenMCDdIBJUuHhTkujkztddiq0cG0Kh1ZAgNQZDZD"

API_AI_ACCESS_TOKEN = "81265a838d6a40b0a086e9b84cb6d67e"

session_id = None


def send_generic_template(user_id, movie_url, movie_name, movie_image_url, movie_description):
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": movie_name,
                        "item_url": movie_url,
                        "image_url": movie_image_url,
                        "subtitle": movie_description,
                        "buttons": [{
                            "type": "web_url",
                            "url": movie_url,
                            "title": "Watch"
                        }, {
                            "type": "postback",
                            "title": "Something else",
                            "payload": "NEXT_SUGGESTION"
                        }]
                    }]
                }
            }
        }
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def send_message(message, user_id):
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message
        }
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def get_ai_api_response(message, session_id):
    ai = apiai.ApiAI(API_AI_ACCESS_TOKEN)
    request = ai.text_request()
    request.query = message
    request.session_id = session_id
    return json.loads(request.getresponse().read())


def check_if_reset(message, user_prefs):
    if message == "bomotreset":
        user_prefs.fav_movies = ""
        user_prefs.apiai_session_id = uuid.uuid4().hex


def fetch_suggestion_and_show_to_user(user_id, user_prefs):
    download_thread = threading.Thread(target=fetch_movies, args=[user_id, user_prefs])
    download_thread.start()


def fetch_movies(user_id, user_prefs):
    send_message("This might take up to 20 seconds.", user_id)
    t = threading.Timer(6.0, send_message, args=["Almost there", user_id])
    t = threading.Timer(12.0, send_message, args=["A bit more :)", user_id])
    t.start()

    movies = suggestor.get_movies(user_prefs.get_movies())
    movie_name = movies[0].title
    movie_url = "https://www.justwatch.com/us/search?q=" + urllib.quote_plus(movie_name)
    movie_image_url = movies[0].poster
    movie_description = movies[0].overview
    send_generic_template(user_id, movie_url, movie_name, movie_image_url, movie_description)


@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        hub_challenge = request.GET.get('hub.challenge')
        if hub_challenge is not None:
            return HttpResponse(hub_challenge)
        else:
            return HttpResponse("Failed validation. Make sure the validation tokens match.", status=403)

    elif request.method == 'POST':
        data = json.loads(request.body.decode(encoding='UTF-8'))
        if data is None:
            return HttpResponse("Data don't exist", status=404)

        print(data)

        messaging = data['entry'][0]['messaging'][0]
        if "sender" in messaging:
            user_id = messaging['sender']['id']
        else:
            return HttpResponse("Missing sender id", status=404)

        try:
            user_prefs = UserPrefs.objects.get(user_id=user_id)
        except UserPrefs.DoesNotExist:
            user_prefs = UserPrefs(user_id=user_id)

        if "message" in messaging:
            message = messaging['message']['text']

            check_if_reset(message, user_prefs)

            response = get_ai_api_response(message, user_prefs.apiai_session_id)
            result = response["result"]
            parameters = result["parameters"]
            speech_response = result["fulfillment"]["speech"]
            user_prefs.apiai_session_id = response["sessionId"]

            if "movie" in parameters:
                movie = parameters["movie"]
                movie = movie.strip()
                if not user_prefs.fav_movies:
                    user_prefs.fav_movies = movie
                else:
                    user_prefs.fav_movies = user_prefs.fav_movies + "," + movie

            user_prefs.save()

            send_message(speech_response, user_id)

            if result["action"] == "fetch-movie-suggestion":
                fetch_suggestion_and_show_to_user(user_id, user_prefs)

        else:
            if "postback" in messaging:
                is_next_suggestion = messaging['postback']['payload'] == "NEXT_SUGGESTION"
                if is_next_suggestion:
                    fetch_suggestion_and_show_to_user(user_id, user_prefs)

        return HttpResponse("Gotcha", status=200)
