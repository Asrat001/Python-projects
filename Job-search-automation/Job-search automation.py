
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data
def format_weather(data):
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    formatted_weather = f"Temperature: {temperature}°C\nHumidity: {humidity}%\nDescription: {description}"
    return formatted_weather
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
