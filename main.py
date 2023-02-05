import locale
import os
import psycopg
import requests
import re
import sys
import zoneinfo
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint

DEBUG = True
load_dotenv()


def main():
    response = requests.get('https://www.knmi.nl/nederland-nu/weer/waarnemingen')
    if DEBUG:
        print(response.status_code)
    if response.status_code != 200:
        print(f'Status Code: {response.status_code}')
        sys.exit(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.table
    location = os.getenv('LOCATION')
    local_weather = table.find_all('td', string=location)[0].parent
    print(local_weather.prettify())
    data = []
    for td in local_weather.find_all('td'):
        data.append(td.text)
    uitgifte = soup.find_all(string=re.compile('Uitgifte'))
    print(uitgifte[0])
    datetime_format = 'Uitgifte: %d %B %Y %H:%M uur'
    locale.setlocale(locale.LC_ALL, os.getenv('LOCALE'))
    datetime_object = datetime.strptime(uitgifte[0],
                                        datetime_format).replace(
                                            tzinfo=zoneinfo.ZoneInfo('Europe/Amsterdam'))
    print(datetime_object)
    data.append(datetime_object)
    if DEBUG:
        pprint(data)
    # Connect to an existing database
    with psycopg.connect(
            f"dbname={os.getenv('DATABASE_NAME')} "
            f"user={os.getenv('DATABASE_USER')} "
            f"host={os.getenv('DATABASE_HOST')} "
            f"port={os.getenv('DATABASE_PORT')} "
            f"password={os.getenv('DATABASE_PASSWORD')}") as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO wind(
                station, weather, temperature, chill,
                humidity, wind, windspeed, windgusts,
                visibility, pressure, observation)
                VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT(station, observation) DO NOTHING;""",
                        (data[0], data[1], data[2], data[3], data[4], data[5],
                         data[6], data[7], data[8], data[9],
                         data[10]))
            cur.execute("""SELECT * FROM wind
                ORDER BY observation DESC;""")
            cur.fetchone()
            for record in cur:
                print(record)
            conn.commit()


if __name__ == '__main__':
    main()
