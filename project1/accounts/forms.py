from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
        "email",
        "email2",
        "username",
        "password",
        ]

    # def clean_email(self):
    #
    #     error_list = []
    #     email = self.cleaned_data.get('email')
    #
    #     db_email = User.objects.filter(email=email)
    #     if db_email.exists():
    #         a = forms.ValidationError("This email is already registered.")
    #         error_list.append(a)
    #
    #     if error_list:
    #         raise forms.ValidationError(error_list)
    #     return email



    def clean(self, *args, **kwargs):
        error_list = []
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        print(self.cleaned_data)
        if email != email2:
            a = forms.ValidationError("Emails must match.")
            error_list.append(a)
        db_email = User.objects.filter(email=email)

        if db_email.exists():
            b = forms.ValidationError("This email is already registered.")
            error_list.append(b)
        if error_list:
            raise forms.ValidationError(error_list)

        return super(RegisterForm, self).clean(*args, **kwargs)
