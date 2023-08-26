
from api_service import get_weather, Coordinates
import pickle






def weather(user) -> str:
    with open('data1.pickle', 'rb') as g:
        dict_of_coordinates = pickle.load(g)
    """Returns a message about the temperature and weather description"""
    print(f"{dict_of_coordinates} in weather")
    try:
        wthr = get_weather(Coordinates(latitude=dict_of_coordinates[user][0], longitude=dict_of_coordinates[user][1]))
        return f'{wthr.location}, {wthr.description}\n' \
               f'Temperature is {wthr.temperature}°C, feels like {wthr.temperature_feeling}°C'
    except KeyError:
        return f"пожалуйста прикрепите геолокацию"


def wind(user) -> str:
    with open('data1.pickle', 'rb') as g:
        dict_of_coordinates = pickle.load(g)
    """Returns a message about wind direction and speed"""
    try:
        wthr = get_weather(Coordinates(latitude=dict_of_coordinates[user][0], longitude=dict_of_coordinates[user][1]))
        return f'{wthr.wind_direction} wind {wthr.wind_speed} m/s'
    except KeyError:
        return f"пожалуйста прикрепите геолокацию"


def sun_time(user) -> str:
    with open('data1.pickle', 'rb') as g:
        dict_of_coordinates = pickle.load(g)
    """Returns a message about the time of sunrise and sunset"""
    try:
        wthr = get_weather(Coordinates(latitude=dict_of_coordinates[user][0], longitude=dict_of_coordinates[user][1]))
        return f'Sunrise: {wthr.sunrise.strftime("%H:%M")}\n' \
               f'Sunset: {wthr.sunset.strftime("%H:%M")}\n'
    except KeyError:
        return f"пожалуйста, прикрепите геолокацию"


photoes = list()
def clothe(arr, user) -> str:
    with open('data1.pickle', 'rb') as g:
        dict_of_coordinates = pickle.load(g)
    global photoes
    try:
        wthr = get_weather(Coordinates(latitude=dict_of_coordinates[user][0], longitude=dict_of_coordinates[user][1]))
        rec = "вам стоит надеть "
        for i in arr:
            if (i[1]<=int(wthr.temperature)<=i[2]) and (i[3]<=int(wthr.wind_speed)<=i[4]):
                rec+=i[0]
                rec+=" "
                photoes.append(i[5])
        #print(rec)
        if (len(photoes)>0):
            return rec
        else:
            return f'у вас нет подходящей одежды, но вы можете добавить ее с помощью кнопки add thing'
    except KeyError:
        return f"пожалуйста прикрепите геолокацию"

def st(arr) -> list:
    array = list()
    for i in arr:
        s = ""
        s+=i[0]
        s+="\n"
        s+="temperature "
        s+=str(i[1])
        s+=" "
        s+=str(i[2])
        s+="\n"
        s+="wind speed "
        s+=str(i[3])
        s+=" "
        s+=str(i[4])
        array.append(s)
    return array

