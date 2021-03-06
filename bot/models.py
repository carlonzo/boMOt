import uuid

from django.db import models


class UserPrefs(models.Model):
    user_id = models.CharField(max_length=500, blank=False, null=False)
    apiai_session_id = models.CharField(max_length=500, blank=True, null=True, default=uuid.uuid4().hex)
    fav_movies = models.CharField(max_length=500, blank=True, null=True)

    def get_movies(self):
        return self.fav_movies.split(",")

    def __str__(self):
        return self.user_id


class MovieSuggest(models.Model):
    movies = models.CharField(max_length=50000, blank=False, null=False)
    user_id = models.CharField(primary_key=True, max_length=500, blank=False, null=False)

    def __str__(self):
        return self.user_id

    def get_movies(self):
        return self.movies.split(",")
