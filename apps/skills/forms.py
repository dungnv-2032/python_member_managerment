from django import forms
from .models import Skill


class AddSkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ['name', 'level', 'used_year_number']

    name = forms.CharField(min_length=4, max_length=200, required=True)
    level = forms.IntegerField(max_value=100, required=True)
    used_year_number = forms.IntegerField(max_value=50, required=True)


