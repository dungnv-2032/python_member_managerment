from django.db import models

from apps.users.models import CreatedUpdatedBase
from apps.users.models import User


class Team(CreatedUpdatedBase):
    class Meta:
        db_table = 'team'

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000, null=True)
    leader_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name
