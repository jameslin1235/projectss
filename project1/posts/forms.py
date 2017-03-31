from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
        "title",
        "content",
        "category"
        ]

    def clean(self, *args, **kwargs):
        error_list = []
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        print(self.cleaned_data)
        # if title == 'money':
        #     a = forms.ValidationError("use a different title")
        #     error_list.append(a)
        # if "honey" in title:
        #     b = forms.ValidationError("wrong title")
        #     error_list.append(b)
        # if "pc" in content:
        #     c = forms.ValidationError("wrong content")
        #     error_list.append(c)
        if error_list:
            raise forms.ValidationError(error_list)
        return super(PostForm, self).clean(*args, **kwargs)
