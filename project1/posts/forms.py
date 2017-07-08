from django import forms
from .models import Post
from project1.project1.topics.models import Topic
class PostForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), empty_label="Select a topic")
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "topic"
        ]


    # def clean(self, *args, **kwargs):
    #     error_list = []
    #     title = self.cleaned_data.get('title')
    #     content = self.cleaned_data.get('content')
    #     print(self.cleaned_data)
    #     # if title == 'money':
    #     #     a = forms.ValidationError("use a different title")
    #     #     error_list.append(a)
    #     # if "honey" in title:
    #     #     b = forms.ValidationError("wrong title")
    #     #     error_list.append(b)
    #     # if "pc" in content:
    #     #     c = forms.ValidationError("wrong content")
    #     #     error_list.append(c)
    #     if error_list:
    #         raise forms.ValidationError(error_list)
    #     return super(PostForm, self).clean(*args, **kwargs)
