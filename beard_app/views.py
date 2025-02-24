from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Avg
from .forms import PostForm, CommentForm, CustomUserCreationForm, UserUpdateForm, DeleteAccountForm
from .models import Post
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

def home(request):
    sort = request.GET.get('sort')
    if sort == 'date_asc':
        posts_list = Post.objects.all().order_by('created_at')
    elif sort == 'date_desc':
        posts_list = Post.objects.all().order_by('-created_at')
    elif sort == 'rating_asc':
        posts_list = Post.objects.all().order_by('average_rating')
    elif sort == 'rating_desc':
        posts_list = Post.objects.all().order_by('-average_rating')
    else:
        posts_list = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    popular_posts = Post.objects.all().order_by('-comment_count')[:5]
    top_rated_posts = Post.objects.all().order_by('-average_rating')[:5]

    context = {
        'posts': posts,
        'popular_posts': popular_posts,
        'top_rated_posts': top_rated_posts,
        'sort': sort,
    }

    # If the request is AJAX (check the title), then we return only the list of posts
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'beard_app/posts_list.html', context)
    else:
        return render(request, 'beard_app/home.html', context)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration was successful! Now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'beard_app/register.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post successfully created!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'beard_app/create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_sort = request.GET.get('comment_sort', 'date_desc')
    
    # Define sorting of comments
    if comment_sort == 'date_asc':
        all_comments = post.comments.all().order_by('created_at')
    elif comment_sort == 'rating_desc':
        all_comments = post.comments.all().order_by('-rating')
    elif comment_sort == 'rating_asc':
        all_comments = post.comments.all().order_by('rating')
    else:
        all_comments = post.comments.all().order_by('-created_at')
    
    # Comment pagination
    comment_paginator = Paginator(all_comments, 5)
    comment_page_number = request.GET.get('comment_page')
    comments = comment_paginator.get_page(comment_page_number)
    
    # If this is a POST request, we process the comment submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                # Updating counters and rating
                post.comment_count = post.comments.count()
                post.average_rating = post.comments.aggregate(avg=Avg('rating'))['avg'] or 0
                post.save()
                # If the request is AJAX - update the list of comments and return HTML
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    # Update pagination after adding a new comment
                    all_comments = post.comments.all().order_by('-created_at')
                    comment_paginator = Paginator(all_comments, 5)
                    comment_page_number = request.GET.get('comment_page')
                    comments = comment_paginator.get_page(comment_page_number)
                    return render(request, 'beard_app/comments_list.html', {
                        'comments': comments,
                        'comment_sort': comment_sort,
                    })
                # If it's a regular POST, we do a redirect
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    
    # If this is an AJAX GET request to sort or paginate comments, return only the list of comments
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'beard_app/comments_list.html', {
            'comments': comments,
            'comment_sort': comment_sort,
        })
    
    return render(request, 'beard_app/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'comment_sort': comment_sort,
    })



@login_required
def profile(request):
    if request.method == 'POST':
        # If the profile update form is submitted
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Data updated!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'beard_app/profile.html', {'profile_form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if request.user.check_password(password):
                request.user.delete()
                messages.success(request, "Your account has been deleted.")
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Account has NOT been deleted.")
    else:
        form = DeleteAccountForm()
    return render(request, 'beard_app/delete_account.html', {'form': form})
