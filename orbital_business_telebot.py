from orbital_business_activity import *
from orbital_business_googlecalendar import *

import warnings
warnings.filterwarnings('ignore')

import telebot
import schedule
import random
import logging
import datetime
from datetime import date, timedelta
from dateutil.parser import parse
from collections import Counter

##pip install python-telegram-bot
##pip install python-telegram-bot-calendar

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import ConversationHandler, CallbackContext
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

BOT_USERNAME = "@gaigai_bot"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, USER_INPUT_ACTIVITY, CALENDAR, TIME, INFORMATION, MAIN, FOOD_LST, CONSOLIDATE, POLL_ANSWERS, USER_INPUT_SCHEDULES, GROUP_INPUT_DATE, GROUP_INPUT_ACTIVITY, USER_INPUT_GOOGLE_CALENDAR, REMIND, USER_INPUT_REMINDER, USER_INPUT_REVIEWS, REVIEWS, PAST_REVIEW = range(23)
# Callback data
PLAN, UPCOMING, PAST, HELP, YES, NO, CHANGE_DATE, KEEP_DATE, KEEP_TIME, KEEP_DATE_2, ACTIVITY, CATEGORY, ADVENTURE, ATTRACTION, FOOD, OTHER, ACTIVITY_OPTION_1, ACTIVITY_OPTION_2, ACTIVITY_OPTION_3, ACTIVITY_RESULT_1, ACTIVITY_RESULT_2, ACTIVITY_RESULT_3, MORE, SELECTED, DECLINE, MENU, END, BACK, SCHEDULES, INPUT_PERIOD, LINK_GOOGLE_CALENDAR, INPUT_REMINDER_DATE, NO_REMINDER, MONTHLY_REMINDER, CONFIRMATION = range(35)
CONSOLIDATE_POLL, GROUP_ACTIVITY, GROUP_DATE, SELECT_ACTIVITY, GROUP_SESSION, GROUP_MENU, GROUP_CATEGORY, GROUP_DATE = range(8)

########################################
############ STORED DATA ###############
########################################

START = []
GROUP = []
DONE = []

ID_LIST = []
GROUP_ID = []
CONTROL_MAN = []

DATES = []
TYPED_SCHEDULE = []
INPUT_GOOGLE_CALENDAR = []
CONFIRM_DATE = []
GROUP_CONFIRM_DATE = []
GROUP_CONFIRM_ACTIVITY = []

checkbox_time = ['Morning', 'Afternoon', 'Night']
CONFIRM_TIME = []

food_time = ['Breakfast Menu', 'Lunch Menu', 'Dinner Menu']
SELECTED_FOOD = []

ACTIVITIES = []
SELECT_PAST_ACTIVITY = []

CONFIRM_MEETING = []

TOTAL_VOTER_COUNT = []
POLL_LIST = []

REMINDER_DATE = []

PAST_ACTIVITY = []
REVIEW_LST = []
RATING_LIST = ['\u2B50', '\u2B50 \u2B50', '\u2B50 \u2B50 \u2B50', '\u2B50 \u2B50 \u2B50 \u2B50', '\u2B50 \u2B50 \u2B50 \u2B50 \u2B50']
USER_REVIEW = {}

review_hour = 0
review_min = 7

########################################
########### COMMON COMMANDS ############
########################################

def start_command(update, context):
    message_type = update.message.chat.type
    user = update.message.from_user
    text = update.message.text
    if message_type == 'group':
        group_name = update.message.chat.title
        GROUP.append(group_name)
        GROUP_ID.append(update.message.chat.id)
        CONTROL_MAN.append(user.first_name)
        logger.info("User %s started the conversation in %s.", user.first_name, group_name)
        numOfMembers = context.bot.get_chat_member_count(update.message.chat.id)
        TOTAL_VOTER_COUNT.append(numOfMembers - 1) #dont count the bot
        keyboard = [
            [InlineKeyboardButton("View Results", callback_data=str(CONSOLIDATE_POLL))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=f"Hello Everyone! Welcome to GaiGai Bot! \U0001F60A \nI am here to help you all plan a meet-up session. \n\nClick the link below and it will bring you to a private message with me to start planning! \nhttp://telegram.me/gaigai_bot?start=start \n\nYou may also click 'View Results' to look at the consolidated date and activity!", 
                                reply_markup=reply_markup)
        return CONSOLIDATE          
    else:
        logger.info("User %s started the conversation.", user.first_name)
        if user not in START:
            START.append(user)
            keyboard = [
                [InlineKeyboardButton("Plan an activity", callback_data=str(PLAN))],
                [InlineKeyboardButton("Upcoming activities", callback_data=str(UPCOMING))],
                [InlineKeyboardButton("Past activities", callback_data=str(PAST))],
                [InlineKeyboardButton("Help", callback_data=str(HELP))],
                [InlineKeyboardButton("Exit", callback_data=str(END))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                f"Hello {user.first_name} ! \U0001F44B I'm GaiGai bot. \nThis bot can help you plan a meetup with your friends! \n\nSimply click the options below to start planning!",
                reply_markup=reply_markup
            )
        else:
            keyboard = [
                [InlineKeyboardButton("Plan an activity", callback_data=str(PLAN))],
                [InlineKeyboardButton("Upcoming activities", callback_data=str(UPCOMING))],
                [InlineKeyboardButton("Past activities", callback_data=str(PAST))],
                [InlineKeyboardButton("Help", callback_data=str(HELP))],
                [InlineKeyboardButton("Exit", callback_data=str(END))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                f"GaiGai Bot has restarted. \nClick the options below to start planning!",
                reply_markup=reply_markup
            )
        return FIRST
    

########################################
############ FIRST BUTTON ##############
########################################

def menu(update, context):
    query = update.callback_query
    SELECT_PAST_ACTIVITY.clear()
    keyboard = [
        [InlineKeyboardButton("Plan an activity", callback_data=str(PLAN))],
        [InlineKeyboardButton("Upcoming activities", callback_data=str(UPCOMING))],
        [InlineKeyboardButton("Past activities", callback_data=str(PAST))],
        [InlineKeyboardButton("Exit", callback_data=str(END))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        f"Welcome to GaiGai Bot Menu! \U0001F916 \nClick the options below to continue",
        reply_markup=reply_markup
    )
    return FIRST

def plan(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(YES)),
         InlineKeyboardButton("No", callback_data=str(NO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text=f"Do you have a specific date for the meetup? \U0001F4C5",
        reply_markup=reply_markup
    )
    return SECOND

def upcoming(update, context):
    query = update.callback_query
    if CONFIRM_MEETING == []:
        if query.message.chat.type == "private":
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(PLAN)),
                InlineKeyboardButton("No", callback_data=str(MENU))]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(PLAN)),
                InlineKeyboardButton("No", callback_data=str(GROUP_MENU))]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="You do not have any upcoming activities. \nDo you want to start planning?",
            reply_markup=reply_markup
        )
        return FIRST
    else:
        keyboard = []
        for session in CONFIRM_MEETING:
            button = [InlineKeyboardButton(session, callback_data=session)]
            keyboard.append(button)
        if query.message.chat.type == "private":
            back = [InlineKeyboardButton("Back", callback_data=str(MENU))]
        else:
            back = [InlineKeyboardButton("Back", callback_data=str(GROUP_MENU))]
        keyboard.append(back)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="Click to view more details!",
            reply_markup=reply_markup
        )
        return INFORMATION

def past(update, context):
    query = update.callback_query
    if PAST_ACTIVITY == [] and CONFIRM_MEETING == []:
        if query.message.chat.type == "private":
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(PLAN)),
                InlineKeyboardButton("No", callback_data=str(MENU))]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(PLAN)),
                InlineKeyboardButton("No", callback_data=str(GROUP_MENU))]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="You do not have any past activities. \nDo you want to start planning?",
            reply_markup=reply_markup
        )
        return FIRST
    elif PAST_ACTIVITY == [] and CONFIRM_MEETING != []:
        if query.message.chat.type == "private":
            keyboard = [
                [InlineKeyboardButton("Upcoming Activity", callback_data=str(UPCOMING)),
                InlineKeyboardButton("Plan Activity", callback_data=str(PLAN))],
                [InlineKeyboardButton("Back", callback_data=str(MENU))],
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Upcoming Activity", callback_data=str(UPCOMING))],
                [InlineKeyboardButton("Back", callback_data=str(GROUP_MENU))],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="You do not have any past activities. \nBut you have an upcoming activity. \n\nPlease select one",
            reply_markup=reply_markup
        )
        return FIRST
    else:
        keyboard = []
        for key in PAST_ACTIVITY:
            button = [InlineKeyboardButton(key, callback_data=key)]
            if button not in keyboard:
                keyboard.append(button)
        if query.message.chat.type == "private":
            back = [InlineKeyboardButton("Back", callback_data=str(MENU))]
        else:
            back = [InlineKeyboardButton("Back", callback_data=str(GROUP_MENU))]
        keyboard.append(back)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="Select one",
            reply_markup=reply_markup
        )
        return PAST_REVIEW

def help(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Back", callback_data=str(MENU))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f'Thank you for choosing GaiGai Bot! \U0001F916 \nI am here to help you plan a meet-up session with your friends! \n\nYou may choose to add me in your group and click "/start" to plan OR you can also start planning at personal chat!',
                             reply_markup=reply_markup)
    return MAIN

########################################
########### SECOND BUTTON ##############
########################################

def yes(update, context):
    query = update.callback_query
    today = date.today()
    calendar, step = DetailedTelegramCalendar(min_date=today).build()
    query.message.reply_text(
        text=f"Select {LSTEP[step]}",
		reply_markup=calendar
	)
    return CALENDAR
    
def change_date(update, context):
    query = update.callback_query
    today = date.today()
    calendar, step = DetailedTelegramCalendar(min_date=today).build()
    query.message.reply_text(
        text=f"Select {LSTEP[step]}",
		reply_markup=calendar
	)
    return CALENDAR

def keep_date(update, context):
    query = update.callback_query
    for session in CONFIRM_MEETING:
        if DATES[-1] in session:
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(CHANGE_DATE)),
                InlineKeyboardButton("No", callback_data=str(KEEP_DATE_2))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(f"You have a meeting on this date. \n\nDetails: \n{session}. \n\nWould like to change the date?", reply_markup=reply_markup)
            return SECOND
    keep_date_2(update, context)
    return TIME

def keep_date_2(update, context):
    query = update.callback_query
    keyboard = []
    for label in checkbox_time:
        check = [InlineKeyboardButton(label, callback_data=label)]
        keyboard.append(check)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"What time will be your meet-up session? \u23F0 \nYou may select more than one", reply_markup=reply_markup)
    return TIME

def no(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Link To Google Calendar", callback_data=str(INPUT_PERIOD))],
        [InlineKeyboardButton("Type In Your Free Date(s)", callback_data=str(SCHEDULES))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text=f"Link to Google Calendar or type in your schedules now! \U0001F4C5",
        reply_markup=reply_markup
    )
    return SECOND

def input_period(update, context):
    query = update.callback_query
    TYPED_SCHEDULE.clear()
    query.message.reply_text("Before bringing you the authentication page, please type in the period you wish to extract.") 
    query.message.reply_text("Please type in this format \n\nStart: YYYY-MM-DD \nEnd: YYYY-MM-DD \n\nEg. \n2023-07-01 \n2023-07-30")
    return USER_INPUT_GOOGLE_CALENDAR

def link_google_calendar(update, context):
    query = update.callback_query
    start_date = INPUT_GOOGLE_CALENDAR[0].split("-")
    end_date = INPUT_GOOGLE_CALENDAR[-1].split("-")
    creds = get_creds()
    cal = get_calendar(creds)
    lst = free_meet(cal, int(start_date[0]), int(start_date[1]), int(start_date[2]), int(end_date[0]), int(end_date[1]), int(end_date[2]))
    if lst == []:
        keyboard = [
            [InlineKeyboardButton("Input new period", callback_data=str(INPUT_PERIOD))],
            [InlineKeyboardButton("Type In Your Free Date(s)", callback_data=str(SCHEDULES))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("You have no free dates. \nPlease select one", reply_markup=reply_markup)
        return SECOND
    else:
        str = ""
        for free_date in lst:
            CONFIRM_DATE.append(free_date)
            if str == "":
                str += free_date
            else:
                str = str + " \n" + free_date 
        query.message.reply_text(f"Your free dates are: \n{str}")
        if SELECT_PAST_ACTIVITY == []:
            select_activity(update, context)
        else:
            confirmation(update, SELECT_PAST_ACTIVITY[-1])
        return THIRD


########################################
############ THIRD BUTTON ##############
########################################

def category(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Adventure", callback_data=str(ADVENTURE))],
        [InlineKeyboardButton("Attractions", callback_data=str(ATTRACTION))],
        [InlineKeyboardButton("Food/Dining", callback_data=str(FOOD))],
        [InlineKeyboardButton("Others", callback_data=str(OTHER))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Choose the category of the activity!", reply_markup=reply_markup)
    return FOURTH

def activity(update, context):
    query = update.callback_query
    query.message.reply_text("Type in what you wish to do! \nEg. BBQ, Escape Room, Theme Park, Picnic etc")
    return USER_INPUT_ACTIVITY

def schedules(update, context):
    query = update.callback_query
    TYPED_SCHEDULE.clear()
    query.message.reply_text("Type in your schedule(s) in this format. \n\nYYYY-MM-DD (TIME) \nYYYY-MM-DD (TIME)")
    return USER_INPUT_SCHEDULES


########################################
########### FOURTH BUTTON ##############
########################################

def adventure(update, context):
    query = update.callback_query
    lst = activity_lst("Adventure activities")
    max = len(lst) - 1
    index1 = random.randint(0, max)
    index2 = random.randint(0, max)
    index3 = random.randint(0, max)
    A1 = lst[index1]
    while index2 == index1:
        index2 = random.randint(0, max)
    A2 = lst[index2]
    while index3 == index1 or index3 == index2:
        index3 = random.randint(0, max)
    A3 = lst[index3]
    keyboard = [
        [InlineKeyboardButton(A1, callback_data=str(ACTIVITY_OPTION_1))],
        [InlineKeyboardButton(A2, callback_data=str(ACTIVITY_OPTION_2))],
        [InlineKeyboardButton(A3, callback_data=str(ACTIVITY_OPTION_3))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"These are the 3 adventure activites you can do in Singapore! Select them to view the details", reply_markup=reply_markup)
    return FIFTH

def attraction(update, context):
    query = update.callback_query
    index1 = random.randint(0, 14)
    index2 = random.randint(0, 14)
    index3 = random.randint(0, 14)
    A1 = attraction_api(index1)
    while index2 == index1:
        index2 = random.randint(0, 14)
    A2 = attraction_api(index2)
    while index3 == index1 or index3 == index2:
        index3 = random.randint(0, 14)
    A3 = attraction_api(index3)
    keyboard = [
        [InlineKeyboardButton(A1, callback_data=str(ACTIVITY_RESULT_1))],
        [InlineKeyboardButton(A2, callback_data=str(ACTIVITY_RESULT_2))],
        [InlineKeyboardButton(A3, callback_data=str(ACTIVITY_RESULT_3))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"These are the 3 attractions you can visit in Singapore! Select them to view the details", reply_markup=reply_markup)
    return FIFTH

def food(update, context):
    query = update.callback_query
    keyboard = []
    for f in food_time:
        check = [InlineKeyboardButton(f, callback_data=f)]
        keyboard.append(check)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Choose 1", reply_markup=reply_markup)
    return FOOD_LST

def food_lst(update, context):
    query = update.callback_query
    SELECTED_FOOD.append(query.data)
    lst = restaurant_lst(query.data)
    A1 = lst[0]
    A2 = lst[1]
    A3 = lst[2]
    keyboard = [
        [InlineKeyboardButton(A1, callback_data=str(ACTIVITY_RESULT_1))],
        [InlineKeyboardButton(A2, callback_data=str(ACTIVITY_RESULT_2))],
        [InlineKeyboardButton(A3, callback_data=str(ACTIVITY_RESULT_3))],
        [InlineKeyboardButton("More Options", callback_data=str(MORE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"These are the 3 restaturants you can enjoy in Singapore! Select them to view the details or choose more options for choices!", reply_markup=reply_markup)
    return FIFTH

def more(update, context):
    query = update.callback_query
    lst = activity_lst(SELECTED_FOOD[-1])
    max = len(lst) - 1
    index1 = random.randint(0, max)
    index2 = random.randint(0, max)
    index3 = random.randint(0, max)
    A1 = lst[index1]
    while index2 == index1:
        index2 = random.randint(0, max)
    A2 = lst[index2]
    while index3 == index1 or index3 == index2:
        index3 = random.randint(0, max)
    A3 = lst[index3]
    keyboard = [
        [InlineKeyboardButton(A1, callback_data=str(ACTIVITY_OPTION_1))],
        [InlineKeyboardButton(A2, callback_data=str(ACTIVITY_OPTION_2))],
        [InlineKeyboardButton(A3, callback_data=str(ACTIVITY_OPTION_3))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"Here are more choices for you! Select them to view the details", reply_markup=reply_markup)
    return FIFTH


########################################
############ FIFTH BUTTON ##############
########################################

def activity_option_1(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[0][0]["text"]
    AD1_img = image_api(A1)
    context.bot.sendPhoto(chat_id=query.message.chat_id, photo=AD1_img, caption=f"Image of {A1}")
    activity_option(query, A1)
    return SIXTH

def activity_option_2(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[1][0]["text"]
    AD1_img = image_api(A1)
    context.bot.sendPhoto(chat_id=query.message.chat_id, photo=AD1_img, caption=f"Image of {A1}")
    activity_option(query, A1)
    return SIXTH

def activity_option_3(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[2][0]["text"]
    AD1_img = image_api(A1)
    context.bot.sendPhoto(chat_id=query.message.chat_id, photo=AD1_img, caption=f"Image of {A1}")
    activity_option(query, A1)
    return SIXTH

def activity_result_1(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[0][0]["text"]
    activity_result(context, query, A1)
    return SIXTH

def activity_result_2(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[1][0]["text"]
    activity_result(context, query, A1)
    return SIXTH

def activity_result_3(update, context):
    query = update.callback_query
    A1 = query.message.reply_markup.inline_keyboard[2][0]["text"]
    activity_result(context, query, A1)
    return SIXTH

def activity_option(query, activity):
    lst = top3_options(activity)
    O1 = lst[0][0]
    O1_link = lst[0][1]
    O2 = lst[1][0]
    O2_link = lst[1][1]
    O3 = lst[2][0]
    O3_link = lst[2][1]
    query.message.reply_text(f"Option 1: \nTitle: {O1} \nWebsite: {O1_link}")
    query.message.reply_text(f"Option 2: \nTitle: {O2} \nWebsite: {O2_link}")
    query.message.reply_text(f"Option 3: \nTitle: {O3} \nWebsite: {O3_link}")
    ACTIVITIES.append(activity)
    confirmation(query, activity)
    return SIXTH

def activity_result(context, query, activity):
    A1_img = image_api(activity)
    details = choosen(activity)
    A1_desc = details[0]
    A1_map = details[1]
    A1_link = details[2]
    context.bot.sendPhoto(chat_id=query.message.chat_id, photo=A1_img, caption=f"Image of {activity}")
    query.message.reply_text(f"Look here for more information! \n\nDescription: {A1_desc} \nLocation: {A1_map} \nWebsite: {A1_link}")
    ACTIVITIES.append(activity)
    confirmation(query, activity)
    return SIXTH

def confirmation(query, activity):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(SELECTED)),
         InlineKeyboardButton("No", callback_data=str(DECLINE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"Do you want to confirm {activity} as your activity?", reply_markup=reply_markup)        
    return SIXTH

def confirmation_activity(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(SELECTED)),
         InlineKeyboardButton("No", callback_data=str(DECLINE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"Do you want to confirm {SELECT_PAST_ACTIVITY[-1]} as your activity?", reply_markup=reply_markup)        
    return SIXTH


########################################
############ SIXTH BUTTON ##############
########################################

def selected(update, context):
    query = update.callback_query
    if SELECT_PAST_ACTIVITY != []:
        ACTIVITIES.append(SELECT_PAST_ACTIVITY[-1])
        del SELECT_PAST_ACTIVITY[-1]
    query.message.reply_text(f"Success! \U0001F604 \nYour selected activity is {ACTIVITIES[-1]}")
    if GROUP == []:
        session = ACTIVITIES[-1] + " on " + CONFIRM_DATE[0]
        d = CONFIRM_DATE[0].split(" ")[0].split("-")
        review_dt = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), hour=int(review_hour), minute=int(review_min)) - timedelta(hours=8)
        context.job_queue.run_once(review, review_dt, context=query.message.chat_id)
        CONFIRM_MEETING.append(session)
        if INPUT_GOOGLE_CALENDAR != []:
            creds = get_creds()
            cal = get_calendar(creds)
            create_event(cal, ACTIVITIES[-1], "Organised by Let's Go GaiGai", CONFIRM_DATE[-1].split(" ")[0]+"T00:00:00+08:00", CONFIRM_DATE[-1].split(" ")[0]+"T23:59:00+08:00")
        keyboard = [
            [InlineKeyboardButton("YES!!", callback_data=str(INPUT_REMINDER_DATE)),
            InlineKeyboardButton("Nope, thank you!", callback_data=str(NO_REMINDER))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Do you want a reminder for your meeting?", reply_markup=reply_markup)
        CONFIRM_DATE.clear()
        CONFIRM_TIME.clear()
        ACTIVITIES.clear()
        DATES.clear()
        return REMIND
    else:
        name = str(query.message.chat.first_name)
        id = str(query.message.chat.id)
        if name not in DONE:
            DONE.append(name)
        if id not in ID_LIST:
            ID_LIST.append(id)
        keyboard = [
            [InlineKeyboardButton("I want to add more activities for this date", callback_data=str(SELECT_ACTIVITY))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Select one", reply_markup=reply_markup)
        CONFIRM_TIME.clear()
        return SECOND


########################################
############# USER INPUT ###############
########################################

def user_input_google_calendar(update, context):
    input = update.message.text
    string = input.split("\n")
    if len(string) == 1:
        update.message.reply_text("There should be a start date and end date. Please re-enter the period by using 'shift-enter' to type the end date too")
        return USER_INPUT_GOOGLE_CALENDAR
    elif len(string) > 2:
        update.message.reply_text("There should be on a start date and end date. Please enter again")
        return USER_INPUT_GOOGLE_CALENDAR
    else:
        for date_time in string:
            date_string = date_time.split(" ")[0]
            date_format = '%Y-%m-%d'
            try:
                dateObject = datetime.datetime.strptime(date_string, date_format)
                INPUT_GOOGLE_CALENDAR.append(date_time)
            except ValueError:
                update.message.reply_text("Incorrect data format, should be YYYY-MM-DD. \nKindly type your free date again")
                return USER_INPUT_GOOGLE_CALENDAR
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(LINK_GOOGLE_CALENDAR)),
            InlineKeyboardButton("No", callback_data=str(INPUT_PERIOD))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"We will be extracting your google calendar from {INPUT_GOOGLE_CALENDAR[0]} to {INPUT_GOOGLE_CALENDAR[-1]} \n\nDo you want to confirm?", reply_markup=reply_markup)
        return SECOND

def message_activity(update, context):
    input = update.message.text
    update.message.reply_text(f"Your activity is {input}")
    details = choosen(input)
    A1_desc = details[0]
    A1_map = details[1]
    A1_link = details[2]
    update.message.reply_text(f"Description: {A1_desc} \nLocation: {A1_map} \nWebsite: {A1_link}")
    ACTIVITIES.append(input)
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(SELECTED)),
         InlineKeyboardButton("No", callback_data=str(ACTIVITY))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Do you want to confirm {input} as your activity?", reply_markup=reply_markup)        
    return SIXTH

def message_schedules(update, context):
    input = update.message.text
    string = input.split("\n")
    for date_time in string:
        date_string = date_time.split(" ")[0]
        date_format = '%Y-%m-%d'
        try:
            dateObject = datetime.datetime.strptime(date_string, date_format)
            TYPED_SCHEDULE.append(date_time)
        except ValueError:
            update.message.reply_text("Incorrect data format, should be YYYY-MM-DD. \nKindly type your free date again")
            return USER_INPUT_SCHEDULES
        if dateObject.date() < date.today():
            update.message.reply_text("Meeting date will need to be today or after today. \nKindly type your date again.")
            return USER_INPUT_SCHEDULES
    if SELECT_PAST_ACTIVITY == []:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(SELECT_ACTIVITY)),
            InlineKeyboardButton("No", callback_data=str(SCHEDULES))],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(CONFIRMATION)),
            InlineKeyboardButton("No", callback_data=str(SCHEDULES))],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Your free date(s) is/are: \n{input} \n\nDo you want to confirm?", reply_markup=reply_markup)
    return SECOND

def select_activity(update, context):
    query = update.callback_query
    if TYPED_SCHEDULE != []:
        for date in TYPED_SCHEDULE:
            CONFIRM_DATE.append(date)
    keyboard = [
        [InlineKeyboardButton("Yes, I have an activity in mind!", callback_data=str(ACTIVITY))],
        [InlineKeyboardButton("No.. Can you help me?", callback_data=str(CATEGORY))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Do you have an activity in mind?", reply_markup=reply_markup)
    return THIRD


########################################
########### CALENDAR BUTTON ############
########################################

def calendar(update, context):
    query = update.callback_query
    today = date.today()
    result, key, step = DetailedTelegramCalendar(min_date=today).process(query.data)
    if not result and key:
        query.message.reply_text(f"Select {LSTEP[step]}", reply_markup=key)
    elif result:
        query.message.reply_text(f"You selected {result}", reply_markup=None)
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(KEEP_DATE)),
             InlineKeyboardButton("No", callback_data=str(CHANGE_DATE))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Please confirm this meeting date.", reply_markup=reply_markup)
        DATES.append(str(result))
        return SECOND
    
########################################
############## TIME BUTTON #############
########################################

def time(update, context):
    query = update.callback_query
    option = query.data
    keyboard = []
    if option in CONFIRM_TIME:
        CONFIRM_TIME.remove(option)
    else:
        CONFIRM_TIME.append(option)
    for label in checkbox_time:
        if label in CONFIRM_TIME:
            check = [InlineKeyboardButton(label + ' ' + '\u2705', callback_data=label)]
            keyboard.append(check)
        else:
            check = [InlineKeyboardButton(label, callback_data=label)]
            keyboard.append(check)
    confirm = [InlineKeyboardButton(f"Submit \U0001F44D", callback_data=str(KEEP_TIME))]
    keyboard.append(confirm)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f"What time will be your meet-up session? \u23F0 \nYou may select more than one \n\nClick Confirm once done!", reply_markup=reply_markup)
    return TIME

def keep_time(update, context):
    query = update.callback_query
    if SELECT_PAST_ACTIVITY != []:
        if len(CONFIRM_TIME) == 1:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]})"
            CONFIRM_DATE.append(update_date)
        elif len(CONFIRM_TIME) == 2:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]} and {CONFIRM_TIME[1]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]} and {CONFIRM_TIME[1]})"
            CONFIRM_DATE.append(update_date)
        else:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]} to {CONFIRM_TIME[-1]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]} to {CONFIRM_TIME[-1]})"
            CONFIRM_DATE.append(update_date)
        confirmation(query, SELECT_PAST_ACTIVITY[-1])
        return SIXTH
    else:
        if len(CONFIRM_TIME) == 1:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]})"
            CONFIRM_DATE.append(update_date)
        elif len(CONFIRM_TIME) == 2:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]} and {CONFIRM_TIME[1]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]} and {CONFIRM_TIME[1]})"
            CONFIRM_DATE.append(update_date)
        else:
            query.message.reply_text(f"Selected Time: {CONFIRM_TIME[0]} to {CONFIRM_TIME[-1]}")
            update_date = f"{DATES[-1]} ({CONFIRM_TIME[0]} to {CONFIRM_TIME[-1]})"
            CONFIRM_DATE.append(update_date)
        keyboard = [
            [InlineKeyboardButton("Yes, I have an activity in mind!", callback_data=str(ACTIVITY))],
            [InlineKeyboardButton("No.. Can you help me?", callback_data=str(CATEGORY))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Do you have an activity in mind?", reply_markup=reply_markup)
        return THIRD

    
########################################
########### INFORMATION ################
########################################

def information(update, context):
    query = update.callback_query
    choice = query.data
    if "(" not in choice:
        d = choice.split(" on ")[1]
        a = choice.split(" on ")[0]
        t = ""
    else: 
        d = choice.split(" on ")[1].split("(")[0]
        a = choice.split(" on ")[0]
        t = choice.split("(")[1].split(")")[0]
    details = choosen(a)
    A1_desc = details[0]
    A1_map = details[1]
    A1_link = details[2]  
    query.message.reply_text(f"Details: \nDate: {d} \nTime: {t} \nActivity: {a} \n\nDescription: {A1_desc} \nLocation: {A1_map} \nWebsite: {A1_link}")
    if query.message.chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("Go back to menu", callback_data=str(MENU))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Go back to menu", callback_data=str(GROUP_MENU))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Select the following.", reply_markup=reply_markup)
    return MAIN


########################################
######### GROUP MESSAGE ################
########################################

def consolidate_poll(update, context):
    query = update.callback_query
    if len(DONE) == TOTAL_VOTER_COUNT[-1]:
        remove_duplicates = []
        if len(CONFIRM_DATE) == 1:
            remove_duplicates.append(CONFIRM_DATE[-1])
        else:
            new_confirm_date = []
            for d in CONFIRM_DATE:
                new_confirm_date.append(d.split(" ")[0])
            c = Counter(new_confirm_date)
            for tuple in c.items():
                if tuple[1] > 1:
                    remove_duplicates.append(tuple[0])
        if len(remove_duplicates) > 1:
            questions = remove_duplicates
            message = context.bot.send_poll(
                update.effective_chat.id,
                f"These are your common free dates. Please select you preferred date(s).",
                questions,
                is_anonymous=False,
                allows_multiple_answers=True,
            )
            payload = {
                message.poll.id: {
                    "questions": questions,
                    "message_id": message.message_id,
                    "chat_id": update.effective_chat.id,
                    "answers": 0,
                }
            }
            context.bot_data.update(payload)
        elif len(remove_duplicates) == 1:
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(GROUP_ACTIVITY)),
                 InlineKeyboardButton("No", callback_data=str(GROUP_DATE))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(update.effective_chat.id, f"You have one common free date on {remove_duplicates[-1]}. \nWould you like to proceed? \n\nNOTE: Only {CONTROL_MAN[-1]} can interact with the bot.", reply_markup=reply_markup)
            GROUP_CONFIRM_DATE.append(remove_duplicates[-1])
            return CONSOLIDATE
        else:
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(MONTHLY_REMINDER)),
                 InlineKeyboardButton("No", callback_data=str(GROUP_MENU))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(update.effective_chat.id, f"There are no common free date among the participants in the group. \nWould you like to organize the meet up next month instead? \n\nNOTE: Only {CONTROL_MAN[-1]} can interact with the bot.", reply_markup=reply_markup)
            return CONSOLIDATE

    elif DONE == []:
        keyboard = [
            [InlineKeyboardButton("Refresh", callback_data=str(CONSOLIDATE_POLL))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(update.effective_chat.id, f"There is no inputs. \nPlease refresh when you have done inputting in the private chat. \n\nhttp://telegram.me/gaigai_bot?start=start", reply_markup=reply_markup)
        return CONSOLIDATE
    else:
        complete = ""
        for name in DONE:
            if complete == "":
                complete += name
            else:
                complete = complete + ", " + name
        keyboard = [
            [InlineKeyboardButton("Refresh", callback_data=str(CONSOLIDATE_POLL))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(update.effective_chat.id, f"Only {complete} has/have put in their inputs. \nPlease refresh again when other group member(s) has completed. \n\nhttp://telegram.me/gaigai_bot?start=start", reply_markup=reply_markup)
        return CONSOLIDATE
    
def group_activity(update, context):
    context.bot.send_message(update.effective_chat.id, f"Your meeting date is: {GROUP_CONFIRM_DATE[-1]}.")
    remove_activity_duplicates = []
    [remove_activity_duplicates.append(y) for y in ACTIVITIES if y not in remove_activity_duplicates]
    if len(remove_activity_duplicates) > 1:
        questions = remove_activity_duplicates
        message = context.bot.send_poll(
                update.effective_chat.id,
                "These are the activities suggested. Please select you preferred activities for the meeting!",
                questions,
                is_anonymous=False,
                allows_multiple_answers=True,
            )
        payload = {
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
        context.bot_data.update(payload)
    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(GROUP_SESSION)),
            InlineKeyboardButton("No", callback_data=str(GROUP_CATEGORY))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        GROUP_CONFIRM_ACTIVITY.append(remove_activity_duplicates[-1])
        context.bot.send_message(update.effective_chat.id, f"You have one activity for the meeting: {remove_activity_duplicates[-1]}. \nWould you like to proceed? \n\nNOTE: Only {CONTROL_MAN[-1]} can interact with the bot.", reply_markup=reply_markup)
        return CONSOLIDATE

def group_session(update, context):
    session = GROUP_CONFIRM_ACTIVITY[-1] + " on " + GROUP_CONFIRM_DATE[-1]
    d = GROUP_CONFIRM_DATE[-1].split(" ")[0].split("-")
    review_dt = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), hour=int(review_hour), minute=int(review_min)) - timedelta(hours=8)
    for id in ID_LIST:
        context.job_queue.run_once(review, review_dt, context=id)
    context.bot.send_message(update.effective_chat.id, f"Success! \U0001F604 \n\n{GROUP[0]} has a meeting doing {session}")
    if INPUT_GOOGLE_CALENDAR != []:
        creds = get_creds()
        cal = get_calendar(creds)
        create_event(cal, GROUP_CONFIRM_ACTIVITY[-1], "Organised by Let's Go GaiGai", GROUP_CONFIRM_DATE[0].split(" ")[0]+"T00:00:00+08:00", GROUP_CONFIRM_DATE[0].split(" ")[0]+"T23:59:00+08:00")
    CONFIRM_MEETING.append(session)
    keyboard = [
        [InlineKeyboardButton("YES!!", callback_data=str(INPUT_REMINDER_DATE)),
         InlineKeyboardButton("Nope, thank you!", callback_data=str(NO_REMINDER))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(update.effective_chat.id, "Do you want a reminder for your meetings?", reply_markup=reply_markup)
    CONFIRM_DATE.clear()
    CONFIRM_TIME.clear()
    ACTIVITIES.clear()
    DATES.clear()
    GROUP_CONFIRM_DATE.clear()
    GROUP_CONFIRM_ACTIVITY.clear()
    TOTAL_VOTER_COUNT.clear()
    DONE.clear()
    return REMIND

def group_date(update, context):
    query = update.callback_query
    context.bot.send_message(update.effective_chat.id, f"Type in your schedule(s) in this format. \n\nYYYY-MM-DD (TIME) \nYYYY-MM-DD (TIME) \n\nRemember to reply to this message so I can capture your input! \U0001F916")
    return GROUP_INPUT_DATE

def group_category(update, context):
    query = update.callback_query
    context.bot.send_message(update.effective_chat.id, f"Please type in the activity name \n\nRemember to reply to this message so I can capture your input! \U0001F916")
    return GROUP_INPUT_ACTIVITY

def group_menu(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Upcoming activities", callback_data=str(UPCOMING))],
        [InlineKeyboardButton("Past activities", callback_data=str(PAST))],
        [InlineKeyboardButton("Exit", callback_data=str(END))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(update.effective_chat.id,
        f"Welcome to GaiGai Bot Menu! \U0001F916 \nClick the options below to continue. \n\nYou may also click /start at your personal chat to create another session",
        reply_markup=reply_markup
    )
    return FIRST

def monthly_reminder(update, context): ## reminder to organize a meetup every 1st day of the month 
    query = update.callback_query
    t = datetime.time(hour=14, minute=0) # 14,0 is 9am reminder on 1st day of the month 
    context.job_queue.run_monthly(monthly, t, 1, context=GROUP_ID[-1])
    keyboard = [
        [InlineKeyboardButton("Go back to menu", callback_data=str(GROUP_MENU))],
        [InlineKeyboardButton("End this session", callback_data=str(END))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(update.effective_chat.id, f"We have added a reminder for you to organize meet up next month! \U0001F916", reply_markup=reply_markup)
    return CONSOLIDATE
     

########################################
########## GROUP INPUTS ################
########################################

def group_input_activity(update, context):
    input = update.message.text
    GROUP_CONFIRM_ACTIVITY.append(input)
    group_session(update, context)
    return CONSOLIDATE

def group_input_date(update, context):
    input = update.message.text
    GROUP_CONFIRM_DATE.append(input)
    group_activity(update, context)
    return CONSOLIDATE

        
########################################
########## POLL ANSWERS ################
########################################

def receive_poll_answer(update, context):
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids #list of chosen options
    for option in selected_options:
        POLL_LIST.append(option)
    answered_poll["answers"] += 1
    # Close poll after all participants voted
    if answered_poll["answers"] == TOTAL_VOTER_COUNT[-1]:
        context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
        mostFrequent = max(set(POLL_LIST), key=POLL_LIST.count)
        answer_string = questions[mostFrequent]
        context.bot.send_message(answered_poll["chat_id"], f"Majority choose {answer_string}.")
        try: 
            result = bool(parse(answer_string.split(" ")[0], fuzzy=False))
            if result:
                GROUP_CONFIRM_DATE.append(answer_string)
                keyboard = [
                    [InlineKeyboardButton("Yes", callback_data=str(GROUP_ACTIVITY)),
                    InlineKeyboardButton("No", callback_data=str(GROUP_DATE))],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(answered_poll["chat_id"], f"Would you like to proceed? \n\nNOTE: Only {CONTROL_MAN[-1]} can interact with the bot.", reply_markup=reply_markup)
                POLL_LIST.clear()
                return CONSOLIDATE
        except ValueError:
            GROUP_CONFIRM_ACTIVITY.append(answer_string)
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data=str(GROUP_SESSION)),
                InlineKeyboardButton("No", callback_data=str(GROUP_CATEGORY))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(answered_poll["chat_id"], f"Would you like to proceed? \n\nNOTE: Only {CONTROL_MAN[-1]} can interact with the bot.", reply_markup=reply_markup)
            POLL_LIST.clear()
            return CONSOLIDATE
        

########################################
############ REMINDER ##################
########################################

def no_reminder(update, context):
    query = update.callback_query
    if GROUP == []:
        keyboard = [
            [InlineKeyboardButton("Go back to menu", callback_data=str(MENU))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if REMINDER_DATE == []:
            query.message.reply_text("Select the following.", reply_markup=reply_markup)
        else:
            query.message.reply_text("A reminder has been set! \nSelect the following.", reply_markup=reply_markup)
        return MAIN
    else:
        keyboard = [
            [InlineKeyboardButton("Go back to menu", callback_data=str(GROUP_MENU))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if REMINDER_DATE == []:
            context.bot.send_message(update.effective_chat.id, "Select the following.", reply_markup=reply_markup)
        else:
            context.bot.send_message(update.effective_chat.id, "A reminder has been set! \n\nSelect the following.", reply_markup=reply_markup)
        return CONSOLIDATE

def input_reminder_date(update, context):
    query = update.callback_query
    if GROUP == []:
        query.message.reply_text(f"Type in your reminder datetime in this format. \nYYYY-MM-DD HH:MM")
    else:
        context.bot.send_message(update.effective_chat.id, f"Type in your reminder datetime in this format. \nYYYY-MM-DD HH:MM \n\nRemember to reply to this message so I can capture your input! \U0001F916")
    return USER_INPUT_REMINDER

def user_input_reminder(update, context):
    string = update.message.text
    date_format = '%Y-%m-%d %H:%M'
    try:
        dateObject = datetime.datetime.strptime(string, date_format)
        REMINDER_DATE.append(string)
    except ValueError:
        update.message.reply_text("Incorrect data format, should be YYYY-MM-DD HH:MM. \nKindly type your reminder date again")
        return USER_INPUT_REMINDER
    if dateObject < datetime.datetime.now():
        update.message.reply_text("Reminder datetime will need to be a later time. \nKindly type your datetime again.")
        return USER_INPUT_REMINDER
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(NO_REMINDER)),
         InlineKeyboardButton("No", callback_data=str(INPUT_REMINDER_DATE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    d = REMINDER_DATE[-1].split(" ")[0].split("-")
    t = REMINDER_DATE[-1].split(" ")[1].split(":")
    reminder_dt = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), hour=int(t[0]), minute=int(t[1])) - timedelta(hours=8)
    context.job_queue.run_once(reminder_msg, reminder_dt, context=update.message.chat_id)
    context.bot.send_message(update.effective_chat.id, f"You will be reminded on {string} \n\nDo you want to confirm?", reply_markup=reply_markup)
    return REMIND

def reminder_msg(context): 
    str = ""
    for upcoming in CONFIRM_MEETING:
        if str == "":
            str = upcoming
        else:
            str = str + " \n" + upcoming
    context.bot.send_message(context.job.context, text=f"Reminder \U0001F514 \n\nThe following is your upcoming activity: \n\n{str}") 

def monthly(context: CallbackContext):
    context.bot.send_message(context.job.context, text="Hi :)! Why not organize a meetup with your friends now? Send /start@gaigai_bot to me and Let's Go GaiGai !!")

########################################
############ REVIEWS ###################
########################################

def review(context: CallbackContext):
    context.bot.send_message(context.job.context, text=f"Review Time! \U0000270F \n\nHow is your meeting session for {CONFIRM_MEETING[0]} with your friends? \n\nShare your experience with us")
    return USER_INPUT_REVIEWS

def user_input_review(update, context):
    input = update.message.text
    PAST_ACTIVITY.append(CONFIRM_MEETING[0].split(" on ")[0])
    for p in PAST_ACTIVITY:
        for c in CONFIRM_MEETING:
            if p in c:
                CONFIRM_MEETING.remove(c)
    REVIEW_LST.append([PAST_ACTIVITY[-1]]) 
    REVIEW_LST[-1].append(input)
    keyboard = []
    for star in RATING_LIST:
        keyboard.append([InlineKeyboardButton(star, callback_data=star)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(update.effective_chat.id, f"Please rate the meeting session!", reply_markup=reply_markup)
    return REVIEWS

def rating(update, context):
    query = update.callback_query
    choice = query.data
    REVIEW_LST[-1].append(choice) 
    result = []
    for l in REVIEW_LST:
        for i in l:
            if PAST_ACTIVITY[-1] in i:
                result.append(l[1:])
    USER_REVIEW[PAST_ACTIVITY[-1]] = result
    context.bot.send_message(update.effective_chat.id, "Thank you for sharing!")
    end(update, context)
    return ConversationHandler.END

########################################
########### PAST REVIEW ################
########################################

def past_review(update, context):
    query = update.callback_query
    choice = query.data
    lst = USER_REVIEW.get(choice)
    context.bot.send_message(update.effective_chat.id, f"Activity: {choice}")
    rating = []
    review = []
    for i in lst:
        ra = i[1]
        re = i[0]
        if ra not in rating:
            rating.append(ra)
        if re not in review:
            review.append(re)
    for j in range(len(rating)):
        context.bot.send_message(update.effective_chat.id, f"Rating: {rating[j]} \nReview: {review[j]}")
    if query.message.chat.type == "group":
        keyboard = [
            [InlineKeyboardButton("Go back to menu", callback_data=str(GROUP_MENU))],
            [InlineKeyboardButton("End this session", callback_data=str(END))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(update.effective_chat.id, f"Select one", reply_markup=reply_markup)
        return CONSOLIDATE
    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data=str(PLAN)),
             InlineKeyboardButton("No", callback_data=str(MENU))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        SELECT_PAST_ACTIVITY.append(choice)
        context.bot.send_message(update.effective_chat.id, f"Do you wish to choose {choice} as your new meeting session's activity?", reply_markup=reply_markup)
        return FIRST


########################################
############### END ####################
########################################

def end(update, context):
    query = update.callback_query
    if GROUP != [] and DONE != []:
        query.message.reply_text(f"Thank you for your inputs! \U0001F929 \nYou may now click 'View Results' in the group chat (if haven't) or click 'Refresh' to view the poll!")
        query.message.reply_text(f"See you next time! \U0001FAE1")
    elif query.message.chat.type == "private":
        query.message.reply_text(f"See you next time! \U0001FAE1 \n\nClick /start to start Let's Go GaiGai privately or in your group chat!")
    else:
        query.message.reply_text(f"See you next time! \U0001FAE1")
    START.clear()
    return ConversationHandler.END


########################################
######### ERROR MESSAGE ################
########################################

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
