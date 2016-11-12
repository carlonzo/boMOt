#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  # import sys package, if not already imported

import moviemap
import themoviedb
from bot.models import MovieSuggest

reload(sys)
sys.setdefaultencoding('utf-8')


def _list_movie_suggestion(query_list):
    common_movies = set([])

    for query in query_list:
        list_suggestions = moviemap.get_movie_list(query)

        if len(list_suggestions) == 0:
            continue

        list_suggestions = moviemap.enhance_movie_list(list_suggestions)

        common_movies = common_movies.union(list_suggestions)

    return common_movies


def generate_suggestions(user_id, query_list):
    list_suggestions = _list_movie_suggestion(query_list)

    list_titles = []
    index = 0
    for movie_sugg in list_suggestions:
        if index >= 20:
            break
        list_titles.append(movie_sugg.title)
        index += 1

    list_titles_string = ','.join([str(x) for x in list_titles])

    modelMovieDB = MovieSuggest(user_id=user_id, movies=list_titles_string)
    modelMovieDB.save()


def get_next_suggestion(user_id):
    modelMovieDB = MovieSuggest.objects.get(user_id=user_id)

    movie_titles = modelMovieDB.get_movies()

    movie = None
    for i in range(len(movie_titles)):
        title = movie_titles[i]
        movie = themoviedb.get_movie(title)

        if movie is None:
            continue

        movie_titles = movie_titles[i:]

    list_titles_string = ','.join([str(x) for x in movie_titles])
    modelMovieDB = MovieSuggest(user_id=user_id, movies=list_titles_string)
    modelMovieDB.save()

    return movie


if __name__ == '__main__':
    generate_suggestions("abc", ["x men", "the lion king", "cinderella"])

    print get_next_suggestion("abc")
    print get_next_suggestion("abc")
    print get_next_suggestion("abc")
