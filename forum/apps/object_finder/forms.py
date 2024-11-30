from .models import Comment
from django.forms import formset_factory
from django import forms
from .models import Post, AttributeName


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


class AttributeForm(forms.Form):
    attribute_name = forms.ModelChoiceField(
        queryset=AttributeName.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    value = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


AttributeFormSet = formset_factory(AttributeForm, extra=1, can_delete=True)


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
