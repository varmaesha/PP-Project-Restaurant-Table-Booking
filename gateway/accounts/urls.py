from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("register",views.register, name="register"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("orderHistory",views.orderHistory, name="orderHistory"),
    path("hotelPage/<str:city_name>/<str:hotel_name>",views.hotelPage, name="hotelPage"),
    path("hotelSearch",views.hotelSearch, name="hotelSearch")
]