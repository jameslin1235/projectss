from django.forms import ModelForm, RadioSelect
from .models import Profile
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_gender",
            "profile_credential",
            "profile_description",
            "profile_residence",
            "profile_occupation",
            "profile_position",
            "profile_company",
            "profile_school",
            "profile_major",
        ]



    def clean_profile_major(self):
        print(self.cleaned_data)
        data = self.cleaned_data['profile_major']

        # if data.isspace():
        #     print('x')
        #     raise forms.ValidationError("This field contains only whitespace.")
        # if data.isdigit():
        #     print('isdigit')

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

class ProfileAvatarForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]

class ProfileBackgroundForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "background",
        ]
