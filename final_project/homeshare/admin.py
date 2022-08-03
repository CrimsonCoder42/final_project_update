from django.contrib import admin
from .models import User, Profile, Property_listing, LikePost, FollowersCount
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Property_listing)
admin.site.register(LikePost)
admin.site.register(FollowersCount)