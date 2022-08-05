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

from .models import User, Profile, Property_listing, LikePost, FollowersCount, Notifications


@login_required(login_url="login")
def feed(request):
    current_profile = Profile.objects.get(user=request.user)
    current_listings = Property_listing.objects.filter(active=True)
    user_listings = Property_listing.objects.filter(owner=request.user)
    follow_requests = Notifications.objects.filter(
        user=request.user,
        recipients=request.user,
        archived=False,
        follow_request=True,
        book_location=False
    )
    booking_notice = Notifications.objects.filter(
        user=request.user,
        recipients=request.user,
        archived=False,
        follow_request=False,
        book_location=True
    )
    messages = Notifications.objects.filter(
        user=request.user,
        recipients=request.user,
        archived=False,
        follow_request=False,
        book_location=False
    )

    prop_listing = request.user.property_follow.all()

    return render(request, "homeshare/feed.html", {
        'current_profile': current_profile,
        'current_listings':current_listings,
        'user_listings':user_listings,
        'follow_requests':follow_requests,
        'messages':messages,
        'prop_listing': prop_listing,
        'booking_notice': booking_notice
        })



@login_required(login_url="login")
def property_profile(request, id):
    current_listing = Property_listing.objects.get(id=id)
    following = request.user.property_follow.all()
    print(following)

    return render(request, "homeshare/property_profile.html", {
        'current_listing': current_listing,
        'following':following
    })


@login_required(login_url="login")
def user_profile(request, username):
    get_user = User.objects.get(username=username)
    owner_profile = Profile.objects.get(username=username)
    owner_listings = Property_listing.objects.filter(owner=get_user)

    return render(request, "homeshare/user_profile.html", {
        'owner_profile': owner_profile,
        'owner_listings': owner_listings,
        'get_user': get_user
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


# Took to long to find the answer to restricting username and password with out building a model so I just wrote a helper function
def prevent_duplicate_email(email):
    try:
        check = User.objects.get(email=email)
        return True
    except:
        return False


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
            if prevent_duplicate_email(email):
                return render(request, "homeshare/login_register.html", {
                    "register_message": "email already taken."
                })
            else:
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


# ------------------------------------Notification Section-------------------------------



# give you the ability to message an individual
@csrf_exempt
@login_required
def create_alert(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    notifications = [notice.strip() for notice in data.get("recipients").split(",")]
    if notifications == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for notice in notifications:
        try:
            user = User.objects.get(email=notice)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User {notice} does not exist."
            }, status=400)

    # Get contents of email
    subject = data.get("subject", "")
    body = data.get("body", "")
    follow_request = False
    book_location = False
    if data.get("follow_request") is not None:
        follow_request = data.get("follow_request", "")
    if data.get("book_location") is not None:
        book_location = data.get("book_location", "")


    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        new_notice = Notifications(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user,
            follow_request=follow_request,
            book_location=book_location

        )

        # if data.get("follow_request") is not None:
        #     print("hello")
        #     new_notice.follow_request = data["follow_request"]

        new_notice.save()
        for recipient in recipients:
            new_notice.recipients.add(recipient)

        new_notice.save()


    return JsonResponse({"message": "Email sent successfully."}, status=201)


@csrf_exempt
@login_required
def notice(request, notice_id):

    # Query for requested email
    try:
        note_message = Notifications.objects.get(user=request.user, pk=notice_id)

    except Notifications.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(note_message.serialize())

    # Update whether email is read or should be archived

    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("read") is not None:
            note_message.read = data["read"]
        if data.get("archived") is not None:
            note_message.archived = data["archived"]
        note_message.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
# Update listings as needed
def property(request, listing_id):

    # Query for requested email
    try:
        prop_listing = Property_listing.objects.get(owner=request.user, pk=listing_id)
        print("listing", prop_listing)

    except Property_listing.DoesNotExist:
        return JsonResponse({"error": "Property not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(prop_listing.serialize())

    # Update whether email is read or should be archived

    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("active") is not None:
            prop_listing.active = data["active"]
        prop_listing.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def follow_property(request, listing_id):
    try:
        prop_listing = Property_listing.objects.get( pk=listing_id)

    except Property_listing.DoesNotExist:
        return JsonResponse({"error": "Property not found."}, status=404)

    request.user.property_follow.add(prop_listing)

    return HttpResponseRedirect(reverse("property_profile", args=(prop_listing.id,)))



def unfollow_property(request, listing_id):
    try:
        prop_listing = Property_listing.objects.get( pk=listing_id)

    except Property_listing.DoesNotExist:
        return JsonResponse({"error": "Property not found."}, status=404)

    request.user.property_follow.remove(prop_listing)

    return HttpResponseRedirect(reverse("feed"))

