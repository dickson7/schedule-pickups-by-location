from .__init__ import *

class DriverProximity(GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        params = {key: value for key, value in request.GET.items()}
        
        response = {}
        
        try:
            drivers = location_driver()
            location_user = int(params["lng"]) + int(params["lat"])
            date = save_date_utc(params["date"])
            
            for driver in drivers:
                print(int(driver["lat"])+int(driver["lng"]))
                driver["location"]=int(driver["lat"])+int(driver["lng"])
                driver["proximity"]=abs(driver["location"]-location_user)
                
            drivers = sorted(drivers, key=lambda driver : driver['proximity'])
            
            for driver in drivers:
                driver_proximity = DetailsDriverAvailability.objects.filter(
                    driver=driver["id"],
                    date__year=date.year,
                    date__month=date.month,
                    date__day=date.day,
                    hour=NUM_TO_HOUR[str(view_date(date).hour)]
                )
                if driver_proximity and driver_proximity[0].status == "DISPONIBLE":
                    response={
                        "driver_id": driver_proximity[0].driver.id,
                        "driver_name": driver_proximity[0].driver.name,
                        "lat":driver["lat"],
                        "lng":driver["lng"],
                        "available_hour_id":driver_proximity[0].id
                    }
                    break
                else:
                    response={
                        "details": "No se encontraron conductores cerca"
                    }
            status = codes.HTTP_200_OK
        except Driver.DoesNotExist:
            response = DRIVER_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"details":  str(e)}
            status = codes.HTTP_400_BAD_REQUEST
            
        return HttpResponse(json.dumps(response), APPLICATION_JSON, status=status)