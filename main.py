import openmeteo_requests
import time
from plyer import notification
import requests_cache
from retry_requests import retry
import datetime

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 43.3575,
	"longitude": 132.1914,
	"hourly": ["rain", "snowfall", "showers"],
	"timezone": "Australia/Sydney",
	"forecast_days": 1,
	"timeformat": "unixtime",
}


responses = openmeteo.weather_api(url, params=params)

response = responses[0]

hourly = response.Hourly()

hourly_rain = hourly.Variables(0).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(1).ValuesAsNumpy()
hourly_showers = hourly.Variables(2).ValuesAsNumpy()

r_h = []
s_h = []

i = 0
for r, s, sh in zip(hourly_rain, hourly_snowfall, hourly_showers):
    if r >= 0.2 or sh >= 0.2:
        if time.localtime()[3] <= i + 1:
            r_h.append(i)
    if s >= 0.2:
        if time.localtime()[3] <= i + 1:
            s_h.append(i)
    i+=1

time.sleep(2)
if len(s_h) > 0:
    notification.notify(
        title="Погодный скрипт",
        message=f"❄️❄️❄️ Кажется сегодня будет СНЕГ! 🌨️ \n{s_h}",
        app_name="Python Weather",
        timeout=20
    )
    time.sleep(5)
elif len(r_h) > 0:
    notification.notify(
        title="Погодный скрипт",
        message=f"💧💧💧 Кажется сегодня будет ДОЖДЬ! 🌧️\n{r_h}",
        app_name="Python Weather",
        timeout=20
    )
    time.sleep(5)
else:
    # notification.notify(
    #     title="Погодный скрипт",
    #     message="Скрипт ничего не обнаружил!",
    #     app_name="Python Weather",
    #     timeout=15
    # )
    pass