from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models

# Create your views here.
def read_blogs(request):
    blogs = models.BlogModel.objects.all()

    if request.method == 'GET':
        blogsearch = request.GET.get('blogsearch', '')
        # blogsearch is name in input field, while '' is default string.
        # Since '' is substring of every string that is why we used it so that by defualt we get all model objects
        blogs = models.BlogModel.objects.filter(blog_heading__icontains=blogsearch)     # __icontains helps us when complete heading name is not searched but a part of it is

    data = {
        'blogs' : blogs
    }

    return render(request, 'home.html', data)

def complete_blog(request, blog_id):
    blog = models.BlogModel.objects.get(id=blog_id)
    # That blog with same id in DB as blog_id in url will be returned

    data = {
        'blog' : blog
    }

    return render(request, 'completeblog.html', data)

def write_blog(request):
    success = False
    # When blog is not posted, success variable will have False value and success message will not be displayed
    if request.method == 'POST':
        username = request.POST['username']
        blog_heading = request.POST['blog_heading']
        blog_content = request.POST['blog_content']

        user = User.objects.get(username=username)
        # Since User model was used as foreign key, so here we compare which username in DB is same as the username of the user writing the blog

        obj = models.BlogModel(blog_heading=blog_heading, blog_author=user, blog_content=blog_content)
        obj.save()

        success = True
        # When blog is posted, success variable will have boolean value True and now success message will be displayed


    data = {
        'success' : success
    }

    return render(request, 'writeblog.html', data)

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Since both passwords cannot be different
        if password == password2:
            # If someone with same username already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                # After saving user details, taking that user to login page so that user can login
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('signup')

    return render(request, 'signup.html')

def log_user_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If username or password is incorrect, authenticate function returns None
        if user is not None:
            # Logging user in
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Recheck Inputs. Unable to login.')
            return redirect('login')

    return render(request, 'login.html')

# If user wants to log in from write blog page
def log_in_write_blog(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If username or password is incorrect, authenticate function returns None
        if user is not None:
            # Logging user in
            login(request, user)
            return redirect('writeblog')
        else:
            messages.info(request, 'Recheck Inputs. Unable to login.')
            return redirect('login')
    
    return render(request, 'login.html')

def log_user_out(request):
    # Logging user out
    logout(request)
    return redirect('home')
