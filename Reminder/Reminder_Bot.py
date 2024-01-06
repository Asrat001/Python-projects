from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
import time
from datetime import datetime

user_data = {}
TOKEN = '6749837961:AAG1ybD-NI8GVLjGC_dRskS8mLkm35l4m9M'




updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Send /settime to schedule a reminder time.")

def set_time(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {'status': 'waiting_time'}
        context.bot.send_message(chat_id=chat_id, text="Please send the reminder time in HH:MM format.")
    else:
        context.bot.send_message(chat_id=chat_id, text="You've already set the reminder time. Send the reminder message.")

def process_message(update, context):
    chat_id = update.effective_chat.id
    if chat_id in user_data and user_data[chat_id]['status'] == 'waiting_time':
        user_data[chat_id]['time'] = update.message.text
        user_data[chat_id]['status'] = 'waiting_message'
        context.bot.send_message(chat_id=chat_id, text="Reminder time set. Send the reminder message.")
    elif chat_id in user_data and user_data[chat_id]['status'] == 'waiting_message':
        reminder_message = update.message.text
        reminder_time = user_data[chat_id]['time']


        print(reminder_time)
        # Format the reminder time for scheduling
        formatted_time = datetime.strptime(reminder_time, "%H:%M").time()
        formatted_12hr_time=formatted_time.strftime("%I:%M %p")
       # time_24hr_format = formatted_12hr_time.strftime("%H:%M")
        print(formatted_time)

        # Schedule the reminder
        schedule.every().day.at(str(formatted_time)).do(send_reminder, context.bot, chat_id, reminder_message)
        
        # Debugging: Print a message to verify the scheduling
        print(f"Scheduled reminder for {reminder_time}")

        context.bot.send_message(chat_id=chat_id, text=f"Reminder scheduled for {reminder_time}.")
        user_data.pop(chat_id)  # Clear user data after scheduling
    else:
        context.bot.send_message(chat_id=chat_id, text="Please set the reminder time first using /settime.")

def send_reminder(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

start_handler = CommandHandler('start', start)
set_time_handler = CommandHandler('settime', set_time)
message_handler = MessageHandler(Filters.text & ~Filters.command, process_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(set_time_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
