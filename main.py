import requests
from pprint import pprint
from weather import open_weather_token
from datetime import datetime
from sqlalchemy import create_engine,MetaData,Table,Integer,String,Column,Text,DateTime,Boolean,ForeignKey,select

def get_weather(city,open_weather_token):
    global humidity
    global data
    code_to_smile = {
        'Clear':'Ясно \U00002600',
        'Clouds':'Облачно \U00002601',
        'Rain':'Дождь \U00002614',
        'Drizzle':'Дождь \U00002614',
        'Thunderstorm':'Гроза \U000026A1',
        'Mist':'Туман \U0001F328',
        'Snow':'Снег \U0001F328'
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        weather_discription = data['weather'][0]['main']
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "Не знаю это какая погода. Посмотри в окно бро)"

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        wind = data['wind']['speed']
        pressure = data['main']['pressure']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        print(f"***{current_date}***")
        print(f"Погода в городе ---{city}---\nТемпература: {cur_weather}°C {wd}\nМакс.температура: {temp_max}°C\nМин.температура: {temp_min}°C\n"
              f"Влажность: {humidity}%\nВетер: {wind}м/c\nДавление: {pressure}мм.рт.ст\n"
              f"Время рассвета: {sunrise_timestamp}\nВремя заката: {sunset_timestamp}")

    except Exception as ex:
        print(ex)
        print('Проверьте название города!!!')

metadata = MetaData()

city_table = Table('cities', metadata,
    Column('id', Integer(), primary_key=True),
    Column('city', String(200), nullable=False),
)

city_weather_table = Table('weather', metadata,
    Column('id', Integer(), primary_key=True),
    Column('weather', String(200), nullable=False),
    Column('humidity', String(200),  nullable=False),
    Column('temp_max', String(200),  nullable=False),
    Column('temp_min', String(200),  nullable=False),
    Column('wind', String(200),  nullable=False),
    Column('pressure', String(200),  nullable=False),
    Column('city_table_id', ForeignKey("cities.id")),
)
# engine = create_engine("mysql+pymysql://root:123456789@localhost/mydb")
# metadata.create_all(engine )
# conn = engine.connect()
# metadata.create_all(engine)
# ins = city_table.insert().values(city_table="Ashgabat")
# conn.execute(ins)
# s = select([city_table])
# r = conn.execute(s)
# print(r.fetchall())
def main():
    city = input('Введитe название города: ')
    print('')
    get_weather(city,open_weather_token)

if __name__=='__main__':
    main()