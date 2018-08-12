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



from __future__ import print_function
from apiclient.discovery import build # pip install --upgrade google-api-python-client
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import settings
from sentenceGeneratorCalendar import SentenceGeneratorCalendar
import dateparser
import json


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class Calendar:
    
    def __init__(self):
        # Setup the Calendar API
        store = file.Storage(settings.DATA_DIR + '/credentials_calendar.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(settings.CALENDAR_CLIENT_SECRET_FILE, settings.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))

        
    """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        """
        
        
    #list(calendarId=*, orderBy=None, showHiddenInvitations=None, timeMin=None, privateExtendedProperty=None, pageToken=None, updatedMin=None, singleEvents=None, alwaysIncludeEmail=None, showDeleted=None, sharedExtendedProperty=None, maxAttendees=None, syncToken=None, iCalUID=None, maxResults=None, timeMax=None, q=None, timeZone=None)
    def getEvents(self, CalendarId='primary', timeMin=None, maxResults=10, timeMax=None):

        if not timeMin:
            timeMin = datetime.datetime.utcnow()
            
        if not timeMax:
            timeMax = datetime.datetime.utcnow()  
            timeMax = timeMax + datetime.timedelta(days=1)
            
        interval = self._interval(timeMin, timeMax)
        fromToday = self._fromToday(timeMin)
            
        timeMin = timeMin.replace(tzinfo=None).isoformat() + 'Z' # 'Z' 
        timeMax = timeMax.replace(tzinfo=None).isoformat() + 'Z' # 'Z'
        
        print("timeMin : " + timeMin)
        print("timeMax : " + timeMax)
        
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=CalendarId, timeMin=timeMin, maxResults=maxResults, singleEvents=True, orderBy='startTime', timeMax=timeMax).execute()
        events = events_result.get('items', [])
        
        result = []
        
        if not events:
            print('No upcoming events found.')
        
        for event in events:
            start = event.get('start',None).get('dateTime', None) 
            end = event.get('end',None).get('dateTime', None) 
            
            organizer = event.get('displayName',None)
            attendees = event.get('attendees',None)
            location = event.get('location',None)
            description = event.get('description',None)
            summary = event.get('summary',None)

            result.append({'start':start, 'organizer':organizer, 'attendees':attendees, 'location':location, 'description':description, 'end':end, 'summary':summary})
            
        text = SentenceGeneratorCalendar.generate_sentence_event(self, result, interval, fromToday)

        return text
    
    def _interval(self, timeMin, timeMax):
        if timeMax <> None:
            ptimeMin = timeMin.replace(tzinfo=None)
            ptimeMax = timeMax.replace(tzinfo=None)
            delta_days = (ptimeMax - ptimeMin).days
            if delta_days > 1:
                return delta_days
            else:
                return 0
        else:
            return 0
            
    def _fromToday(self, timeMin):
        ptimeMin = int(timeMin.strftime("%d"))
        now = int(datetime.datetime.utcnow().strftime("%d"))
        delta_days = (ptimeMin - now)
        if delta_days < 0:
            return 0
        else:
            return delta_days
         
        
        
        
    #insert(calendarId=*, body=*, sendNotifications=None, supportsAttachments=None, conferenceDataVersion=None, maxAttendees=None)
    
    def addEvents(self, calendarId, summary, location, attendees, timeMin, timeMax):
        
        if not timeMin:
            timeMin = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            
        if not timeMax:
            timeMax = timeMin + datetime.timedelta(hours=1)
        
        creator = {"self":True,"displayName":"Paul MAGNIER","email":"contact@paulmagnier.fr"}
        """creator {
                self -> True
                displayName -> str 
                email -> str}"""
        """organizer {
                self -> true
                displayName -> str 
                email -> str}"""
        summary = summary
        """pattendees = {}
        for attendee in attendees
        attendees 
                [{displayName -> str
                self -> bool
                email -> str
                organizer -> bool}]"""
        start = {"dateTime": timeMin.isoformat("T")} #"date":timeMin.replace(tzinfo=None).strftime("%Y-%m-%d"),
        location =  location 
        visibility = "default" 
        end = {"dateTime": timeMax.isoformat("T")} #"date":timeMax.replace(tzinfo=None).strftime("%Y-%m-%d"),
        #source = {"title":"Create by snips"}
        kind = "event" 
        #reminders = {"useDefault":True} #{"overrides":[{"minutes":30, method:"email"}, {"minutes":30, method:"popup"}]}
        
        body = {
        "summary":  summary,
        "location":  location,
        "creator":  creator,
        "start":  start,
        "end":  end,
        "kind":  kind,
        } #"reminders": reminders, "source":  source, "visibility":  visibility,
        
        events_result = self.service.events().insert(calendarId=calendarId, body=body).execute() # , sendNotifications=True, supportsAttachments=None, conferenceDataVersion=None, maxAttendees=None
        #print('Event created: %s' % (events_result.get('htmlLink')))

        return 'ajouté'
    
    #delete(calendarId=*, eventId=*, sendNotifications=None)
    #get(calendarId=*, eventId=*, alwaysIncludeEmail=None, timeZone=None, maxAttendees=None)
    #import_(calendarId=*, body=*, supportsAttachments=None, conferenceDataVersion=None)
    #instances(calendarId=*, eventId=*, timeMin=None, showDeleted=None, alwaysIncludeEmail=None, pageToken=None, maxAttendees=None, maxResults=None, timeMax=None, timeZone=None, originalStart=None)
    #instances_next(previous_request=*, previous_response=*)
    #list_next(previous_request=*, previous_response=*)
    #move(calendarId=*, eventId=*, destination=*, sendNotifications=None)
    #patch(calendarId=*, eventId=*, body=*, sendNotifications=None, alwaysIncludeEmail=None, supportsAttachments=None, conferenceDataVersion=None, maxAttendees=None)
    #quickAdd(calendarId=*, text=*, sendNotifications=None)
    #update(calendarId=*, eventId=*, body=*, sendNotifications=None, alwaysIncludeEmail=None, supportsAttachments=None, conferenceDataVersion=None, maxAttendees=None)
    """def update(self, calendarId='primary', eventId=*, body=*, sendNotifications=None, alwaysIncludeEmail=None, supportsAttachments=None, conferenceDataVersion=None, maxAttendees=None):
        return None"""
        
    #watch(calendarId=*, body=*, orderBy=None, showHiddenInvitations=None, timeMin=None, privateExtendedProperty=None, pageToken=None, updatedMin=None, singleEvents=None, alwaysIncludeEmail=None, showDeleted=None, sharedExtendedProperty=None, maxAttendees=None, syncToken=None, iCalUID=None, maxResults=None, timeMax=None, q=None, timeZone=None)
    
    