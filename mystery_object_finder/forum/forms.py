from django import forms
from .models import MysteryObject

class MysteryObjectForm(forms.ModelForm):
    class Meta:
        model = MysteryObject
        fields = [
            'material', 'size', 'color', 'shape', 
            'weight', 'description', 'location',
            'time_period', 'smell', 'taste',
            'texture', 'hardness', 'pattern',
            'brand', 'print', 'image', 'functionality'
        ]
        widgets = {
            'material': forms.TextInput(attrs={'placeholder': 'Enter material type'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the object'}),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),                                
            # Allow multiple file uploads
        }
        help_texts = {
            'material': 'What is the material of the object?',
            'size': 'What is the size of the object?',
            'location': 'Where was the object found?',
            # Add help texts laterrrrr
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight
