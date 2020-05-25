from django.db import models
from django.contrib.contenttypes.models import ContentType
from apps.users.models import CreatedUpdatedBase


class Position(CreatedUpdatedBase):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=200)

    class Meta:
        db_table = 'position'

    def __str__(self):
        return self.name
