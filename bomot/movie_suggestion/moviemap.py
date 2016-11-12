#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  # import sys package, if not already imported

reload(sys)
sys.setdefaultencoding('utf-8')

from urlparse import urljoin

import requests
from lxml import html


class Movie:
    def __init__(self, title, relative_link):
        self.title = title
        self.link = self.resolve_relative_link(relative_link)

    def title(self):
        return self.title

    def link(self):
        return self.link

    def __str__(self):
        return "%s - %s" % (self.title, self.link)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    @staticmethod
    def resolve_relative_link(relative_link):
        if relative_link == "":
            return None
        else:
            return urljoin("http://www.movie-map.com/", relative_link)


def _get_movie_result_from_url(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    gnodmaps = tree.xpath('//*[@id="gnodMap"]')

    if len(gnodmaps) == 0:
        return []

    movie_elements = gnodmaps[0].getchildren()

    list_movie = []
    for movie_elem in movie_elements:
        link = movie_elem.get("href")

        if "http://www.gnovies.com/discussion/" in link:
            link = ""

        movie = Movie(movie_elem.text, link)
        list_movie.append(movie)

    return list_movie


def get_movie_list(query):
    list_movie = _get_movie_result_from_url('http://www.movie-map.com/map-search.php?legacy=0&f=%s' % query)

    return list_movie


def enhance_movie_list(movie_list):
    newlist = []

    count = 0
    for movie in movie_list:

        if count >= 6:
            break

        if movie.link is None:
            continue

        other_movie = _get_movie_result_from_url(movie.link)
        newlist.extend(other_movie)
        count += 1

    return set(newlist)


if __name__ == '__main__':
    listm = get_movie_list("x man")

    enhanced_list = enhance_movie_list(listm)

    print len(listm)
    print len(enhanced_list)
