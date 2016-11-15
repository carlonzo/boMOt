#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import sys

reload(sys)
sys.path.insert(0, os.path.abspath("../"))  # base folder is one folder up
sys.setdefaultencoding('utf-8')

import moviemap
import themoviedb
from bot.models import MovieSuggest


def _list_movie_suggestion(query_list):
    common_movies = set([])

    for query in query_list:
        list_suggestions = moviemap.get_movie_list(query)

        if len(list_suggestions) == 0:
            continue

        list_suggestions = moviemap.enhance_movie_list(list_suggestions)

        print ("movielist for %s : %s" % (query, len(list_suggestions)))
        if len(common_movies) == 0:
            common_movies = set(list_suggestions)
        else:
            common_movies = common_movies.intersection(list_suggestions)
        print ("intersection for %s : %s" % (query, len(common_movies)))

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
    while movie == None:

        if len(movie_titles) == 0:
            break
        
        title = movie_titles[0]
        movie = themoviedb.get_movie(title)

        del movie_titles[0]

    list_titles_string = ','.join([str(x) for x in movie_titles])
    modelMovieDB = MovieSuggest(user_id=user_id, movies=list_titles_string)
    modelMovieDB.save()

    return movie


if __name__ == '__main__':
    generate_suggestions("abc", ["x men", "the lion king", "cinderella"])

    print get_next_suggestion("abc")
    print get_next_suggestion("abc")
    print get_next_suggestion("abc")
