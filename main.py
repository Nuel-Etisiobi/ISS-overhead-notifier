import time
import requests
from datetime import datetime
import json
from email.message import EmailMessage
import ssl
import smtplib

MY_LAT = 4.858190
MY_LONG = 4.858190
MY_POSITION = (MY_LAT, MY_LONG)


def iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_data = iss_response.json()

    longitude = float(iss_data['iss_position']['longitude'])
    latitude = float(iss_data['iss_position']['latitude'])
    # timestamp = iss_data['timestamp']
    # iss_time = datetime.fromtimestamp(timestamp)
    iss_position = (latitude, longitude)

    # check if the iss is over head
    if MY_LAT - 5 <= iss_position[0] <= MY_LAT + 5 and MY_LONG - 5 <= iss_position[1] <= MY_LONG + 5:
        return True


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params="lat=4.858190&lng=4.858190&formatted=0")
    # raise errors
    response.raise_for_status()

    current_hour = datetime.now().hour

    data = response.json()
    sunrise = data['results']['sunrise'].split("T")[1].split(":")[0]
    sunset = data['results']['sunset'].split("T")[1].split(":")[0]

    if current_hour == sunset:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        with open("../MyPass Generator/data.json", mode="r") as file:
            details = json.load(file)
            sender_email = details["Python"]["email"]
            sender_password = details['Python']['password']

        receiver_email = "youngharmony44@gmail.com"
        subject = "ISS Overhead"
        body = "Hey, Go outside and look up to see the the ISS Satellite over you"

        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as message:
            message.login(sender_email, sender_password)
            message.sendmail(sender_email, receiver_email, em.as_string())
