import requests
import json
import pytz
from pytz import timezone

from datetime import datetime, timedelta
from .constants import  TZ_LOCAL

def location_driver(id=None):
    url = "https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json"
    response = requests.get(url)
    data= json.loads(response.text)
    location={}
    if id:
        for alfred in data['alfreds']:
            if alfred["id"] == id:
                location={
                    "lng":alfred["lng"],
                    "lat":alfred["lat"]
                }
        return location
    else:
        return data['alfreds']
    
    
def save_date_utc(date):
    tz_local = pytz.timezone(TZ_LOCAL)
    publish_date = datetime.strptime(
        date, "%Y-%m-%d %H:%M:%S"
    )
    cest_local = tz_local.localize(publish_date, is_dst=True)
    date = cest_local.astimezone(pytz.utc)
    return date

def view_date(date):
    return date.astimezone(timezone(TZ_LOCAL))