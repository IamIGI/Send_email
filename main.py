import requests
import smtplib
import os
import datetime


MY_EMAIL = "YOUR_EMAIL"
PASSWORD = "PASSWORD_TO_YOUR_EMAIL"
CHOOSE_EMAIL = "TARGET+EMAIL "
URL = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = "1260fa0855cfe91f77ebe79f5e75f7ef"
weather_params = {
    "lat": 49.994940,
    "lon": 20.757135,
    "exclude": "minutely,current,daily",                            #hourly,daily
    "appid": API_KEY,
}
hour_list = [1, 4, 9, 13]                                           #0 - hour 7 a.m . Program  will check the weather by 7 a.m

response = requests.get(url=URL, params=weather_params)
response.raise_for_status()
data_weather = response.json()

#get the datetime
d = datetime.datetime.now()
datetime_now = f"{d.strftime('20%y')}-{d.strftime('%m')}-{d.strftime('%d')} "

os.remove("weather.txt")
for i in hour_list:
    with open("weather.txt", mode="a") as file:
        file.write( f"Pogoda o godzinie {6+i}: "
                    f"{data_weather['hourly'][i]['weather'][0]['main']} Opis: {data_weather['hourly'][i]['weather'][0]['description']}\n "
                    f"Temperatura: {round(data_weather['hourly'][i]['temp'] - 273.15, 1)}\n\n")
with open("weather.txt", mode="r") as file:
    weather = file.read()

connect = smtplib.SMTP('smtp.gmail.com', port=587)            #64.233.184.108
connect.starttls()
connect.login(user=MY_EMAIL, password=PASSWORD)
connect.sendmail(from_addr=MY_EMAIL, to_addrs=CHOOSE_EMAIL, msg=f"Subject: Pogoda dnia: {datetime_now}\n\n "
                                                                f"Pogodna dnia: {datetime_now}\n {weather}")
connect.close()