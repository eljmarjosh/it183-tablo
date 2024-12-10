from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import HttpResponseRedirect
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .serializers import PostSerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.exceptions import PermissionDenied

# Create your views here.

from django.http import HttpResponseRedirect

# Create your views here.

def blog_list(request):
   post = Post.objects.all()
   context = {

       'blog_list':post
   }
   return render(request, "blog/blog_list.html",context)

def blog_delete(request, id):
    each_post = Post.objects.get(id = id)
    if each_post.author != request.user:
        messages.info(request, "You are not authorized to delete this post.")
        return redirect('/')  # Redirect to the homepage or another relevant page
    each_post.delete()
    return HttpResponseRedirect('/')

@login_required  # Ensure only logged-in users can leave comments
def blog_detail(request, id):
    each_post = get_object_or_404(Post, id=id)
    comments = each_post.comments.all()  # Fetch related comments
    comment_count = comments.count()
    avg_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0.0  # Calculate average rating

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = each_post
            comment.author = request.user  # Assign the logged-in user as the author
            comment.save()
            return redirect('blog_detail', id=each_post.id)
    else:
        form = CommentForm()

    context = {
        'blog_detail': each_post,
        'form': form,
        'comments': comments,
        'comment_count': comment_count,
        'avg_rating': avg_rating,
    }
    return render(request, "blog/blog_detail.html", context)

@login_required
def blog_create(request):
    form = PostForm(request.POST or None, request.FILES or None)  # Include request.FILES for file uploads
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user  # Assign the logged-in user as the author
        post.save()
        messages.success(request, "Post created successfully!")
        return redirect('/')  # Redirect to the homepage or another relevant page
    context = {
        "form": form
    }
    return render(request, "blog/blog_create.html", context)

@login_required
def blog_update(request, id):
    post = get_object_or_404(Post, id=id)

    # Check if the logged-in user is the author
    if post.author != request.user:
        messages.error(request, "You are not authorized to update this post.")
        return redirect('/')  # Redirect to the homepage or another relevant page

    form = PostForm(request.POST or None, request.FILES or None, instance=post)  # Include request.FILES for file uploads
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated successfully!")
        return HttpResponseRedirect('/')

    context = {
        "form": form,
        'form_type': 'Update'
    }
    return render(request, "blog/blog_create.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to the homepage or any other page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'blog/login.html')  # Use your login.html template

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')  # Redirect to the login page

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Automatically log in the user after registration
        messages.success(request, "Account created successfully!")
        return redirect('home')  # Redirect to homepage or any other page

    return render(request, 'blog/register.html')  # Render the registration page

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
