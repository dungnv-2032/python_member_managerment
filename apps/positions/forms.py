from django import forms
from .models import Position


class AddPositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['name', 'abbreviation']

    name = forms.CharField(min_length=4, max_length=200, required=True)
    abbreviation = forms.CharField(min_length=1, max_length=200, required=True)


