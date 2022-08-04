from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("complete_profile", views.complete_profile, name="complete_profile"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("property_profile/<int:id>", views.property_profile, name="property_profile"),
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),


    # API Routes
    path("create_alert", views.create_alert, name="create_alert"),

]
