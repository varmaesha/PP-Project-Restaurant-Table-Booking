from django.db import models
from datetime import datetime
from django.utils.timezone import now

class previousOrders(models.Model):

    username = models.CharField(max_length=100)
    ordertime = models.DateTimeField(default=now, blank=True)
    hotelname = models.CharField(max_length=50)
    cityname = models.CharField(max_length=50)
    bookingdate = models.DateField(auto_now=False, auto_now_add=False)
    bookingtime = models.TimeField(auto_now=False, auto_now_add=False)

class restra_info():
    res_name: str
    res_city: str
    res_type: str

