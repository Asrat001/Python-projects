
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xmltodict
import json

def main():
      sender_email="asratadane169@gmail.com"
      sender_password="vhhg qrxv cjbz vtyt"
      receiver_email="asratadane169@gmail.com"
      subject="IE Networks JObs"
      jobs=get_Jobs()
      message=formating_Message(jobs)
      send_email(sender_email, sender_password, receiver_email, subject, message)
      print("message sent")

def get_Jobs():
    url = "https://www.ienetworksolutions.com/?feed=job_feed"
    response = requests.get(url)
    data_dict = xmltodict.parse(response._content)
    json_data = json.dumps(data_dict)
    data = json.loads(json_data)
    filterd_data= data['rss']['channel']['item']
    job_list =[]
    for job in filterd_data:
          job_list.append(    {
              "title":job['title'],
              "job_location":job['job_listing:location'],
              "job-link":job['link']
          })

    return  job_list
def formating_Message(jobs):
     message =""
     for i in jobs:
          message+=f"{i['title'],i['job_location'],i['job-link']}"
     return   message    
def send_email(sender_email, sender_password, receiver_email, subject, message):
    smtp_server = "smtp.gmail.com"  # Change this if using a different email provider
    smtp_port = 587  # Change this if using a different email provider

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(message, 'plain'))

    # Start the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    
if __name__ == "__main__":
   main()
     
