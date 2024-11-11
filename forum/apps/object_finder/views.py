from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    return render(request, 'object_finder/profile.html')


def index(request):
    posts = Post.objects.all()
    return render(request, 'object_finder/index.html', {'posts': posts})


@login_required
def form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

    else:
        form = PostForm()

    return render(request, 'object_finder/form.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
