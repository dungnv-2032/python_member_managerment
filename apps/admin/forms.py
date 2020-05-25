from django import forms


class AdminLoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=200)
    password = forms.CharField(min_length=6, max_length=200)


