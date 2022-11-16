from django.db import models
from authentication.models import User
from helpers.models import TrackingModels

# Create your models here.
class Driver(TrackingModels):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    
class DriverAvailability(TrackingModels):
    driver = models.ForeignKey(
        Driver,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Cuenta del driver",
    )
    is_availability = models.BooleanField(default=True)
    date = models.DateTimeField(null=False)
    hours_availability = models.CharField(max_length=20, null=False)


class DetailsDriverAvailability(TrackingModels):
    driver_availability = models.IntegerField(null=True)
    driver = models.ForeignKey(
        Driver,
        null=False,
        on_delete=models.CASCADE,
    )
    is_availability = models.BooleanField(default=True)
    hour = models.CharField(max_length=20, null=False)
    date = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, null=False, default="DISPONIBLE")
    pickup_id = models.IntegerField(null=True)



class Pickup(TrackingModels):
    driver = models.ForeignKey(
        Driver,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="ID driver",
    )
    availability = models.IntegerField(null=False)
    pickup_lng = models.CharField(max_length=20)
    pickup_lat = models.CharField(max_length=20)
    pickup_address = models.TextField()
    target_lng = models.CharField(max_length=20)
    target_lat = models.CharField(max_length=20)
    target_address = models.TextField()
    user_id = models.IntegerField(null=False)
    description = models.TextField()
    
    
    
  