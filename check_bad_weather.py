
def check_weather(conditions: dict) -> str:
    """Погода считается неблагоприятной, если :
    1. Температура воздуха ниже -10 или выше +40 градусов по Цельсию
    2. Влажность ниже 15% или выше 85%
    3. Вероятность осадков выше 80%
    4. Скорость ветра выше 50 км/ч
    """

    weather_verdict = 'погода хорошая :)'

    if any([conditions['Minimal Temperature'] < -10, conditions['Maximal Temperature'] > 40,
            85 < conditions['Humidity'] < 15, conditions['Precipitation Probability'] > 80,
            conditions['Wind Speed'] > 50]):
        weather_verdict = 'погода плохая :('

    return weather_verdict


if __name__ == '__main__':
    conditions = {'Minimal Temperature': 6.3,
                  'Maximal Temperature': 12.2,
                  'Humidity': 70,
                  'Wind Speed': 18.5,
                  'Precipitation Probability': 4}
    print(check_weather(conditions))