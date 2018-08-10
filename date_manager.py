# Copyright (C) <2018>  <MAGNIER Paul>

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from geopy.geocoders import GoogleV3 #Nominatim #pip install geopy
from tzwhere import tzwhere #pip install tzwhere
from datetime import *
import pytz
import settings
import log
import dateparser #pip install dateparser



class Date:
    @staticmethod
    def extract_date(self, slots, utc):
        
        #print(slots)
        
        interval = False
        
        if utc == 'True':
            if slots.get("locality", None):
                Locality = slots.get("locality", None).get("value", None)
            
            if slots.get("country", None):
                Country = slots.get("country", None).get("value", None)
                
            if slots.get("region", None):
                Region = slots.get("region", None).get("value", None)
                
            if slots.get("geographical_poi", None):
                POI = slots.get("geographical_poi", None).get("value", None)
            
            geolocator = GoogleV3(api_key=settings.GEOLOCALISATION_API) #Nominatim()
            
            if Locality or Country or Region:
                if (Locality):
                    place, (lat, lng) = geolocator.geocode(Locality) #g.geocode(Locality)
                elif (Country):
                    place, (lat, lng) = geolocator.geocode(Country) #g.geocode(Country)
                elif (Region):
                    place, (lat, lng) = geolocator.geocode(Region) #g.geocode(Region)
            else:
                Locality = settings.DEFAULT_CITY_NAME
                place, (lat, lng) = geolocator.geocode(Locality) #g.geocode(Locality)
            
            w = tzwhere.tzwhere()

            local_tz = pytz.timezone(w.tzNameAt(float(lat), float(lng)))
        
        dateTo = None
        dateFrom = None
        type = "none"
        
        grain = None
        if slots.get("start_datetime", None):
            grain = slots.get("start_datetime", None).get("grain", None)
        
        if slots.get("start_datetime", None):
            type = slots.get("start_datetime", None).get("kind", None)
        
        if (type == "InstantTime"):
            log.debug('InstantTime')
            dateFrom = slots.get("start_datetime", None).get("value", None)
            dateFrom = dateparser.parse(dateFrom)
            dateTo = dateFrom
            if grain:
                if grain == "Day":
                    dateFrom = dateFrom.replace(hour=0)
                    dateTo = dateTo.replace(hour=23)
                    

        elif (type == "TimeInterval"):
            interval = True
            dateTo = slots.get("start_datetime", None).get("to", None)
            dateFrom = slots.get("start_datetime", None).get("from", None)
            dateTo = dateparser.parse(dateTo)
            dateFrom = dateparser.parse(dateFrom)
        else:
            log.debug('Neither instant time nor interval')
            dateFrom = datetime.now()
            dateFrom = dateFrom + timedelta(hours=1)
            dateTo = dateFrom
        
        now = datetime.now().replace(tzinfo=None)
        delta_hours = (dateFrom.replace(tzinfo=None) - now).seconds//3600
        delta_days = (dateFrom.replace(tzinfo=None) - now).days
        if delta_hours == 0 or delta_hours < 0:
            dateFrom = datetime.now().replace(tzinfo=None)
            dateFrom = now + timedelta(hours=1)
            dateTo = dateTo.replace(tzinfo=None)
        
        # Determine granularity
        granularity = None
        if dateFrom:  # We have an information about the date.
            if delta_days > 10: # There a week difference between today and the date we want the forecast.
              granularity = 2 # Give the day of the forecast date, plus the number of the day in the month.
            elif delta_days > 5: # There a 10-day difference between today and the date we want the forecast.
              granularity = 1 # Give the full date
            else:
              granularity = 0 # Just give the day of the week
        else:
            granularity = 0
            
        if utc == 'True':
            #log.debug('utc')
            dateFrom = dateFrom.replace(tzinfo=local_tz)
            dateTo = dateTo.replace(tzinfo=local_tz)
        
        data = {"dateStart": dateFrom, "dateTo": dateTo,"granularity": granularity}
        return data
