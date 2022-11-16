from .__init__ import *


class SchedulePickup(GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        params = request.data.copy()
        response = {}
        try:
            driver = Driver.objects.get(id=params["driver_id"])
            availability = DetailsDriverAvailability.objects.get(id=params["availability_id"])
            if driver and availability and availability.status == DISPONIBLE:
                pickup = Pickup.objects.create(
                    driver=driver,
                    availability=availability.id,
                    pickup_lng=params["pickup_lng"],
                    pickup_lat=params["pickup_lat"],
                    pickup_address=params["pickup_address"],
                    target_lng=params["target_lng"],
                    target_lat=params["target_lat"],
                    target_address=params["target_address"],
                    user_id=params["user_id"],
                    description=params["description"]
                )
                availability.status=OCUPADO
                availability.pickup_id=pickup.id
                availability.save()
            else:
                raise Exception("Esta franja ya esta ocupada por otra recogida")
            response = {
                "status": "Done"
            }
            status = codes.HTTP_200_OK 
        except DetailsDriverAvailability.DoesNotExist:
            response = DETAILS_DRIVER_AVAILABILITY_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Driver.DoesNotExist:
            response = DRIVER_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"details":  str(e)}
            status = codes.HTTP_400_BAD_REQUEST
            
        return HttpResponse(json.dumps(response), APPLICATION_JSON, status=status)


    def get(self, request, *args, **kwargs):
        params = {key: value for key, value in request.GET.items()}
        
        response = {}
        hours_availability=[]
        date_search = save_date_utc(params["date"])
        try:
            pickups = DetailsDriverAvailability.objects.filter(
                date__year=date_search.year,
                date__month=date_search.month,
                date__day=date_search.day)
            for i in HOURS:
                response[i]=[]
            for pickup in pickups:
                if pickup.status==OCUPADO:
                    details_pickup=Pickup.objects.get(id=pickup.pickup_id)
                    response[pickup.hour]+=[{
                        "driver_id": details_pickup.driver.id,
                        "driver_name": details_pickup.driver.name,
                        "pickup_id":pickup.pickup_id,
                        "pickup_lat": details_pickup.pickup_lat,
                        "pickup_lng": details_pickup.pickup_lng,
                        "user_id": details_pickup.user_id,
                        "description": details_pickup.description
                    }]
                print(pickup)
            
            status = codes.HTTP_200_OK
        except Driver.DoesNotExist:
            response = DRIVER_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"details":  str(e)}
            status = codes.HTTP_400_BAD_REQUEST
            
        return HttpResponse(json.dumps(response), APPLICATION_JSON, status=status)
