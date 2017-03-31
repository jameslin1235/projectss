from django import forms
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()

class RegisterForm(forms.ModelForm):

    email2 = forms.EmailField()

    class Meta:
        model = User
        fields = [
        "email",
        "email2",
        "username",
        "password",
        ]
        widgets = {
            'password': forms.PasswordInput,
        }
        help_texts = {
            'password': ('Use at least 8 characters.'),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self, *args, **kwargs):

        cleaned_data =  super(RegisterForm, self).clean()
        print(cleaned_data)
        error_list = []
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        if email and email2:
            if email != email2:
                b = forms.ValidationError("Emails must match.")
                error_list.append(b)
        if error_list:
            raise forms.ValidationError(error_list)
        return cleaned_data
