from .models import Comment
from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False, help_text='Optional.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'form-control'
            }),
        }



class CommentForm(forms.ModelForm):
    anonymous_name = forms.CharField(
        max_length=255, required=False, label='Your Name (optional)')

    class Meta:
        model = Comment
        fields = ['content', 'anonymous_name']

    content = forms.CharField(
        widget=forms.Textarea(attrs={
                              'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your comment here...'}),
        label='',
    )

    def __init__(self, *args, **kwargs):
        user_authenticated = kwargs.pop('user_authenticated', False)
        super(CommentForm, self).__init__(*args, **kwargs)
        if user_authenticated:
            self.fields.pop('anonymous_name', None)
