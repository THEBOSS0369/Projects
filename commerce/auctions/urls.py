from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("display", views.display, name="display"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removelist/<int:id>", views.removelist, name="removelist"),
    path("addlist/<int:id>", views.addlist, name="addlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction"),
]
