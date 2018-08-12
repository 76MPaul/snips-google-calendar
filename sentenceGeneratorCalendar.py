# -*- coding: utf-8 -*-

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



import datetime
from enum import Enum
import locale
import random
from functions.date_manager import Date
import sys

class SentenceGeneratorCalendar(object):
    @staticmethod
    def generate_sentence_introduction(self, tone):
        
        sentence_beginning = ""
        
        return sentence_beginning
    
    @staticmethod
    def generate_sentence_event(self, events, nbDays, fromToday):
        """
        :param tone:
        :return: an introduction string
        """
        
        reload(sys)
        sys.setdefaultencoding('utf8')
        
        text = ""
        
        nombreEvenement = len(events)
        now = datetime.datetime.utcnow()
        
        
        if nbDays < 2:
            if options3.get(fromToday, None):
                days = options3.get(fromToday, None)
            elif fromToday < 7:
                day = now + datetime.timedelta(days=nbDays)
                days = day.strftime("%A")
            else:
                day = now + datetime.timedelta(days=nbDays)
                days = "le " +  day.strftime("%d")
        elif nbDays == 7:
            days = "cette semaine"
        else:
            days = "sur les {} prochains jours".format(nbDays)
        
        if nombreEvenement > 0:
            if nombreEvenement == 1:
                s = ""
            else:
                s = "s"
            part0 = "Vous avez {} événement{} à effectuer {}. ".format(nombreEvenement, s, days)
        else:
            part0 = "Vous n'avez pas d'événements à effectuer {}. ".format(days)
            
        text = text + part0
        
        for event in events:
            part3 = "" # 'Vous devriez partir à {}, vous aurez au moins {} de temps de route.' #
            
            """ -- Event date -- """
            granularity = 0
            if event['start'] and event['end']:
                if nbDays < 2:
                    start = event['start'].strftime("de %H heures %M") 
                else:
                    start = event['start'].strftime("le %d de %H heures %M")
                
                end = event['end'].strftime("%H heures %M") 
                part2Bis = ' {} à {}'.format(start, end)
            elif event['start'] and not event['end']:
                if nbDays < 2:
                    start = date_to_string(event['start'], granularity=granularity).strftime("à %H heures %M")
                else:
                    start = date_to_string(event['start'], granularity=granularity).strftime("le %d à %H heures %M")
                    
                part2Bis = ' {}'.format(start)
            else:
                part2Bis = ""
            
            """ -- Event location -- """
            if event['location']:
                location = " " + event['location']
            else:
                location = ""
            
            """ -- Event organizer -- """
            if event['organizer']:
                organizer = event['organizer']
                part11 = 'oragnisé par {}. '.format(organizer)
            else :
                part11 = ""
                organizer = ""
            
            """ -- Event summary -- """
            if event['summary']:
                summary = event['summary']
            else:
                summary = ""
            
            """ -- Event attendees -- """
            if event['attendees']:
                attendees = event['attendees']
                if nombre > 1:
                    part4 = '{} {}. '.format(options2[nombre], attendees)
                else:
                    part4 = '{} {}. '.format(attendees, options2[nombre])
            else:
                attendees = ""
                part4 = ""
            
            """ -- Event description -- """
            if event['description']:
                description = event['description']
            else:
                description = ""

            """ -- Assemble text -- """
            if events.index(event) == 0:
                if nombreEvenement == 1:
                    part1 = 'Vous avez {} {}. '.format(summary, part11) #summary - 
                else:
                    part1 = 'Vous aurez à commencer par {} {}. '.format(summary, part11) #summary - 
            elif events.index(event) == 1:
                part1 = 'Vous avez ensuite {} {}. '.format(summary, part11)
            elif events.index(event) == len(events)-1:
                part1 = 'Et enfin {} {}. '.format(summary, part11)
            else:
                part1 = 'Puis {} {}. '.format(summary, part11)
            
            nombre = random.randint(0, 3)
            part2 = 'Vous {}{}{}. '.format(options1[nombre], location, part2Bis)
            

            text = text + part1 + part2 + part3 + part4
            
        return text
        
    
options1 = {0 : 'êtes attendus',
            1 : 'serez attendus',
            2 : 'devrez être',
            3 : 'êtes conviés',
}

options2 = {0 : 'Accompagné de ',
            1 : 'Vous serez avec ',
            2 : 'participierons',
            3 : 'sont attendus',
}

options3 = {0 : "aujourd'hui",
            1 : "demain",
            2 : "apprès-demain",
            7 : "prochain",
            8 : "prochain",
            9 : "prochain",
            10 : "prochain",
            11 : "prochain",
            12 : "prochain",
            13 : "prochain",
}

"""if french_is_masculine_word(Country) and (not starts_with_vowel(Country)):
        return "au {}".format(Country)
    else:
        return "en {}".format(Country)
        
    
    
def date_to_string(date, granularity=0):
    ""Convert a date to a string, with an appropriate level of
        granularity.

    :param date: A datetime object.
    :param granularity: Granularity for the desired textual representation.
                        0: precise (date and time are returned)
                        1: day (only the week day is returned)
                        2: month (only year and month are returned)
                        3: year (only year is returned)
    :return: A textual representation of the date.
    ""
    if not date:
        return ""

    if granularity == 0:
        return date.strftime("%A")
    elif granularity == 1:
        return date.strftime("%A, %d")
    elif granularity == 2:
        return date.strftime("%A, %d %B")

    return date.strftime("%A, %d %B, %H:%M%p")
    
def french_is_masculine_word(word):
    return word[len(word) - 1] not in ['é', 'e']
    
def starts_with_vowel(word):
    return word[0] in ['a', 'e', 'i', 'o', 'u', 'y']
        
    
        """