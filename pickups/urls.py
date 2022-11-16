from django.urls import path
from .views.driver_availability_view import DriverAvailabilityView
from .views.schedule_pickup import SchedulePickup
from .views.driver_proximity import DriverProximity

urlpatterns = [
    path('pickup/schedule', SchedulePickup.as_view(),name='schedule'),
    path('driver/proximity', DriverProximity.as_view(),name='proximity'),
    path('driver/availability', DriverAvailabilityView.as_view(),name='availability'),
]