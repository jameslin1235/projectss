from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
        "position",
        "company",
        "school",
        "concentration",
        "degree_type",
        "avatar",
        ]
