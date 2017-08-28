from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]


    #
    # def clean_email(self):
    #         data = self.cleaned_data['email']
    #         if "fred@example.com" not in data:
    #             raise forms.ValidationError("You have forgotten about Fred!")
    #
    #         # Always return a value to use as the new cleaned data, even if
    #         # this method didn't change it.
    #         return data
