import re

from flask import Flask, render_template, request, redirect, url_for, flash

from API_requests import get_weather_conditions
from errors import BadRequest, APIKeyError
from check_bad_weather import check_weather

def is_valid_float(value):
    regex = r'^-?\d+(\.\d{1,4})?$'
    return re.match(regex, value) is not None

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')  # Главная страница сформой ввода
def index():
    return render_template('form.html')


# Обработка формы
@app.route('/process', methods=['POST'])
def process():
    # Получаем данные с формы
    start_lon = request.form['start_lon']
    start_lat = request.form['start_lat']
    end_lon = request.form['end_lon']
    end_lat = request.form['end_lat']

    # Валидация полученных данных с формы
    if not (is_valid_float(start_lon) and is_valid_float(start_lat) and is_valid_float(end_lon) and is_valid_float(
            end_lat)):
        error = 'Все значения должны быть числами с 4 цифрами после точки.'
        return render_template('form.html', error=error)

    try:
        start_point_conditions = get_weather_conditions(start_lon, start_lat)
        end_point_conditions = get_weather_conditions(end_lon, end_lat)

        start_weather_verdict = check_weather(start_point_conditions)
        end_weather_verdict = check_weather(end_point_conditions)
        return render_template('result.html',
                                weather_info=f'В стартовой точке {start_weather_verdict}\n'
                                             f'В конечной точке {end_weather_verdict}')

    except BadRequest as e:
        error = f"Ошибка запроса: {str(e)}"
        return render_template('form.html', error=error)


    except APIKeyError as e:
        error = f"Ошибка API: {str(e)}"
        return render_template('form.html', error=error)


    except Exception as e: # Ловим любые другие исключения
        error = f"Произошла неизвестная ошибка: {str(e)}"
        return render_template('form.html', error=error)




if __name__ == '__main__':
    app.run(debug=True)
