import datetime, pytz, time, requests, json
from datetime import date
import locale 

def find_time(place_query):
    namekz = ''
    ans = ""
    print("Place = "+place_query)
    
    if (place_query==''):
        ans = "Введите местоположение"
        ans_voice = "Введите местоположение"
        return ans_voice, ans
    GOOGLE_API_KEY = "AIzaSyAmlSnOEVeOhuCpet_lCtxCSXAb3C36VIo"
    try:
        place_res = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json',
                                 params={'query': place_query, 'language': 'ru', 'key': GOOGLE_API_KEY})
        place_data = place_res.json()
        lat = json.dumps(place_data['results'][0]['geometry']['location']['lng'])
        lon = json.dumps(place_data['results'][0]['geometry']['location']['lat'])
        namekz = place_data['results'][0]['name']
        print(place_data)
    except Exception as e:
        print("Error requests: ", e)
        ans = "Такого местоположения не найдено. Пожалуйста, повторите запрос"
        ans_voice = "Такого местоположения не найдено. Пожалуйста, повторите запрос"
        return ans_voice, ans
    pass
    lons = str(lon)
    lats = str(lat)
    print("Запрос:"+namekz+"\nДолгота:" + lons + "\nШирота: " + lats)
    
    URL = "https://maps.googleapis.com/maps/api/timezone/json"
    res = requests.get(URL,
                       params={"location": lons + "," + lats, "timestamp": str(round(time.time())),
                               "key": GOOGLE_API_KEY})
    data = res.json()
    print(data)
    tzid = data['timeZoneId']
    print("Найдено часовой пояс: " + tzid )
    timezone = pytz.timezone(tzid)
    url = "https://api.teleport.org/api/locations/" + str(lon) + "," + str(
        lat) + "/?embed=location:nearest-cities/location:nearest-city/city:timezone/tz:offsets-now%20|%20jq%20%27._embedded.%22location:nearest-cities%22[0]._embedded.%22location:nearest-city%22._embedded.%22city:timezone%22%27"
    res = requests.get(url)
    data = res.json()
    href = data['_embedded']['location:nearest-cities'][0]['_embedded']['location:nearest-city']['_embedded'][
        'city:timezone']['_embedded']['tz:offsets-now']['_links']['self']['href']
    date_and_time = href[-20:]
    date = date_and_time[:-10]
    times = date_and_time[-9:]
    times = times[:-1]
    then = date + " " + times
    date_obj = datetime.datetime.strptime(then, "%Y-%m-%d %H:%M:%S")
    time_find = date_obj + timezone.utcoffset(date_obj)
    utime = time_find.time()
    udate = time_find.date()
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    ans = "Сейчас в местоположении " + namekz + " " + str(utime) + ", " + udate.strftime('%A %d %B %Y')
    ans_voice = "Сейчас в местоположении " + namekz + " " + str(utime.hour) + " часов, " + str(utime.minute) + " минут, " + udate.strftime('%A %d %B %Y')
    return ans_voice, ans


#print(find_time("нью йорк"))
#print(find_time("новая зеландия"))
