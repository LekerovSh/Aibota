import json
import requests
import apikey
from datetime import datetime
from datetime import timedelta
import settings

appid = apikey.openweatherapi
city_id = 0

gifs = {
                    '01d': '🌞',
                    '02d': '⛅',
                    '03d': '☁',
                    '04d': '☁',
                    '09d': '☔',
                    '10d': '⛅ ☔',
                    '11d': '⚡',
                    '13d': '❄',
                    '50d': '☁',
                    '01n': '🌛',
                    '02n': '☁',
                    '03n': '☁',
                    '04n': '☁',
                    '09n': '☔',
                    '10n': '⛅ ☔',
                    '11n': '⚡',
                    '13n': '❄',
                    '50n': '☁'
                }
            

def weatherapp(text, day, user_date):
    im = ""
    icon=""
    place_query = text
    place_apikey = apikey.google_place_api
    weather = "error"
    lat = "lat"
    lon = "lot"
    now = user_date
    namekz = ""
    try:
        place_res = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json',
                                 params={'query': place_query, 'language': 'ru', 'key': place_apikey})
        print(place_res)
        place_data = place_res.json()
        print(place_data)
        lon = json.dumps(place_data['results'][0]['geometry']['location']['lng'])
        lat = json.dumps(place_data['results'][0]['geometry']['location']['lat'])
        namekz = place_data['results'][0]['name']

        #print(place_data)

    except Exception as e:
        print("Error requests: ", e)
        return [weather, weather]
    pass
    
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'lat': lat, 'lon': lon, 'units': 'metric',
                                   'lang': 'ru', 'appid': appid})
        data = res.json()
        #print(data)
        
        if (day == "сегодня"):
            t = 0
        elif (day == "завтра"):
            t = 1
        elif (day == "послезавтра"):
            t = 2
        list = data['list']
        #print("t=",t)
        for daily in list:
            name = str(data['city']['name'])
            conditions = str(daily['weather'][0]['description'])
            clouds = str(daily['clouds']['all'])
            wind_speed = str(daily['wind']['speed'])
            temp = daily['main']['temp']
            humi = str(daily['main']['humidity'])
            date = str(daily['dt_txt'])
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            settings.context["city"] = namekz
            temp_suffix=""
            if (temp > 0):
                temp_suffix = " выше нуля"
            elif (temp < 0):
                temp_suffix = " ниже нуля"
            weather = ""
            prefix = ""
            if (date=="завтра" or date=="послезавтра"):
                prefix = " будет "

            if (temp > 0):
                temp = "+" + str(temp)
            # hours 00, 03, 06, 09, 12, 15, 18, 21 
            hour_diff_min = 2
            
            if t>0 and date.hour==12 and date.day==(now + timedelta(days=t)).day:
                icon = str(daily['weather'][0]['icon'])
                #print(icon)
                for key, val in gifs.items():
                    if (key == icon):
                        im = val
                        print(val)
                        break
                weather_voice = day.capitalize() + " в городе " + namekz + prefix + str(conditions).capitalize()+ "."+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"
                weather = day.capitalize() + " в городе  <b>" + namekz + "</b>" + prefix + "<em> " + str(conditions).capitalize()+ ' ' +im + "</em>" +". \n"+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"  + " \nВлажность: " + humi + " %\nОблачность: " + clouds + " %\nСкорость ветра: " + wind_speed + " м/с\n\n" 
                return [weather_voice, weather]
                
            elif t==0 and (abs(date.hour - now.hour) < hour_diff_min or abs(date.hour - now.hour)==23)  and date.day==now.day:
                icon = str(daily['weather'][0]['icon'])
                #print(icon)
                for key, val in gifs.items():
                    if (key == icon):
                        im = val
                        #print(val)
                        break
                weather_voice = day.capitalize() + " в городе " + namekz + prefix + str(conditions).capitalize()+". \n"+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"
                weather = day.capitalize() + " в городе  <b>" + namekz + "</b>" + prefix + "<em> " + str(conditions).capitalize()+ ' ' +im + "</em>" +". \n"+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"  + " \nВлажность: " + humi + " %\nОблачность: " + clouds + " %\nСкорость ветра: " + wind_speed + " м/с\n\n"
                return [weather_voice, weather]
                                


        '''

        temp_suffix=""
        if (temp > 0):
            temp_suffix = " выше нуля"
        elif (temp < 0):
            temp_suffix = " ниже нуля"
        weather = ""
        prefix = ""
        if (date=="завтра" or date=="послезавтра"):
            prefix = " будет "
        
            
        weather = day.capitalize() + " в городе  <b>" + namekz + "</b>" + prefix + "<em> " + str(conditions).capitalize()+ ' ' +im + "</em>" +". \n"+"температура воздуха ".capitalize() + "на " + date + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"  + " \nВлажность: " + humi + " %\nОблачность: " + clouds + " %\nСкорость ветра: " + wind_speed + " м/с\n\n"
        '''
        weather_voice = day.capitalize() + " в городе " + namekz + prefix + str(conditions).capitalize()+ ". \n"+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"
        weather = day.capitalize() + " в городе  <b>" + namekz + "</b>" + prefix + "<em> " + str(conditions).capitalize()+ ' ' +im + "</em>" +". \n"+"температура воздуха ".capitalize() + "на " + day + " " + str(
            temp) + " ºC градусов " + temp_suffix +".\n"  + " \nВлажность: " + humi + " %\nОблачность: " + clouds + " %\nСкорость ветра: " + wind_speed + " м/с\n\n"         
        return [weather_voice, weather]
    except Exception as e:
        print(e)
        return [weather, weather]
        pass
        return [weather, weather]
    return [weather, weather]
