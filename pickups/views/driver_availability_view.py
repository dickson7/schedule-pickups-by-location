from .__init__ import *

class DriverAvailabilityView(GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        params = {key: value for key, value in request.GET.items()}
        
        response = {}
        hours_availability=[]
        
        try:
            driver = Driver.objects.get(id=params["driver_id"])
            date = save_date_utc(params["date"])
            driver_availability = DriverAvailability.objects.filter(
                driver=driver,
                date__year=date.year,
                date__month=date.month,
                date__day=date.day,
                ).first()
            if driver_availability:
                response["id"] = driver.id
                response["name"] = driver.name
                response["location"] = location_driver(driver.id)
                response["date_availability"]=[]
                details= DetailsDriverAvailability.objects.filter(
                        driver_availability=driver_availability.id,
                        date__year=driver_availability.date.year,
                        date__month=driver_availability.date.month,
                        date__day=driver_availability.date.day,
                    ).order_by("driver_availability")

                details_pickup = {}
                for detail in details:
                    if detail.status == OCUPADO:
                        pickup = Pickup.objects.get(id=detail.pickup_id)
                        details_pickup = {
                            "pickup_id":pickup.id,
                            "user_id":pickup.user_id,
                            "target_lng":pickup.target_lng,
                            "target_lat":pickup.target_lat,
                            "description":pickup.description
                        }
                    hours_availability.append({
                        "id":detail.id,
                        "hour": NUM_TO_HOUR[str(view_date(detail.date).hour)],
                        "status": detail.status,
                        "details": details_pickup
                    })
                    details_pickup={}
                    
                response["date_availability"]=[{
                        "date":datetime.strftime((view_date(date)),'%Y-%m-%d'),
                        "hours": hours_availability
                        }]
                        
            status = codes.HTTP_200_OK
        except Driver.DoesNotExist:
            response = DRIVER_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"details":  str(e)}
            status = codes.HTTP_400_BAD_REQUEST
            
        return HttpResponse(json.dumps(response), APPLICATION_JSON, status=status)

    
    def post(self, request, *args, **kwargs):
        params = request.data.copy()
        response = {}
        hours=[]
        try:
            driver = Driver.objects.get(id=params["driver_id"])
            date = save_date_utc(params["date"])
            availability = DriverAvailability.objects.filter(
                driver=driver,
                date__range=(date, (date + timedelta(hours=params["hours_availability"]))))
            if availability:
                raise Exception("Ya tiene agenda programada para este dia")
            driver_availability = DriverAvailability.objects.create(
                driver=driver,
                date=date,
                hours_availability=params["hours_availability"],
            )
            
            for i in range(params["hours_availability"]):
                details= DetailsDriverAvailability.objects.create(
                    driver_availability=driver_availability.id,
                    date=driver_availability.date+timedelta(hours=i),
                    hour=NUM_TO_HOUR[str(view_date(driver_availability.date+timedelta(hours=i)).hour)],
                    driver=driver
                )
                
                hours.append({
                    "id":details.id,
                    "hour": NUM_TO_HOUR[str(view_date(details.date).hour)],
                    "status": details.status,
                    
                })
                
            response = {
                "id": driver.id,
                "name":driver.name,
                "date_availability":[{
                    "date":str(view_date(date)),
                    "hours": hours
                    }]
                    
            }
            status = codes.HTTP_200_OK
        except Driver.DoesNotExist:
            response = DRIVER_NOT_FOUND
            status = codes.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"details":  str(e)}
            status = codes.HTTP_400_BAD_REQUEST
            
        return HttpResponse(json.dumps(response), APPLICATION_JSON, status=status)