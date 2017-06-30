from django.forms import ModelForm
from django import forms
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "gender",
            "credential",
            "description",
            "residence",
            "occupation",
            "position",
            "company",
            "school",
            "major"
        ]

    def clean_position(self):
        data = self.cleaned_data['position']
        if data:
            if "kevin@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Kevin!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_company(self):
        data = self.cleaned_data['company']
        if data:
            if "jack@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Jack!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_school(self):
        data = self.cleaned_data['school']
        if data:
            if "edward@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Edward!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_major(self):
        data = self.cleaned_data['major']
        if data:
            if "fred@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

class ProfileAvatarForm(forms.Form):
     avatar_dataurl = forms.CharField()
     avatar_filename = forms.CharField()


class ProfileBackgroundForm(forms.Form):
    background_dataurl = forms.CharField()
    background_filename = forms.CharField()
