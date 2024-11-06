from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import MysteryObjectForm
from .models import MysteryObject

def home(request):
    """
    View function for the home page, displays all mystery objects.
    """
    objects = MysteryObject.objects.all()  # Fetch all posted mystery objects
    return render(request, 'forum/home.html', {'objects': objects})

def register(request):
    """
    View function for user registration. Handles GET and POST requests.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Use Django's built-in user creation form
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Automatically log in the user
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()  # Create an empty form for GET requests
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    """
    View function for user login. Handles GET and POST requests.
    """
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username from POST request
        password = request.POST.get('password')  # Get password from POST request
        user = authenticate(request, username=username, password=password)  # Authenticate user
        
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home page after successful login
        else:
            return render(request, 'forum/login.html', {'error': 'Invalid credentials'})  # Handle unsuccessful attempt
    
    return render(request, 'forum/login.html')  # Render login page for GET requests

@login_required
def create_object_post(request):
    """
    View function to create a new mystery object post. Requires login.
    """
    if request.method == 'POST':
        form = MysteryObjectForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            object_post = form.save(commit=False)  # Create the object but don't save yet
            object_post.asker = request.user  # Associate the object with the logged-in user
            object_post.save()  # Save object to the database
            return redirect('home')  # Redirect to home page after creation
    else:
        form = MysteryObjectForm()  # Load an empty form for GET requests
    return render(request, 'forum/create_object_post.html', {'form': form})  # Render the form template

@login_required
def profile(request):
    """
    View function for the user's profile page. Requires login.
    """
    return render(request, 'forum/profile.html', {'user': request.user})  # Render the profile page with user information
