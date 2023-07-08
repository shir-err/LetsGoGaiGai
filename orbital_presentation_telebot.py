from orbital_business_telebot import *

##pip install python-telegram-bot
##pip install python-telegram-bot-calendar

from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Filters, PollAnswerHandler

print('Starting up bot...')

token = "6079896577:AAFdcxZDbl0M3ehw-WEuURvzNxEt0v_m5Pc"

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            MAIN: [CallbackQueryHandler(menu, pattern='^' + str(MENU) + '$'),
                   CallbackQueryHandler(end, pattern='^' + str(END) + '$')],

            FIRST: [CallbackQueryHandler(plan, pattern='^' + str(PLAN) + '$'),
                    CallbackQueryHandler(upcoming, pattern='^' + str(UPCOMING) + '$'),
                    CallbackQueryHandler(past, pattern='^' + str(PAST) + '$'),
                    CallbackQueryHandler(help, pattern='^' + str(HELP) + '$'),
                    CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                    CallbackQueryHandler(back, pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(end, pattern='^' + str(END) + '$')],

            SECOND: [CallbackQueryHandler(yes, pattern='^' + str(YES) + '$'),
                    CallbackQueryHandler(keep_date, pattern='^' + str(KEEP_DATE) + '$'),
                    CallbackQueryHandler(keep_date_2, pattern='^' + str(KEEP_DATE_2) + '$'),
                    CallbackQueryHandler(change_date, pattern='^' + str(CHANGE_DATE) + '$'),
                    CallbackQueryHandler(no, pattern='^' + str(NO) + '$'),
                    CallbackQueryHandler(input_period, pattern='^' + str(INPUT_PERIOD) + '$'),
                    CallbackQueryHandler(link_google_calendar, pattern='^' + str(LINK_GOOGLE_CALENDAR) + '$'),
                    CallbackQueryHandler(schedules, pattern='^' + str(SCHEDULES) + '$'),
                    CallbackQueryHandler(select_activity, pattern='^' + str(SELECT_ACTIVITY) + '$'),
                    CallbackQueryHandler(end, pattern='^' + str(END) + '$')],

            THIRD: [CallbackQueryHandler(category, pattern='^' + str(CATEGORY) + '$'),
                    CallbackQueryHandler(activity, pattern='^' + str(ACTIVITY) + '$')],

            FOURTH: [CallbackQueryHandler(adventure, pattern='^' + str(ADVENTURE) + '$'),
                    CallbackQueryHandler(attraction, pattern='^' + str(ATTRACTION) + '$'),
                    CallbackQueryHandler(food, pattern='^' + str(FOOD) + '$'),
                    CallbackQueryHandler(activity, pattern='^' + str(OTHER) + '$')],

            FIFTH: [CallbackQueryHandler(activity_option_1, pattern='^' + str(ACTIVITY_OPTION_1) + '$'),
                    CallbackQueryHandler(activity_option_2, pattern='^' + str(ACTIVITY_OPTION_2) + '$'),
                    CallbackQueryHandler(activity_option_3, pattern='^' + str(ACTIVITY_OPTION_3) + '$'),
                    CallbackQueryHandler(activity_result_1, pattern='^' + str(ACTIVITY_RESULT_1) + '$'),
                    CallbackQueryHandler(activity_result_2, pattern='^' + str(ACTIVITY_RESULT_2) + '$'),
                    CallbackQueryHandler(activity_result_3, pattern='^' + str(ACTIVITY_RESULT_3) + '$'),
                    CallbackQueryHandler(more, pattern='^' + str(MORE) + '$')],

            SIXTH: [CallbackQueryHandler(selected, pattern='^' + str(SELECTED) + '$'),
                    CallbackQueryHandler(activity, pattern='^' + str(ACTIVITY) + '$'),
                    CallbackQueryHandler(category, pattern='^' + str(DECLINE) + '$')],

            USER_INPUT_ACTIVITY: [MessageHandler(Filters.text, message_activity)],

            USER_INPUT_SCHEDULES: [MessageHandler(Filters.text, message_schedules)],

            USER_INPUT_GOOGLE_CALENDAR: [MessageHandler(Filters.text, user_input_google_calendar)],

            CALENDAR: [CallbackQueryHandler(calendar)],

            FOOD_LST: [CallbackQueryHandler(food_lst)],

            TIME: [CallbackQueryHandler(keep_time, pattern='^' + str(KEEP_TIME) + '$'),
                   CallbackQueryHandler(time)],

            INFORMATION: [CallbackQueryHandler(menu, pattern='^' + str(MENU) + '$'),
                          CallbackQueryHandler(information)],

            CONSOLIDATE: [CallbackQueryHandler(consolidate_poll, pattern='^' + str(CONSOLIDATE_POLL) + '$'),
                          CallbackQueryHandler(category, pattern='^' + str(CATEGORY) + '$'),
                          CallbackQueryHandler(group_activity, pattern='^' + str(GROUP_ACTIVITY) + '$'),
                          CallbackQueryHandler(group_session, pattern='^' + str(GROUP_SESSION) + '$'),
                          CallbackQueryHandler(group_menu, pattern='^' + str(GROUP_MENU) + '$'),
                          CallbackQueryHandler(group_category, pattern='^' + str(GROUP_CATEGORY) + '$'),
                          CallbackQueryHandler(group_date, pattern='^' + str(GROUP_DATE) + '$'),
                          CallbackQueryHandler(end, pattern='^' + str(END) + '$')],

            GROUP_INPUT_DATE: [MessageHandler(Filters.text, group_input_date)],

            GROUP_INPUT_ACTIVITY: [MessageHandler(Filters.text, group_input_activity)],

            USER_INPUT_REMINDER: [MessageHandler(Filters.text, user_input_reminder)],

            REMIND: [CallbackQueryHandler(input_reminder_date, pattern='^' + str(INPUT_REMINDER_DATE) + '$'),
                     CallbackQueryHandler(no_reminder, pattern='^' + str(NO_REMINDER) + '$'),
                     CallbackQueryHandler(set_reminder, pattern='^' + str(SET_REMINDER) + '$')],

        },
        fallbacks=[CommandHandler('start', start_command)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)
    dp.add_handler(PollAnswerHandler(receive_poll_answer))  

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print('Polling...')
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()