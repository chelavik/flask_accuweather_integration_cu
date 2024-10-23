import requests

from errors import BadRequest, APIKeyError
from initialize import BASEURL, API_KEY, SEARCH_BY_GEOLOCATION, FORECAST_BY_GEOLOCATION


def result_to_geokey(response) -> str:
    data = response.json()
    geokey = data['Key']

    return geokey

def geokey_request(lon: str, lat: str) -> str:  # Запрос к API для получения геокода для дальнейших запросов
    location = f'{lon},{lat}'
    query = {'apikey': API_KEY, 'q' :location}

    get_location_key_request = requests.get(url=BASEURL+SEARCH_BY_GEOLOCATION,
                                    params=query)

    if get_location_key_request.status_code == 400 or get_location_key_request.json() is None:
        raise BadRequest

    if get_location_key_request.status_code == 401:
        raise APIKeyError


    geokey = result_to_geokey(get_location_key_request)
    return geokey


def result_to_conditions(response) -> dict:  # Парсит необходимые данные прогноза от API
    data = response.json()

    min_temperature = data['DailyForecasts'][0]['Temperature']['Minimum']['Value']
    max_temperature = data['DailyForecasts'][0]['Temperature']['Maximum']['Value']
    humidity = data['DailyForecasts'][0]['Day']['RelativeHumidity']['Average'] #  Влажность в процентах
    wind_speed = data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'] # Скорость ветра в км/ч
    precipitation_probability = data['DailyForecasts'][0]['Day']['PrecipitationProbability'] #  вероятность осадков в %

    conditions = {'Minimal Temperature': min_temperature,
                  'Maximal Temperature': max_temperature,
                  "Humidity": humidity,
                  'Wind Speed': wind_speed,
                  'Precipitation Probability': precipitation_probability
                  }
    return conditions


def weather_by_key_request(geokey: str) -> dict:
    query = {'apikey': API_KEY,
             'language': 'ru-ru',
             'details': True,
             'metric': True}
    get_weather_by_key = requests.get(url=BASEURL+FORECAST_BY_GEOLOCATION+geokey,
                                      params=query)

    if get_weather_by_key.status_code == 400:
        raise BadRequest
    if get_weather_by_key.status_code == 401:
        raise APIKeyError

    conditions = result_to_conditions(get_weather_by_key)

    return conditions


def get_weather_conditions(lon: str, lat: str) -> dict:
    try:
        geokey = geokey_request(lon, lat)
        conditions = weather_by_key_request(geokey)
        return conditions

    except BadRequest:
        raise BadRequest("По этим координатам нельзя получить погоду..")
    except APIKeyError:
        raise APIKeyError("Проблема с API-ключом!")



if __name__ == "__main__":
    lon = '55.764108'
    lat = '37.592446'
    print(get_weather_conditions(lon, lat))
