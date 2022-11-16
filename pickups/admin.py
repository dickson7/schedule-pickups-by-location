from django.contrib import admin

# Register your models here.

from .models import Pickup, DriverAvailability, Driver


class PickupAdmin(admin.ModelAdmin):
    
    list_display=()
    search_fields =('user_id', 'driver',)
    list_per_page=25

admin.site.register(Pickup,PickupAdmin)

class DriverAvailabilityAdmin(admin.ModelAdmin):
    
    list_display=('driver','is_availability','date','hours_availability',)
    list_per_page=25

admin.site.register(DriverAvailability,DriverAvailabilityAdmin)

class DriverAdmin(admin.ModelAdmin):
    
    list_display=('id', 'name','is_active', )
    search_fields =('name',)
    list_per_page=25

admin.site.register(Driver,DriverAdmin)