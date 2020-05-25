from django.db import models

from apps.users.models import CreatedUpdatedBase


class Skill(CreatedUpdatedBase):
    class Meta:
        db_table = 'skill'

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
    used_year_number = models.IntegerField()
    user = models.ManyToManyField('users.User', blank=True)

    def __str__(self):
        return self.name
