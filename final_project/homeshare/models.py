from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


# following a property should pretty much be what watch list was for eCom project
class User(AbstractUser):
    property_follow = models.ManyToManyField("Property_listing", related_name="follow_property")


# Every person who signs up gets a profile but should be able to add and edit profile.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.TextField(blank=True)
    profile_id = models.IntegerField()
    profilePic = models.ImageField(upload_to='profile_images', default='Blank-User.jpg')
    bio = models.TextField(blank=True)


# Each listing has an address and ammenities associated with it. ALong with dates on when the property is avail.
class Property_listing(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="owner_listings")
    title = models.CharField(max_length=144)
    created_at = models.DateTimeField(default=datetime.now)
    image_url = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    image_url_2 = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    image_url_3 = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    image_url_4 = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    image_url_5 = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    image_url_6 = models.ImageField(upload_to='listing_images', default='pic1.jpg')
    rooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=144)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=False)
    cost = models.DecimalField(max_digits=19, decimal_places=2)
    pool = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    free_parking = models.BooleanField(default=False)
    jacuzzi = models.BooleanField(default=False)
    washer = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    self_check_in = models.BooleanField(default=False)
    workspace = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    smoke_alarm = models.BooleanField(default=False)
    carbon_monoxide_alarm = models.BooleanField(default=False)
    fire_extinguisher = models.BooleanField(default=False)
    first_aid_kit = models.BooleanField(default=False)
    crib_and_high_chair = models.BooleanField(default=False)
    bathtub = models.BooleanField(default=False)
    wine_glasses = models.BooleanField(default=False)
    coffee_maker = models.BooleanField(default=False)

# change the email to allow for notifications. When boolean values are checked they are endered differently.
class Notifications(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="notifications_sent")
    recipients = models.ManyToManyField("User", related_name="notifications_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    follow_request = models.BooleanField(default=False)
    book_location = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }




class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user