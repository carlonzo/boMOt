#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  # import sys package, if not already imported

reload(sys)
sys.setdefaultencoding('utf-8')

import moviemap

common_movies = []


def add_movie_liked(query):
    list_suggestions = moviemap.get_movie_list(query)

    if len(list_suggestions) == 0:
        return 0

    list_suggestions = moviemap.enhance_movie_list(list_suggestions)
    common_movies.extend(list_suggestions)

    return len(list_suggestions)




add_movie_liked("xmen")
add_movie_liked("the lion king")

print common_movies
print len(common_movies)
