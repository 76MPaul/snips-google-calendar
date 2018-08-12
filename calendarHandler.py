# -*- coding: utf8 -*-

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



import datetime, pytz
import settings
import json
from modules.calendar.calendar_manager import Calendar
from functions.date_manager import Date
from modules.calendar.sentenceGeneratorCalendar import SentenceGeneratorCalendar

class calendarHandler:
    @staticmethod
    def getCalendar(self, intentname, slots):
        
        text = ""
        calendarId = None
        
        """ --- Common var --- """
        timeMin = None
        timeMax = None
        if slots.get("start_datetime", None):
            dateAndGranularity = Date.extract_date(self, slots, 'False')
            if dateAndGranularity.get('dateStart',None) == dateAndGranularity.get('dateTo',None):
                timeMin = dateAndGranularity.get('dateStart',None)
                timeMax = None
                granularity = dateAndGranularity.get('granularity',None)
            else:
                timeMin = dateAndGranularity.get('dateStart',None)
                timeMax = dateAndGranularity.get('dateTo',None)
                granularity = dateAndGranularity.get('granularity',None)
        
        if slots.get("calendarId", None):
            calendarId = slots.get("calendarId", None).get("value", None)
        
        if not calendarId:
            calendarId = 'primary'
        
        """ --- Intents --- """
        
        if intentname == "getEvents":
            maxResults = None
            if slots.get("maxResults", None):
                maxResults = slots.get("maxResults", None).get("value", None)
            if not maxResults:
                maxResults = 10
            
            text = self.calendar.getEvents(CalendarId=calendarId, timeMin=timeMin, maxResults=maxResults, timeMax=timeMax)
        
        if intentname == "addEvent":
            
            summary = ''
            location = ''
            attendees = {}
            if slots.get("summary", None):
                summary = slots.get("summary", None).get("value", "None")
            else:
                summary = "Non défini"
            if slots.get("location", None):
                location = slots.get("location", None).get("value", None)
            if slots.get("attendees", None):
                attendees = slots.get("attendees", None).get("value", None)
            
            results = self.calendar.addEvents(calendarId, summary, location, attendees, timeMin, timeMax)
        
        return text