from django import forms
from .models import Team


class AddTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'description', 'leader_id']

    name = forms.CharField(min_length=4, max_length=200, required=True)
    description = forms.CharField(max_length=1000, required=False)
    leader_id = forms.IntegerField(required=True)


