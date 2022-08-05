# CSCI_s_33_Final_Project


# Overview

homeShare is a social network version of Airbnb for those individuals who would rather 
have someone they know stay at their home or property. You are able to request a booking by date, 
message a user and add properties to your follow list as needed. 

# To Begin 

1. Download 
2. From your terminal cd into final_project at the same level as the manage.py file.
3. Run python manage.py makemigrations homeshare
4. Run python manage.py migrate

# \Understanding the Code:

Once you start you will notice that due to limitations of needing to sign in you will need to register an account.
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



As you can see above you will not be taken directly to the main page 
but to a completion page where you will have the option to add a photo and fill out some additional information about 
yourself. 

In your profile under the home feed you will see Your Profile. To add a new property simply click
Add Property to the right of the screen. this will take you to a simple page so you can add to your properties

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


As you can see from the code above there is a multitude of different options and addons to account for once you use the
create button. Once you are completed you will be taken back to the main feed page where you will be able to skim through
your posting. Please note that the "make active button must be checked in order for your property to appear. 
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





If you wish to hide the property from the feed you will need to navigate to Your Profile and hit 'Delist'. This will essentially set 
the property to archive mode so no other users have the ability to see it. 

In order to view the properties of others navigate to your Home Feed and hit see property. It will have a display of the 
main picture, any subsequent pictures. If you wish to follow the property hit follow and it will be added to your follow 
list in the main feed view. While request booking will allow you to select dates you wish to 

All in all the user interface is simple and straight fora=ward along with the messaging. 

