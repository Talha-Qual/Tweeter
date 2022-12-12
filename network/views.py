from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
import random
from django.core.paginator import Paginator
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import User, Tweet, Profile
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView
from .forms import ContactForm
from django.urls import reverse_lazy

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

class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'

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
                Profile.objects.create(user = user, handle = tw_handle)
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
    all_users  = User.objects.all().values('username')
    tweets = Tweet.objects.all().order_by('-created_at')
    user_list = []
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        logout(request)
        return redirect('explore')

    if request.method == "GET":
        search = request.GET.get("q")
        if search is not None:
            search = search.lower().strip()
            for key in all_users:
                for idx in key:
                    print(idx)
                    if search == key[idx].lower():
                        username = search
                        return redirect("profile", username)
                if user_list:
                    return render(request, "network/search_profile.html", {
                        "user_list": user_list,
                        "search": search
                    })
    return render(request, "network/index.html", {
        'tweets': tweets,
        'profile': profile})

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
                'tweeter': request.user.username,
                'tweet_id': t.id,
                'created_at': t.created_at,
            })
        return JsonResponse({
            'error': 'tweet length needs to be longer.'}, status = 400)
    return JsonResponse({
        'error': 'error processing request, try again.'}, status = 400)

"""Return type: JSON"""
@csrf_exempt
@login_required(login_url = 'explore')
def like(request):
    if request.method == "POST":
        tweet_id = request.POST.get('id')
        liked = request.POST.get('liked')
        try:
            tweet = Tweet.objects.get(id = tweet_id)
            # if the tweet is already liked, remove the like
            if liked == 'yes':
                tweet.like.remove(request.user)
                liked = 'no'
            elif liked == 'no':
                tweet.like.add(request.user)
                liked = 'yes'
            tweet.save()
            return JsonResponse({
            'likes': tweet.like.count(),
            'liked': liked,
            'status': 200})
        except:
            return JsonResponse({
                'error': 'tweet not found.',
                'status': 400})
    return JsonResponse({
        'error': 'error processing request, try again later.', 'status': 400})

def explore(request):
    tweets = list(Tweet.objects.all())
    random_tweets = random.sample(tweets, 5)
    return render(request, "network/explore.html", {
        'random_tweets': random_tweets
    })

"""Function to return all of the posts by people you are following. Return type: JSON"""
@login_required(login_url = 'explore')
def following(request):
    try:
        following = Profile.objects.get(user=request.user).following.all()
    except:
        logout(request)
        return redirect('explore')
    tweets = Tweet.objects.filter(user__in=following).order_by('-created_at')
    return render(request, "network/following.html", {
        'tweets': tweets
    })

"""Function to follow a user, this is so you can see posts from people you are following, see list of followers, etc.  Return type: JSON"""
@csrf_exempt
@login_required(login_url = 'explore')
def follow(request):
    if request.method == "POST":
        curr_user = request.POST.get('user')
        user_action = request.POST.get('user_action')
        if user_action == "Follow":
            # add to list of people the current user is following
            user = User.objects.get(username=curr_user)
            profile = Profile.objects.get(user=request.user)
            profile.following.add(user)
            profile.save()
            # add to list of followers the user has
            profile = Profile.objects.get(user=user)
            profile.follower.add(request.user)
            profile.save()
            return JsonResponse({
                'status': 200,
                'user_action': 'Unfollow',
                'follower_count': profile.follower.count()})
        else:
            # remove user from list of people the current user is following
            user = User.objects.get(username=curr_user)
            profile = Profile.objects.get(user=request.user)
            profile.following.remove(user)
            profile.save()
            print(user_action)
            # remove user from list of followers
            profile = Profile.objects.get(user=user)
            profile.follower.remove(request.user)
            profile.save()
            return JsonResponse({
                'status': 200,
                'user_action': "Follow",
                "follower_count": profile.follower.count()
            })
    return JsonResponse({'status': 400})

@login_required(login_url = 'explore')
def edit_tweet(request):
    pass

@login_required(login_url = 'explore')
def profile(request, username):
    try:
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user = user)
        users_profile = Profile.objects.get(user=request.user)
    except:
        messages.error(request, 'Unable to fetch user profile information')
        return render(request, 'network/error_page.html')
    tweets = Tweet.objects.filter(user = user).order_by('-created_at')
    context = {
        'user': user,
        'profile': profile,
        'tweets': tweets,
        'users_profile': users_profile,
        'tweet_amount': len(tweets)
    }
    return render(request, "network/profile.html", context)

