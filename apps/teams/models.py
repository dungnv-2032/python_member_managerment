from django.db import models

from apps.users.models import CreatedUpdatedBase


class Team(CreatedUpdatedBase):
    class Meta:
        db_table = 'team'

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    leader = models.IntegerField()
    user = models.ManyToManyField('users.User', blank=True, related_name='team_user')

    def __str__(self):
        return self.name
