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

    def clean_profile_position(self):
        data = self.cleaned_data['profile_position']
        if data:
            if "kevin@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Kevin!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_profile_company(self):
        data = self.cleaned_data['profile_company']
        if data:
            if "jack@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Jack!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_profile_school(self):
        data = self.cleaned_data['profile_school']
        if data:
            if "edward@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Edward!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean_profile_major(self):
        data = self.cleaned_data['profile_major']
        if data:
            if "fred@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data




# class ProfileAvatarForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = [
#             "avatar",
#         ]

# class ProfileBackgroundForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = [
#             "background",
#         ]

class ProfileAvatarForm(forms.Form):
    profile_avatar = forms.CharField()
