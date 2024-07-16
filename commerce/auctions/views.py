from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid


def index(request):
    activelisting = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activelisting,
        "categories": allCategories
    })

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    listinginwatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    owner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "listinginwatchlist": listinginwatchlist,
        "allcomments": allcomments,
        "owner": owner,
        "update": True,
        "message": "Congrats!! You won the Bid"
    })

def closeauction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    owner = request.user.username == listingData.owner.username
    listinginwatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "listinginwatchlist": listinginwatchlist,
        "allcomments": allcomments,
    })

def watchlist(request):
    currentUser = request.user
    listings = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    owner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "update": True,
            "owner": owner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid was Not Successful",
            "update": False,
            "owner": owner
        })

def addcomment(request, id):
    user = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=user,
        listing=listingData,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing",  args=(id, )))

def addlist(request, id):
    listingData = Listing.objects.get(pk=id)
    user = request.user
    listingData.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing",  args=(id, )))

def removelist(request, id):
    listingData = Listing.objects.get(pk=id)
    user = request.user
    listingData.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def create(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        #Get the data from form
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["url"]
        category = request.POST["category"]
        price = request.POST["price"]

        #Get the data of User
        presentUser = request.user

        #Get all content
        categoryData = Category.objects.get(categoryN=category)

        #bidding
        bid = Bid(bid=float(price), user=presentUser)
        bid.save()

        #create a new listing
        newlist = Listing(
            title=title,
            description=description,
            url=url,
            category=categoryData,
            price=bid,
            owner=presentUser
        )
        
        #save the data
        newlist.save()

        #redirect to index page
        return HttpResponseRedirect(reverse(index))
    
def display(request):
    if request.method == "POST":
        categoryForm = request.POST['category']
        category = Category.objects.get(categoryN=categoryForm)
        activelisting = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activelisting,
            "categories": allCategories
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
