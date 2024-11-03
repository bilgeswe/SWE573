from django.shortcuts import render, redirect               # Functions for rendering templates and redirecting users
from django.contrib.auth import login, authenticate         # Functions for user authentication and session management
from .forms import UserRegistrationForm                     # Importing the custom registration form created earlier
from .forms import ObjectPostForm                           # Import the ObjectPostForm from the forms module in the same app

def home(request):
    return render(request, 'forum/home.html')               # This will render a home page template

def register(request):
    if request.method == 'POST':                            # Check if the request method is POST, indicating form submission
        form = UserRegistrationForm(request.POST)           # Create a UserRegistrationForm instance with the submitted data
        
        if form.is_valid():                                 # Check if the form is valid (e.g., fields are filled out correctly)
            user = form.save()                              # Save the new user instance from the form data
            login(request, user)                            # Log the user in after registration
            return redirect('home')                         # Redirect the user to the home page (or another view)

    else:
        form = UserRegistrationForm()                       # If the request method is not POST, create an empty form
    
    return render(request, 'forum/register.html', {'form': form})       # Render the registration template with the form context

def user_login(request):
    if request.method == 'POST':                            # View function for user login
        username = request.POST['username']                 # Check if the request method is POST, indicating form submission
        password = request.POST['password']                 # Retrieve the username and password from the submitted form

        user = authenticate(request, username=username, password=password)         # Authenticate the user with the provided credentials
        
        if user is not None:                                        # If authentication is successful (user is found)
            login(request, user)                                    # Log the user in
            return redirect('home')                                 # Redirect the user to the home page (or another view)
        else:
            # If authentication fails, render the login page with an error message
            return render(request, 'forum/login.html', {'error': 'Invalid credentials'})

    
    # If the request method is not POST, render the login page without any error
    return render(request, 'forum/login.html')

def create_object_post(request):                                # Define a view function to handle the creation of an ObjectPost
    if request.method == 'POST':                                # Check if the request method is POST (i.e., form submission)
        form = ObjectPostForm(request.POST)                     # Instantiate the form with the submitted data
        if form.is_valid():                                     # Check if the form data is valid
            form.save()                                         # Save the valid form data as a new ObjectPost instance in the database
            return redirect('home')                             # Redirect to the 'home' view after successful creation
    else:                                                       # If the request method is not POST (i.e., a GET request)
        form = ObjectPostForm()                                 # Instantiate an empty form for the user to fill out
    return render(request, 'forum/create_object_post.html', {'form': form})  # Render the form template with the form context
