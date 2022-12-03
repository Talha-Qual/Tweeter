from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Tweet, Profile
from django.http import JsonResponse


from .models import User


class PasswordChangeView():
    template_name = 'registration/password_change_form.html'
    success_url = 'registration/password_change_done.html'

class PasswordChangeDoneView():
    template_name = 'registration/password_change_done.html'

class PasswordResetView():
    template_name = 'registration/password_reset_form.html'
    success_url = 'registration/password_reset_done.html'

class PasswordResetDoneView():
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView():
    template_name = 'registration/password_reset_confirm.html'
    success_url = 'registration/password_reset_complete.html'

class PasswordResetCompleteView():
    template_name = 'registration/password_reset_complete.html'


# class LoginView():
#     template_name = 'network/layout.html'
#     redirect_field_name = 'network/index'

# class LogoutView():
#     template_name = 'network/layout.html'
#     redirect_field_name = 'network/explore'

def login_register(request):
    if request.method == "POST":
        if 'login' == request.POST.get('mode'):
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return render(request, "network/explore.html", {
                    "message": "Invalid username and/or password."
                })
        elif 'register' == request.POST.get('mode'):
            username = request.POST["username"]
            email = request.POST["email"]
            tw_handle = request.POST["tw_handle"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "network/explore.html", {
                    "message": "Passwords must match."
                }) # need to add message to index.html

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                profile = Profile.objects.create(user = user, handle = tw_handle)
            except IntegrityError:
                return render(request, "network/explore.html", {
                    "message": "Username already taken."
                }) # need to add message to index.html
            login(request, user)
            return redirect("index")
        else:
            return redirect("explore")
    else:
        return render(request, "network/explore.html")

def logout_view(request):
    logout(request)
    return redirect("explore")

@login_required(login_url = 'explore')
def index(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, "network/index.html", {'tweets': tweets})

"""Need to think of a way to return a JSON response here and get it picked up by 
a js function for the async call. Might start with just returning a post to make 
sure that the call is working though."""
@login_required(login_url = 'explore')
def post_tweet(request):
    if request.method == "POST":
        if len(request.POST.get('tweet')) != 0: 
            t = Tweet.objects.create(user = request.user, tweet = request.POST.get('tweet'))
            return JsonResponse({
                'tweet': t.tweet,
                'tweeter': f'{t.user}',
                'created_at': t.created_at,
                'status': 200
            })
        return JsonResponse({}, status = 400)
    return JsonResponse({}, status = 400)

"""Return type: JSON"""
@login_required(login_url = 'explore')
def like(request):
    pass

def explore(request):
    return render(request, "network/explore.html")

"""Return type: JSON"""
@login_required(login_url = 'explore')
def following(request):
    return render(request, "network/following.html")

"""Return type: JSON"""
@login_required(login_url = 'explore')
def follow(request):
    pass

@login_required(login_url = 'explore')
def edit_tweet(request):
    pass

@login_required(login_url = 'explore')
def profile(request, username):
    try:
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user = user)
    except:
        messages.error(request, 'Unable to fetch user profile information')
        return render(request, 'network/error_page.html')
    tweets = Tweet.objects.filter(user = user).order_by('-created_at')
    context = {
        'user': user,
        'profile': profile,
        'tweets': tweets,
    }
    return render(request, "network/profile.html", context)

