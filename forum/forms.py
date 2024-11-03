from django import forms                                            # form handling module
from django.contrib.auth.models import User                         # User model for authentication
from .models import ObjectPost                                      # Import the ObjectPost model from the current app's models

class ObjectPostForm(forms.ModelForm):                              # Define a new form class based on the ObjectPost model
    class Meta:                                                     # Meta class for providing metadata to the form
        model = ObjectPost                                          # Specify that this form is associated with the ObjectPost model
        fields = ['title', 'description', 'tags']                   # Define which fields to include in the form

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)          # Define a password field with a password input widget to mask the input
    class Meta:                                                     # Define meta class to specify model and fields for the form
        model = User                                                # Specify that this form is based on the User model
        fields = ['username', 'email', 'password']                  # Fields to include in the form

    def save(self, commit=True):
        user = super().save(commit=False)                           # Create a new User instance but do not save it to the database yet
        
        user.set_password(self.cleaned_data['password'])            # Set the user's password, hashing it for security
        if commit:                                                  # If commit there is a commit, save the user instance to the database
            user.save()                                             # This actually saves the user to the database
        return user                                                 # Return the user instance
