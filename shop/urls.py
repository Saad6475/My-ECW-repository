from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name ="ShopHome"),
    path("about/" , views.about, name ="aboutus"),
    path("contact/" , views.contact, name ="contactus"),
    path("tracker/" , views.tracker, name ="Trackingsystem"),
    path("search/" , views.search, name ="Search"),
    path("products/<int:myid>", views.products, name ="productview"),
    path("checkout/", views.checkout, name ="checkout")
]
