import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator

from .models import User, Profile, Property_listing, LikePost, FollowersCount


@login_required(login_url="login")
def feed(request):
    current_profile = Profile.objects.get(user=request.user)
    current_listings = Property_listing.objects.filter(active=True)
    user_listings = Property_listing.objects.filter(active=True, owner=request.user)


    return render(request, "homeshare/feed.html", {
        'current_profile': current_profile,
        'current_listings':current_listings,
        'user_listings':user_listings,
        })



@login_required(login_url="login")
def property_profile(request, id):
    current_listing = Property_listing.objects.get(id=id)

    return render(request, "homeshare/property_profile.html", {'current_listing': current_listing})


@login_required(login_url="login")
def user_profile(request, username):
    get_user = User.objects.get(username=username)
    owner_profile = Profile.objects.get(username=username)
    owner_listings = Property_listing.objects.filter(owner=get_user)

    return render(request, "homeshare/user_profile.html", {
        'owner_profile': owner_profile,
        'owner_listings': owner_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))
        else:
            return render(request, "homeshare/login_register.html", {
                "login_message": "Invalid username and/or password."
            })
    else:
        return render(request, "homeshare/login_register.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("feed"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "homeshare/login_register.html", {
                "register_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            # A new profile for users is created with sign up.
            # however they need to be redirected to finalize profile page.

            get_user = User.objects.get(username=username)
            create_profile = Profile(
                user=get_user,
                username=username,
                profile_id=get_user.id)

            create_profile.save()

        except IntegrityError:
            return render(request, "homeshare/login_register.html", {
                "register_message": "Username already taken."
            })

        login(request, user)
        return render(request, "homeshare/complete_profile.html")
    else:
        return render(request, "homeshare/login_register.html")


@login_required(login_url="login")
def complete_profile(request):
    current_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('img') != None:
            image = request.FILES.get('img')
            bio = request.POST['bio']

            current_profile.profilePic = image
            current_profile.bio = bio
            current_profile.save()

        if request.FILES.get('img') == None:
            image = current_profile.profilePic
            bio = request.POST['bio']

            current_profile.profilePic = image
            current_profile.bio = bio
            current_profile.save()

        return redirect('feed')
    return render(request, 'feed.html', {'current_profile': current_profile})


@login_required(login_url="login")
def new_listing(request):
    if request.method == 'POST':

        title = request.POST['title']
        image_url = request.FILES.get('img')
        image_url_2 = request.FILES.get('img2')
        image_url_3 = request.FILES.get('img3')
        image_url_4 = request.FILES.get('img4')
        image_url_5 = request.FILES.get('img5')
        image_url_6 = request.FILES.get('img6')
        rooms = request.POST['rooms']
        bathrooms = request.POST['bathrooms']
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        city = request.POST['city']
        state = request.POST['state']
        active = True_or_False(request.POST.get('active'))
        description = request.POST['description']
        cost = request.POST['cost']
        pool = True_or_False(request.POST.get('pool'))
        wifi = True_or_False(request.POST.get('wifi'))
        kitchen = True_or_False(request.POST.get('kitchen'))
        free_parking = True_or_False(request.POST.get('free_parking'))
        jacuzzi = True_or_False(request.POST.get('jacuzzi'))
        washer = True_or_False(request.POST.get('washer'))
        air_conditioning = True_or_False(request.POST.get('air_conditioning'))
        self_check_in = True_or_False(request.POST.get('self_check_in'))
        workspace = True_or_False(request.POST.get('workspace'))
        pets_allowed = True_or_False(request.POST.get('pets_allowed'))
        smoke_alarm = True_or_False(request.POST.get('smoke_alarm'))
        carbon_monoxide_alarm = True_or_False(request.POST.get('carbon_monoxide_alarm'))
        fire_extinguisher = True_or_False(request.POST.get('fire_extinguisher'))
        first_aid_kit = True_or_False(request.POST.get('first_aid_kit'))
        crib_and_high_chair = True_or_False(request.POST.get('crib_and_high_chair'))
        bathtub = True_or_False(request.POST.get('bathtub'))
        wine_glasses = True_or_False(request.POST.get('wine_glasses'))
        coffee_maker = True_or_False(request.POST.get('coffee_maker'))

        create_listing = Property_listing(
            owner=request.user,
            title=title,
            image_url=image_url,
            image_url_2=image_url_2,
            image_url_3=image_url_3,
            image_url_4=image_url_4,
            image_url_5=image_url_5,
            image_url_6=image_url_6,
            rooms=rooms,
            bathrooms=bathrooms,
            address_1=address_1,
            address_2=address_2,
            city=city,
            state=state,
            active=active,
            description=description,
            cost=cost,
            pool=pool,
            wifi=wifi,
            kitchen=kitchen,
            free_parking=free_parking,
            jacuzzi=jacuzzi,
            washer=washer,
            air_conditioning=air_conditioning,
            self_check_in=self_check_in,
            workspace=workspace,
            pets_allowed=pets_allowed,
            smoke_alarm=smoke_alarm,
            carbon_monoxide_alarm=carbon_monoxide_alarm,
            fire_extinguisher=fire_extinguisher,
            first_aid_kit=first_aid_kit,
            crib_and_high_chair=crib_and_high_chair,
            bathtub=bathtub,
            wine_glasses=wine_glasses,
            coffee_maker=coffee_maker

        )

        create_listing.save()

        return redirect('feed')

    else:
        return render(request, "homeshare/new_listing.html")


# helper function to convert on off in check box to True False for Boolean
def True_or_False(bool):
    if bool == 'on':
        return True
    else:
        return False
