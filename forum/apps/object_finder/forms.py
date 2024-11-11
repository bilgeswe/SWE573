from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author', 'date_posted', 'comments', 'images', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter post content', 'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'images':
                if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                    field.widget.attrs.setdefault('class', 'form-control')
                elif isinstance(field.widget, (forms.SelectMultiple, forms.Select)):
                    field.widget.attrs.setdefault('class', 'form-select')

