from django import forms
from django import forms
from django.forms.widgets import Textarea, HiddenInput, Input

from posts.models import Post, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description', 'image')
        widgets = {
            'description': Textarea(attrs={
                'rows': 3,
                'cols': 80,
                'placeholder': 'Опишите публикацию',
                'class': 'border-0 border-top',
                'style': 'padding-right: 150px; outline:0px none transparent; overflow:auto; resize:none',
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': Textarea(attrs={
                'rows': 4,
                'cols': 50,
                'placeholder': 'Добавьте комментарий',
                'class': 'border-0 border-top',
                'style': 'padding-right: 150px; outline:0px none transparent; overflow:auto; resize:none',
            })
        }

