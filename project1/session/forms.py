from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SessionForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super(SessionForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            # Only do something if both fields are valid so far.
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("This user does not exist.")
            
