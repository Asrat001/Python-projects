from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
from telegram import ParseMode
import threading
import re
import time
from datetime import datetime,timedelta

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
        context.bot.send_message(chat_id=chat_id, text="Please send the reminder time in HH:MM format.you must  use 24h format to set up for PM ")
    else:
        context.bot.send_message(chat_id=chat_id, text="set the reminder time.")

def process_message(update, context):
    pattern = re.compile(r'^\d{1,2}:\d{2}$')
    chat_id = update.effective_chat.id
    if chat_id in user_data and user_data[chat_id]['status'] == 'waiting_time':
        user_data[chat_id]['time'] = update.message.text
        user_data[chat_id]['status'] = 'waiting_message'
        if pattern.match(user_data[chat_id]['time']):
             context.bot.send_message(chat_id=chat_id, text="Reminder time set. Send the reminder message.")
        else:
             context.bot.send_message(chat_id=chat_id, text="Your time format is not correct")
    elif chat_id in user_data and user_data[chat_id]['status'] == 'waiting_message':
        reminder_message = update.message.text
        reminder_time = user_data[chat_id]['time']
       
        if pattern.match(reminder_time):
           schedule_reminder(context.bot, chat_id, reminder_message, reminder_time )
           context.bot.send_message(chat_id=chat_id, text=f"Reminder scheduled for {reminder_time}.")
           user_data[chat_id].pop('time')  # Clear time for the next reminder
           user_data[chat_id]['status'] = 'waiting_time' 
        else:
           context.bot.send_message(chat_id=chat_id, text="your time format is wrong,   Please send the reminder time in HH:MM format.you must  use 24h format to set up for PM ")
           user_data[chat_id].pop('time')  # Clear time for the next reminder
           user_data[chat_id]['status'] = 'waiting_time' 
     
          # Clear user data after scheduling
    else:
        context.bot.send_message(chat_id=chat_id, text="Please set the reminder time first using /settime.")

def schedule_reminder(bot, chat_id, reminder_message, reminder_time,):
    twelve_hours = timedelta(hours=12)
    formatted_time = datetime.strptime(reminder_time, "%H:%M").time()
    time_after_12_hours = (datetime.combine(datetime.min, formatted_time) + twelve_hours).time()
    print(formatted_time)
    # Schedule the reminder
    schedule.every().day.at(str(formatted_time)).do(send_reminder, bot, chat_id, reminder_message)
 
def send_reminder(bot, chat_id, message):
    text = f" your <b>Remander is</b> .\n {message} \n \n <i>follow me on Linkedin at </i>, and <a href='https://www.linkedin.com/in/asrat-adane-50a521240/'>Asrat Adane</a>."
    bot.send_message(chat_id=chat_id, text=text,parse_mode=ParseMode.HTML)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()    
start_handler = CommandHandler('start', start)
set_time_handler = CommandHandler('settime', set_time)
message_handler = MessageHandler(Filters.text & ~Filters.command, process_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(set_time_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()
updater.idle()
