#Snips-Google-Calendar

Ce module développer pour Snips vous permet de gérer votre calendrier Google.
Il permet actuellement : 
  - de récupérer et vous énoncer les différents événements à venir de votre calendrier,
  - Ajouter de nouveaux événements à votre calendrier.

##Usages :

Ce module s'intègre dans votre gestionnaire d'événements Snips.

  - Créer une instance de calendar manager :
  ```
    from modules.calendar.calendar_manager import Calendar
  	self.calendar = Calendar()
  ```
  - Appeler calendarHandler pour gérer l'événement
  ```
  	text = calendarHandler.getCalendar(self, intentname, slots)
  ```

##Todo :

  - suppression d'événements
  - Prise en compte d'autres calendriers pour l'ajout d'événements**

##Changelog :

  - 10/08/2018 - Initial Commit
