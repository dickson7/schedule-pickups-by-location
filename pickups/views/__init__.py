import json
import pytz
from pytz import timezone

from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
from django.conf import settings
from ..models import User, DriverAvailability, Driver, DetailsDriverAvailability, Pickup
from rest_framework import viewsets, permissions
from rest_framework import status as codes
from django.http import HttpResponse
from ..constants import APPLICATION_JSON, HOURS, NUM_TO_HOUR, DRIVER_NOT_FOUND, TZ_LOCAL, DETAILS_DRIVER_AVAILABILITY_NOT_FOUND, OCUPADO, DISPONIBLE
from ..utils import location_driver, save_date_utc, view_date