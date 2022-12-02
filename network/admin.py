from django.contrib import admin
from .models import User, Profile, Tweet

admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Profile)

# Register your models here.
