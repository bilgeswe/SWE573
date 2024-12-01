import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from .models import Post, Tag, AttributeName, AttributeValue
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.http import JsonResponse


@login_required
def update_is_solved(request, post_id):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id)
            if request.user != post.author:
                return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

            data = json.loads(request.body)
            is_solved = data.get('is_solved', False)
            post.is_solved = is_solved
            post.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)


def profile_view(request, user_id):
    user_posts = Post.objects.filter(author__id=user_id)
    attribute_names = AttributeName.objects.all()
    return render(request, 'object_finder/profile.html', {'user_posts': user_posts, 'attribute_names': attribute_names})


def index(request):
    attribute_names = AttributeName.objects.all()
    posts = Post.objects.all().order_by('-date_posted')[0:10]
    return render(request, 'object_finder/index.html', {'view_name': 'Recent Discussions', 'posts': posts, 'attribute_names': attribute_names})


def search_posts(request):
    query = request.GET.get('q', '').strip()

    attributes = {}
    for key, value in request.GET.items():
        match = re.match(r'^attributes\[(\d+)\]$', key)
        if match and value.strip():
            attr_id = match.group(1)
            attributes[attr_id] = value.strip()

    has_query_condition = False
    has_attribute_condition = False

    posts = Post.objects.all()

    if query:
        query_condition = Q(title__icontains=query) | Q(
            tags__name__icontains=query)
        posts = posts.filter(query_condition)
        has_query_condition = True

    if attributes:
        for attr_id, value in attributes.items():
            posts = posts.filter(
                attributes__attribute_name__id=attr_id,
                attributes__value__icontains=value
            )
        has_attribute_condition = True

    if not has_query_condition and not has_attribute_condition:
        posts = Post.objects.none()

    posts = posts.distinct().order_by('-date_posted')

    attribute_names = AttributeName.objects.all()

    return render(request, 'object_finder/index.html', {
        'view_name': 'Search Results',
        'posts': posts,
        'attribute_names': attribute_names,
        'query': query
    })


@login_required
def form(request):
    attribute_names = AttributeName.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
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
                        'attribute_names': attribute_names
                    })

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
                        'attribute_names': attribute_names
                    })

                post = form.save(commit=False)
                post.author = request.user
                post.content_delta = content_delta
                post.save()

                for tag_data in tags:
                    tag_id = tag_data.get('id')
                    tag_label = tag_data.get('label')

                    tag, created = Tag.objects.get_or_create(
                        tag_id=tag_id,
                        name=tag_label
                    )
                    post.tags.add(tag)

                for attribute in attribute_names:
                    input_name = f'attribute_{attribute.id}'
                    value = request.POST.get(input_name, '').strip()
                    if value:
                        attribute_value, created = AttributeValue.objects.get_or_create(
                            attribute_name=attribute,
                            value=value
                        )
                        post.attributes.add(attribute_value)

                return redirect('/')
            else:
                form.add_error(None, 'Content is required.')
            return render(request, 'object_finder/form.html', {
                'form': form,
                'attribute_names': attribute_names
            })
    return render(request, 'object_finder/form.html', {
        'form': form,
        'attribute_names': attribute_names
    })


def view_post(request, post_id):
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

    comments = post.comments.all().order_by('date_posted')
    tags = post.tags.all()
    attribute_names = AttributeName.objects.all()

    return render(request, 'object_finder/view_post.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'tags': tags,
        'attribute_names': attribute_names
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
