import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from .models import Post, Tag
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'object_finder/profile.html', {'user_posts': user_posts})


@login_required
def index(request):
    posts = Post.objects.all().order_by('-date_posted')[0:10]
    return render(request, 'object_finder/index.html', {'posts': posts})


@login_required
def form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content_delta = request.POST.get('content_delta', None)
            # Get tags data from hidden input
            tags_data = request.POST.get('tags', '[]')

            if content_delta:
                try:
                    content_delta = json.loads(content_delta)
                    # Parse the JSON string of tags
                    tags = json.loads(tags_data)
                except json.JSONDecodeError:
                    form.add_error(None, 'Invalid content or tags data.')
                    return render(request, 'object_finder/form.html', {'form': form})

                post = form.save(commit=False)
                post.author = request.user
                post.content_delta = content_delta
                post.save()

                # Process and save tags
                for tag_data in tags:
                    tag_id = tag_data.get('id')
                    tag_label = tag_data.get('label')

                    # Retrieve or create the tag
                    tag, created = Tag.objects.get_or_create(
                        tag_id=tag_id,
                        name=tag_label
                    )
                    post.tags.add(tag)

                return redirect('/')
            else:
                form.add_error(None, 'Content is required.')
    else:
        form = PostForm()
    return render(request, 'object_finder/form.html', {'form': form})


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('view_post', post_id=post.id)
    else:
        comment_form = CommentForm()

    # Get all comments for this post
    comments = post.comments.all().order_by('date_posted')

    # Get tags associated with the post
    tags = post.tags.all()

    return render(request, 'object_finder/view_post.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'tags': tags,
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
