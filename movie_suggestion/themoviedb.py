import requests

API_TOKEN = '3a56894826a35368f1dbabf033f5c428'
QUERY_URL = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s'
MOVIE_URL = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=en-US'


class Movie:
    def __init__(self, title):
        self.title = title
        self.poster = ""
        self.vote = 0
        self.overview = ""
        self.link = ""

    def __str__(self):
        return "%s" % self.title

    def __repr__(self):
        return self.__str__()


def _search_movie(query):
    url = QUERY_URL % (API_TOKEN, query)
    print "query url %s " % url

    r = requests.get(url)

    results = r.json()['results']

    if len(results) == 0:
        print "movie %s not found on themoviedb" % query
        return None

    return results[0]


def _retrieve_movie(id_movie):
    url = MOVIE_URL % (id_movie, API_TOKEN)
    print "movie url %s " % url

    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.json()


def get_movie(title_query):
    search_result = _search_movie(title_query)

    if search_result is None:
        return None

    movie_result = _retrieve_movie(search_result['id'])

    if movie_result is None:
        return None

    movie_found = Movie(movie_result['title'])
    movie_found.poster = "http://image.tmdb.org/t/p/w300/" + movie_result['poster_path']
    movie_found.vote = movie_result['vote_average']
    movie_found.overview = movie_result['overview']
    movie_found.link = "http://www.imdb.com/title/%s/" % movie_result['imdb_id']

    return movie_found


print get_movie("x men")
