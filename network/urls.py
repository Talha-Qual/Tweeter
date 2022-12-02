
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("explore", views.explore, name="explore"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    path("logout", views.logout_view, name="logout"),
    path('posttweet/', views.post_tweet, name = "post-tweet"),
]
