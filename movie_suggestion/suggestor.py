#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  # import sys package, if not already imported

import moviemap
import themoviedb

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


def get_movies(query_list):
    list_suggestions = _list_movie_suggestion(query_list)

    list_titles = []
    index = 0
    for movie_sugg in list_suggestions:
        if index >= 1:
            break
        list_titles.append(movie_sugg.title)
        index += 1

    return themoviedb.get_movies(list_titles)


# listm = get_movies(["x men", "the lion king", "cinderella"])

# print listm
