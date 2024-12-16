import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, SignUpForm
from .models import Post, Tag, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def update_is_solved(request, post_id, comment_id):
    """Updates the solved status of a comment on a post"""
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id)
            if request.user != post.author:
                return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

            comment = get_object_or_404(Comment, id=comment_id)
            is_solved = not comment.is_solved
            post.comments.update(is_solved=False)
            comment.is_solved = is_solved
            comment.save()

            comments = post.comments.all().order_by('-date_posted')
            return render(request, 'object_finder/comments.html', {'comments': comments, 'post': post})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)


def profile_view(request, user_id):
    """Displays posts by a specific user"""
    user_posts = Post.objects.filter(author__id=user_id)
    return render(request, 'object_finder/profile.html', {'user_posts': user_posts})


def index(request):
    """Displays the 10 most recent posts"""
    posts = Post.objects.all().order_by('-date_posted')[0:10]
    return render(request, 'object_finder/index.html', {'view_name': 'Recent Discussions', 'posts': posts})


@login_required
def search_posts(request):
    """Searches posts based on query and attributes"""
    query = request.GET.get('q', '').strip()

    attributes = {}
    for key, value in request.GET.items():
        if key.startswith('attribute_') and value.strip():
            attribute_name = key[len('attribute_'):]
            attr_value = value.strip()

            unit_name = f'unit_{attribute_name}'
            unit_value = request.GET.get(unit_name, "").strip()

            attributes[attribute_name] = {
                'value': attr_value,
                'unit': unit_value
            }

    has_query_condition = False
    has_attribute_condition = False

    posts = Post.objects.all()

    if query:
        query_condition = Q(title__icontains=query) | Q(
            tags__name__icontains=query)
        posts = posts.filter(query_condition)
        has_query_condition = True

    if attributes:
        filtered_posts = []
        for p in posts:
            match_all = True
            for attr_id, attr_data in attributes.items():
                search_val = attr_data['value']
                search_unit = attr_data['unit']

                attribute_data = p.attributes.get(attr_id, {})
                if not bool(attribute_data):
                    match_all = False
                    break

                db_val = attribute_data.get("value", "")
                db_unit = attribute_data.get("unit", "")

                if search_val.lower() not in db_val.lower():
                    match_all = False
                    break

                if search_unit and search_unit != db_unit:
                    match_all = False
                    break

            if match_all:
                filtered_posts.append(p)
        posts = filtered_posts
        has_attribute_condition = True

    if not has_query_condition and not has_attribute_condition:
        posts = Post.objects.none()

    posts = sorted(posts, key=lambda x: x.date_posted, reverse=True)

    return render(request, 'object_finder/index.html', {
        'view_name': 'Search Results',
        'posts': posts,
        'query': query
    })


@login_required
def form(request):
    """Handles creation of new posts"""
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            content_delta = request.POST.get('content_delta', None)
            tags_data = request.POST.get('tags', '[]')

            if content_delta:
                try:
                    content_delta = json.loads(content_delta)
                    tags = json.loads(tags_data)
                except json.JSONDecodeError:
                    form.add_error(None, 'Invalid content or tags data.')
                    return render(request, 'object_finder/form.html', {
                        'form': form,
                    })

                # Check if post contains at least one image
                contains_image = False
                for op in content_delta.get('ops', []):
                    insert_content = op.get('insert', {})
                    if isinstance(insert_content, dict) and 'image' in insert_content:
                        contains_image = True
                        break

                if not contains_image:
                    form.add_error(
                        None, 'You must include at least one image in the content.')
                    return render(request, 'object_finder/form.html', {
                        'form': form,
                    })

                # Process attributes
                attributes = {}
                for key, value in request.POST.items():
                    if key.startswith('attribute_'):
                        attribute_name = key[len('attribute_'):]
                        if value.strip():
                            attributes[attribute_name] = {
                                'value': value.strip()}

                            unit_name = f'unit_{attribute_name}'
                            unit_value = request.POST.get(unit_name, None)
                            if unit_value:
                                attributes[attribute_name]['unit'] = unit_value

                post.attributes = attributes
                post.author = request.user
                post.content_delta = content_delta
                post.save()

                # Process tags
                for tag_data in tags:
                    tag_id = tag_data.get('id')
                    tag_label = tag_data.get('label')

                    tag, created = Tag.objects.get_or_create(
                        tag_id=tag_id,
                        name=tag_label
                    )
                    post.tags.add(tag)

                return redirect('/')
            else:
                form.add_error(None, 'Content is required.')
            return render(request, 'object_finder/form.html', {
                'form': form,
            })
    return render(request, 'object_finder/form.html', {
        'form': form,
    })


def view_post(request, post_id):
    """Displays a single post and handles comment submission"""
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        comment_form = CommentForm(user_authenticated=True)
    else:
        comment_form = CommentForm(user_authenticated=False)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'comment_form':
            if request.user.is_authenticated:
                comment_form = CommentForm(
                    request.POST, user_authenticated=True)
            else:
                comment_form = CommentForm(
                    request.POST, user_authenticated=False)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post

                if request.user.is_authenticated:
                    post_as_anonymous = 'post_as_anonymous' in request.POST
                    if post_as_anonymous:
                        # User chose to post anonymously
                        comment.author = None
                    else:
                        comment.author = request.user
                else:
                    # Anonymous user
                    comment.author = None
                    comment.anonymous_name = comment_form.cleaned_data.get(
                        'anonymous_name')

                comment.save()
                return redirect('view_post', post_id=post.id)

    comments = post.comments.all().order_by('-date_posted')
    tags = post.tags.all()
    attribute_names = post.attributes
    is_solved = any([comment.is_solved for comment in comments])

    return render(request, 'object_finder/view_post.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'tags': tags,
        'attribute_names': attribute_names,
        'is_solved': is_solved
    })

def signup_view(request):
    """Handles user registration"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name') 
            user.last_name = form.cleaned_data.get('last_name')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
