from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Tweet, Profile
from django.http import JsonResponse


from .models import User

def index(request):
    if request.method == "POST":
        if 'login' == request.POST.get('mode'):
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "network/index.html", {
                    "message": "Invalid username and/or password."
                })
        elif 'register' == request.POST.get('mode'):
            print("working")
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "network/index.html", {
                    "message": "Passwords must match."
                }) # need to add message to index.html

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "network/index.html", {
                    "message": "Username already taken."
                }) # need to add message to index.html
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, "network/index.html", {'tweets': tweets})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("explore"))

"""Need to think of a way to return a JSON response here and get it picked up by 
a js function for the async call. Might start with just returning a post to make 
sure that the call is working though."""
@login_required
def post_tweet(request):
    if request.method == "POST":
        t = Tweet.objects.create(user = request.user, tweet = request.POST.get('tweet'))
        # print(f'Function post_tweet called. tweet = {t.tweet}')
        return JsonResponse({
            'tweet': t.tweet,
            'tweeter': f'{t.user}',
            'created_at': t.created_at
        })

def explore(request):
    return render(request, "network/explore.html")

def following(request):
    return render(request, "network/following.html")

def like(request):
    pass

def edit_tweet(request):
    pass

def follow(request):
    pass

def profile(request):
    return render(request, "network/profile.html")

