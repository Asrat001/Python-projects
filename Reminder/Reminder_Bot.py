from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
from telegram import ParseMode
import threading
import re
import time
from datetime import datetime,timedelta
import vonage


user_data = {}
TOKEN = '6749837961:AAG1ybD-NI8GVLjGC_dRskS8mLkm35l4m9M'
api_key = '931607dd'
api_secret = '9qTpbBQCJf1tfDbc'
virtual_number = 'Vonage APIs'
client = vonage.Client(key=api_key, secret=api_secret)
Sms=vonage.Sms(client)



updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Send /settime to schedule a reminder time.")

def set_time(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {'status': 'waiting_time'}
        context.bot.send_message(chat_id=chat_id, text=" Please send the reminder time in HH:MM AM/PM example  (1:20 pm) ")
    else:
        context.bot.send_message(chat_id=chat_id, text="set the reminder time.")

def process_message(update, context):
    am_pm_pattern = re.compile(r'\b(?:am|pm)\b', re.IGNORECASE)
    chat_id = update.effective_chat.id
    if chat_id in user_data and user_data[chat_id]['status'] == 'waiting_time':
        user_data[chat_id]['time'] = update.message.text
        user_data[chat_id]['status'] = 'waiting_phone'
        match = re.search(am_pm_pattern, user_data[chat_id]['time'])
        if match:
             context.bot.send_message(chat_id=chat_id, text="Reminder time set. Send the reminder phone number ")
             
        else:
             context.bot.send_message(chat_id=chat_id, text="Your time format is not correct")
    
        
       
    elif chat_id in user_data and user_data[chat_id]['status'] == 'waiting_phone':
        user_data[chat_id]['phone'] = update.message.text
        user_data[chat_id]['status'] = 'waiting_message'
        context.bot.send_message(chat_id=chat_id, text=" you sususfully set Time and Phone Number now set your Reminder")
        
    elif chat_id in user_data and  user_data[chat_id]['status']== 'waiting_message':
        reminder_message = update.message.text
        reminder_time = user_data[chat_id]['time'] 
        reminder_Phone =user_data[chat_id]['phone']

        schedule_reminder(context.bot, chat_id, reminder_Phone,reminder_message, reminder_time )
        context.bot.send_message(chat_id=chat_id, text=f"Reminder scheduled for {reminder_time}.")
        user_data[chat_id].pop('time')  # Clear time for the next reminder
        user_data[chat_id]['status'] = 'waiting_time' 
       
     
          # Clear user data after scheduling
    else:
        context.bot.send_message(chat_id=chat_id, text="Please set the reminder time first using /settime.")

def schedule_reminder(bot, chat_id,reminder_Phone, reminder_message, reminder_time,):
   
    
    pm_pattern = re.compile(r'\b(?:pm)\b', re.IGNORECASE)
    am_pattern = re.compile(r'\b(?:am)\b', re.IGNORECASE)
    matchPM = re.search(pm_pattern, reminder_time)
    matchAM = re.search(am_pattern, reminder_time)
    formatted_time = datetime.strptime(reminder_time,  "%I:%M %p").time()
    #twelve_hours=timedelta(hours=12)
    #time_after_12_hours = (datetime.combine(datetime.min, formatted_time) + twelve_hours).time()
     
    # cleaned_timeAM = reminder_time[:matchAM.start()] + reminder_time[matchAM.end():]
  
    print(reminder_Phone)
    schedule.every().day.at(str(formatted_time)).do(send_reminder, bot, chat_id, reminder_message,reminder_Phone)

def send_reminder(bot, chat_id, message,phone):
    text = f" your <b>Remander is</b> .\n {message} \n \n <i>follow me on Linkedin at </i>, at <a href='https://www.linkedin.com/in/asrat-adane-50a521240/'>Asrat Adane</a>."
    bot.send_message(chat_id=chat_id, text=text,parse_mode=ParseMode.HTML)
    print(phone)
    responseData= Sms.send_message({
    'from': virtual_number,
    'to':"251"+phone,
    'text':message+" \n"+"From Assrat-ReminderBot"
                      })
    if responseData["messages"][0]["status"] == "0":
      print("Message sent successfully.")
    else:
      print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

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
