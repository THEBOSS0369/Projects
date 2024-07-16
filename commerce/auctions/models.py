from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryN = models.CharField(max_length = 300)

    def __str__(self):
        return self.categoryN
    
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='userBid')

    def __str__(self):
        return str(self.bid)

class Listing(models.Model):
    title = models.CharField(max_length = 40)
    description = models.CharField(max_length = 4000)
    url = models.CharField(max_length = 1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice") # if no bid exists for a listing, it will be set to
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title
    

     
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, null=False, related_name='listing')
    message = models.CharField(max_length = 4000)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    
