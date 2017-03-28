from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):

    email2 = forms.EmailField()
    # password = forms.CharField(widget=forms.PasswordInput, help_text='Use at least 8 characters.')


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

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     print(self.cleaned_data)
    #     return username



    def clean(self, *args, **kwargs):
        error_list = []
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        password = self.cleaned_data.get('password')
        print(self.cleaned_data)
        if email != email2:
            a = forms.ValidationError("Emails must match.")
            error_list.append(a)
        # db_email = User.objects.filter(email=email)
        # if db_email.exists():
        #     b = forms.ValidationError("This email is already registered.")
        #     error_list.append(b)
        # if len(password) < 8:
        #     c = forms.ValidationError("The password is too short.")
        #     error_list.append(c)
        if error_list:
            raise forms.ValidationError(error_list)

        return super(RegisterForm, self).clean(*args, **kwargs)
