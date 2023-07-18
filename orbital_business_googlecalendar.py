## pip install google-api-python-client
## pip install apscheduler

from __future__ import print_function

import datetime
import os.path
import pytz
import json

from telegram.ext import Updater, CommandHandler
from time import sleep
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_creds():
    creds = None

    if os.path.exists('userToken.json'):
        creds = Credentials.from_authorized_user_file('userToken.json', SCOPES)
    # If there are no (valid) credentials available, create one after user authorizes
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'calendarCredentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('userToken.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar(creds):
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(cal):
    try:
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = cal.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

def free_meet(cal, startyear, startmonth, startday, endyear, endmonth, endday):
    tz  = pytz.timezone('Asia/Singapore')
    startdt = datetime.datetime(startyear, startmonth, startday).isoformat() + 'Z'
    enddt = datetime.datetime(endyear, endmonth, endday).isoformat() + 'Z'
    # user can choose to select a range of dates or input specific dates
    ## if range of dates:
    datels = [tz.localize(datetime.datetime(startyear, startmonth, startday)) + datetime.timedelta(days=idx) for idx in range(endday-startday+1)]
    #if select dates
    ## datels = [tz.localize(datetime.datetime(dateyear, datemonth, dateday)), tz.localize(datetime.datetime(startyear, startmonth, startday))]

    try:
        # Call the Calendar API
        print('Checking if user is busy on stated dates...')
        events_result = cal.events().list(calendarId='primary', timeMin= startdt,
                                          timeMax = enddt, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('User is free on all days')
            return datels

        # Prints the start and name of events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            if len(start) <= 10: ## full day event
                eventstart = datetime.datetime.strptime(start[0:10], "%Y-%m-%d")
                eventend = datetime.datetime.strptime(end[0:10], "%Y-%m-%d")
                eventdates = [tz.localize(eventstart) + datetime.timedelta(days=idx) for idx in range((eventend - eventstart).days)]
                for d in datels:
                    for e in eventdates:
                        if e == d:
                            del datels[datels.index(d) : datels.index(d) + (eventend - eventstart).days]

            else:
                for d in datels:
                    if start[0:10] == d.strftime("%Y-%m-%d"):
                        datels.remove(d) ## add in condition to specify time specific event planned here
        freedates = []
        if not datels:
            return freedates
        else:
            for d in datels:
                freedates.append(d.strftime("%Y-%m-%d"))
            return freedates

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_avail(cal, startyear, startmonth, startday, endyear, endmonth, endday):
    startdt = datetime.datetime(startyear, startmonth, startday).isoformat() + 'Z'
    enddt = datetime.datetime(endyear, endmonth, endday).isoformat() + 'Z'

    try:
        # Call the Calendar API
        print('You are busy on')
        events_result = cal.events().list(calendarId='primary', timeMin= startdt,
                                          timeMax = enddt, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, end, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

def create_event(cal, name, des, startdt, enddt):
    event = {
    'summary': name,
    'description': des,
    'start': {
        'dateTime': startdt, ## example => '2023-05-28T12:00:00+08:00'
        'timeZone': 'Asia/Singapore',
    },
    'end': {
        'dateTime': enddt, ## example => '2023-05-28T14:00:00+08:00'
        'timeZone': 'Asia/Singapore',
    },
    'attendees': [
        {'email': 'tan.shirer@gmail.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    event = cal.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

'''
def set_reminder(bot, update, job_queue, year, month, day):
    bot.send_message(chat_id = update.message.chat_id, text = "A reminder has been set!")
    t = datetime.datetime(year, month, day)
    job_queue.run_once(reminder_msg, t, context=update)

def reminder_msg(bot, update):
    message = "Hello! This is a reminder that you have an upcoming activity" #: " + event -> where event holds the name of the activity
    bot.send_message(chat_id = update.message.chat_id, text = message)
'''

# ## test with schedule python
# def create_reminder(event):
#     send_scheduled_msg(event)
#     return schedule.CancelJob ## makes it so that the reminder/ Job only happens once

# def send_scheduled_msg(chat_id, event): ## job in scheduler
#     bot = get_bot()
#     message = "Hello! This is a reminder that you have an upcoming activity: " + event
#     return bot.send_message(chat_id, message)

# def make_job(job, reminddate):
#     return schedule.every().day.do(job).tag(reminddate)

# def run_schedule():
#     today = datetime.date.today()
#     while True:
#         jobs_today = schedule.get_jobs(today)

#         for job in jobs_today:
#             schedule.every().day.do(job)

#         schedule.run_pending()
#         sleep(1)

# def free_busy(cal):
#     tz  = pytz.timezone('Asia/Singapore')
#     startdt = tz.localize(datetime.datetime(2023, 6, 1))
#     enddt = tz.localize(datetime.datetime(2023, 5, 30))

#     freebusy_query = {
#       "timeMin": startdt.isoformat(),
#       "timeMax": enddt.isoformat(),
#       "timeZone": 'Asia/Singapore',
#       "items": [{"id": 'pinkyse6@gmail.com'}]
#     }

#     eventsResult = cal.freebusy().query(body=freebusy_query) ## full day events are automatically seen as "free" in google calendar so it won't be flagged as busy
#     #print(json.dumps(eventsResult, indent = 2)) ## to view json response nicely
#     cal_dict = eventsResult['calendars']
#     print("Days user is not free in from " + eventsResult['timeMin'] + " to " + eventsResult['timeMax'])
#     for cal_id in cal_dict:
#         for cal_busy in cal_dict[cal_id]['busy']:
#             print(cal_busy)
