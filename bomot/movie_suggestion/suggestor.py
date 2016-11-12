#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  # import sys package, if not already imported

reload(sys)
sys.setdefaultencoding('utf-8')

import moviemap


def list_movie(query_list):
    common_movies = set([])

    for query in query_list:
        list_suggestions = moviemap.get_movie_list(query)

        if len(list_suggestions) == 0:
            continue

        list_suggestions = moviemap.enhance_movie_list(list_suggestions)

        common_movies = common_movies.union(list_suggestions)

    return len(common_movies)


listm = list_movie(["x men", "the lion king", "cinderella"])

print listm
