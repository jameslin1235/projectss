from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
        "gender",
        "profile_credential",
        "residence",
        "occupation",
        "position",
        "company",
        "school",
        "major",
        ]
