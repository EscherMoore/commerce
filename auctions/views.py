from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import Textarea
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid, Category

@login_required
def wishlist(request):
    delete = False
    wish_user = User.objects.get(pk=request.user.id)
    wishlist = wish_user.wishlist_item.all()
    if request.method == "GET":
        return render(request, "auctions/wishlist.html", {
            "wishlist": wishlist,
            })


def index(request):
    active_listings = Listing.objects.exclude(is_closed=True).all()
    return render(request, "auctions/index.html", {
        "listings": active_listings.order_by('-date_created'),
        })


def closed(request):
    closed_listings = Listing.objects.exclude(is_closed=False).all()
    return render(request, "auctions/closed.html", {
        "closed_listings": closed_listings.order_by('-date_created'),
        })


def categories(request): 
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.order_by('category').all()
        })


def results(request, category_id):
    is_results = False
    category = Category.objects.get(id=category_id)
    if Listing.objects.filter(category=category):
        is_results = True
        results = Listing.objects.filter(category=category)
        return render(request, "auctions/results.html", {
            "results": results,
            "is_results": is_results,
            })

    results = Listing.objects.filter(category=category)
    return render(request, "auctions/results.html", {
        "results": results,
        "is_results": is_results,
        })



class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']



class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
                'body': Textarea(attrs={'cols': 40, 'rows': 5}),
            }


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.listings = Listing.objects.get(id=listing_id)
            comment.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))




class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'body', 'starting_bid', 'image', 'link']
        widgets = {
                'body': Textarea(attrs={'cols': 40, 'rows': 5}),
            }
 
       
@login_required
def create(request):
    categories = Category.objects.order_by('category').all()
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            if 'category' in request.POST:
                category_id = int(request.POST["category"])
            else:
                category_id = False
            if category_id != False:
                category = Category.objects.get(id=category_id)
                new_listing = Listing.objects.get(id=listing.id)
                new_listing.category.add(category)
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))
    

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": NewListingForm(),
        "categories": categories,
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



class AddOrRemWishlistItem(forms.Form):
    fields = ["add_wishlist", "remove_wishlist"] 



@login_required
def remove_wishlist_from_wishlist_page(request, listing_id):
    if request.method == "POST":
        form = AddOrRemWishlistItem(request.POST)
        if form.is_valid():
            if ["remove_wishlist"]:
                user = request.user
                listing = Listing.objects.get(id=listing_id)
                listing.wishlist.remove(user)
                return HttpResponseRedirect(reverse("wishlist"))
            return HttpResponseRedirect(reverse("wishlist"))
        return HttpResponseRedirect(reverse("wishlist"))
    return HttpResponseRedirect(reverse("wishlist"))



@login_required
def remove_wishlist(request, listing_id):
    if request.method == "POST":
        form = AddOrRemWishlistItem(request.POST)
        if form.is_valid():
            if ["remove_wishlist"]:
                user = request.user
                listing = Listing.objects.get(id=listing_id)
                listing.wishlist.remove(user)
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))



@login_required
def add_wishlist(request, listing_id):
    if request.method == "POST":
        form = AddOrRemWishlistItem(request.POST)
        if form.is_valid():
            if ["add_wishlist"]:     
                request.user.wishlist_item.add(listing_id)
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))



class CloseListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["is_closed"]


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        form = CloseListing(request.POST, instance=listing)
        if form.is_valid():
            if ["is_closed"]: 
                closed_listing = form.save(commit=False)
                closed_listing.is_closed = True
                closed_listing.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))



def listing(request, listing_id):
    has_watchlist_item = False
    listing = Listing.objects.get(id=listing_id)
     
    latest_bid = listing.bids.last
    if latest_bid:
        current_bid = latest_bid

        # need to add a parameter for non logged in users to not see 
    if request.user.is_authenticated:
        wish_user = User.objects.get(pk=request.user.id)
        for item in wish_user.wishlist_item.all():
            if item == listing:
                has_watchlist_item = True


    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = Listing.objects.get(id=listing_id)
            if listing.bids.last():
                if bid.bid <= listing.bids.last().bid:
                    return render(request, "auctions/listing.html", {
                        "bid_form": NewBidForm(),
                        "comment_form": NewCommentForm(),
                        "listing": listing,
                        "comments": listing.comments.all(),
                        "current_bid": current_bid, 
                        "has_watchlist_item": has_watchlist_item,
                        "categories": listing.category.all(),
                        "message": "You must bid higher than the last bid!",
                        "bid_count": listing.bids.count(),
                        })
                bid.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
            if bid.bid <= listing.starting_bid:
                return render(request, "auctions/listing.html", {
                    "bid_form": NewBidForm(),
                    "comment_form": NewCommentForm(),
                    "listing": listing,
                    "comments": listing.comments.all(),
                    "current_bid": current_bid, 
                    "has_watchlist_item": has_watchlist_item,
                    "categories": listing.category.all(),
                    "message": "You must bid higher than the starting bid!",
                    "bid_count": listing.bids.count(),
                    })
            bid.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
                
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return render(request, "auctions/listing.html", {
        "bid_form": NewBidForm(),
        "comment_form": NewCommentForm(),
        "listing": listing,
        "comments": listing.comments.all(),
        "current_bid": current_bid, 
        "has_watchlist_item": has_watchlist_item,
        "categories": listing.category.all(),
        "bid_count": listing.bids.count(),
        })
