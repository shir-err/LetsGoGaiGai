# Let's Go GaiGai :dancing_women:
NUS Orbital 2023 - Team 5702

Developed By :
Lai Hui Ling (@hhuilingg) , Tan Shir Er (@shir-err)

## Motivation
Initiating, organising and scheduling a meetup with your friends can be troublesome as everyone has a different and complex schedule. This is especially so for bigger groups as the tendency for schedule clashes becomes higher. Furthermore, it can be difficult to find activities to do as a group. 

As a busy student, it can be quite time-consuming to compare everyone's schedules and research on possible activities. Hence, one would either wait for their friends to take the initiative to organise the meetup or not meet them till months later, if ever.

## Aim
To develop a Telegram Bot for people to easily plan their gatherings by recommending various group activities and finding a common free date to hang out for them. The platform would help to automatically update their online schedule with said activity once it has been confirmed to help better plan for future activities.

<img align="center" src="https://github.com/shir-err/LetsGoGaiGai/blob/main/Let's%20Go%20GaiGai%20-%20Poster.jpg">

## Features
### Accessible and Intuitive User Interface
The Telegram Bot can be accessed via Private Chat and also within a Group Chat. Users can choose to message the bot privately or add the bot to a group chat to allow other participants to interact with the bot.

In a private chat, the bot comprises four main user-bot interactions - Plan an Activity, Upcoming Activities, Past Activities, and Help. In “Plan an Activity”, the bot will guide the user in organising an outing by prompting the user for necessary details such as the event's date, time, and venue. If the user lacks any of such details, the bot will prompt the user to use its functions to determine these details (e.g.: consolidation of schedule, suggested activities). In “Upcoming Activities”, the bot will store the activities planned by the users and provide more details when clicked. Once the upcoming session has ended, it will be removed from the upcoming activities and added to the past activities. Last but not least, the “Help” button will provide instructions on the usage of GaiGai Bot.

**Status : Completed [:green_circle:]**

### Interactable with Telegram Group Settings
The Telegram Bot is able to add into a group and all members are able to start the bot. After starting the bot, there will be a link for all members to start a private chat with the bot to input their free dates and the activities they would like to carry out during the meeting. This private message allows all users to be involved and make the meeting session more interesting. After all members' inputs are stored, there will be a poll carried out in the group chat with the majority being the final meeting session date and activity. This will then be added to all members' upcoming activities. Meanwhile, all members are able to chat in the group without any interference from the bot, only if there is a reply message to the bot. 

**Status : Completed [:green_circle:]**

### Consolidate Multiple Schedules
The Telegram Bot is able to accept multiple types of schedules such as Google Calendar and manual input to determine the availability of the participants relative to others.

The user is able to:
1. Upload their Google Calendar to the Telegram Bot
2. Alternatively, the user is able to manually input their availability
3. Display the top few dates with the most number of participants available

**Status : Completed [:green_circle:]**

### Insert New Event into Participants’ Calendar (if any)
Once an event has been agreed upon by the participants, the users who had uploaded a link to their Google or Outlook Calendar can choose to insert a new event into their calendar about the aforementioned event.

The bot is able to:
1. Update the participant’s calendar by inserting a new event on the confirmed day to meet
2. Event is furnished with the agreed-upon date, time and venue

**Status : Completed [:green_circle:]**

### Provides Suggested Activities to Do
The Telegram Bot is able to provide a list of suggested activities that the participants could explore with their friends. The activities would be grouped into various categories such as “Adventure”, “Attractions”, “Food/Dining” and “Others” to help users filter through the myriad of activities available.

The bot is able to:
1. Allow users to choose the category of activities 
2. Display details of the activities (eg. Image, Description, Location, Website)

**Status : Completed [:green_circle:]**

### Send Reminders to Participants on Upcoming Plans
Each participant in the planned activity would receive a private message from the Telegram Bot asking if they wish to be reminded of the activity. If yes, the bot will prompt for when the user wishes to be reminded such as how many days before and at what time. The reminder would be sent in the form of a message by the Telegram Bot to the user. The Telegram Bot will also prompt the group chat on whether they wish for the bot to send a reminder to the chat as well.

The user is able to:
1. Choose whether they wish to be sent a reminder
2. Specify the period they wish to be reminded

The bot is able to:
1. Send automated messages to the group and to individuals to remind them of the planned activity

**Status : Completed [:green_circle:]**

### Collate Reviews from Participants
After the day of the activity, Telegram Bot will initiate a private conversation with the participants and ask them to rate and review the activity, if any. This would be kept in the Telegram Bot’s system for future reference of all its users who wish to view the reviews of past activities.

The bot is able to:
1. Prompt participants after an activity for a rating and text review
2. Store the reviews and retrieve it for future use

**Status : Completed [:green_circle:]**

### Track Past Activities of Each User
The Telegram Bot is able to keep a record of the activities each individual has attended through using the bot. This will allow the user to access past activities and how they had reviewed the activity for future reference, should they wish to take part in a similar activity again with other groups of friends.

The user is able to:
1. Access a list of past activities they had taken part in
2. View their reviews and other reviews (if any) of the selected activity

**Status : Completed [:green_circle:]**

### Set Scheduled Monthly Reminders for Groups to Plan Events
The Telegram Bot is able to send a scheduled message to participants to remind them to plan an activity with the group. This will cater to users who are interested in having monthly meetings, for example, and encourage more consistent meetups despite everyone's busy schedules.

The user is able to:
1. Set a reminder for the bot to prompt them to organize a meetup if there are no common free dates

**Status : Completed [:green_circle:]**
