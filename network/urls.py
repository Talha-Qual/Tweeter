
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import MyPasswordResetForm

urlpatterns = [
    path("", views.explore, name="explore"),
    path("home", views.index, name="index"),
    path("login_reg", views.login_register, name="login_register"),
    path('following/', views.following, name="following"),
    path('u/<username>', views.profile, name="profile"),
    path("logout", views.logout_view, name="logout"),
    path('posttweet/', views.post_tweet, name = "post-tweet"),
    path('like/', views.like),
    path('follow/', views.follow),
    path('edit_tweet/', views.edit_tweet),
    path("password_change", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class = MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
