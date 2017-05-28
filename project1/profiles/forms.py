from django.forms import ModelForm, RadioSelect
from .models import Profile

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
        widgets = {
            'profile_gender': RadioSelect(),
        }
