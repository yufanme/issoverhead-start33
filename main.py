import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude
MY_EMAIL = "562937707@qq.com"
MY_PASSWORD = "bpyjiqjylklcbdhe"


def is_iss_overland():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    # If the ISS is close to my current position,
    lat = iss_latitude - MY_LAT
    long = iss_longitude - MY_LONG
    if -5 < lat < 5 and -5 < long < 5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour
    # and it is currently dark
    if sunset < hour or hour < sunrise:
        return True
    else:
        return False


# BONUS: run the code every 60 seconds.
while True:
    if is_iss_overland() and is_night():
        # Then email me to tell me to look up.
        with smtplib.SMTP("smtp.qq.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject:See!\n\nlook up!")
            print("email sent.")
    else:
        print("nothing happen.")
    time.sleep(60)

