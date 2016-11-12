import requests

API_TOKEN = '3a56894826a35368f1dbabf033f5c428'
QUERY_URL = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s'


class Movie:
    def __init__(self, title):
        self.title = title
        self.poster = ""
        self.vote = 0
        self.overview = ""

    def __str__(self):
        return "%s" % self.title

    def __repr__(self):
        return self.__str__()


def _get_movie_result(query):
    url = QUERY_URL % (API_TOKEN, query)
    print "query url %s " % url

    r = requests.get(url)

    results = r.json()['results']

    if len(results) == 0:
        print "movie %s not found on themoviedb" % query
        return None

    return results[0]


def get_movies(movies_to_query):
    movies_found = []

    for movie in movies_to_query:

        movie_result = _get_movie_result(movie.title())

        if movie_result is None:
            continue

        movie_found = Movie(movie_result['title'])
        movie_found.poster = "http://image.tmdb.org/t/p" + movie_result['poster_path']
        movie_found.vote = movie_result['vote_average']
        movie_found.overview = movie_result['overview']

        movies_found.append(movie_found)

    return movies_found
