from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=240)
    starting_bid = models.IntegerField()
    largest_bid = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    link = models.URLField(max_length=240, blank=True)
    image = models.ImageField(upload_to='listing_images', blank=True)
    wishlist = models.ManyToManyField(User, blank=True, related_name="wishlist_item")
    is_closed = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title}: {self.body[:25]}..."


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField(default=5)


    def __str__(self):
        return f"${self.bid}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listings = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=240, null=True)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.body[:30]}..."
