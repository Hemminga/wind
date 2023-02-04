import requests
import sys
import re
from bs4 import BeautifulSoup
# from pprint import pprint

DEBUG = True


def main():
    response = requests.get('https://www.knmi.nl/nederland-nu/weer/waarnemingen')
    if DEBUG:
        print(response.status_code)
    if response.status_code != 200:
        print(f'Status Code: {response.status_code}')
        sys.exit(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.table
    eelde = table.find_all('td', string="Eelde")[0].parent
    print(eelde.prettify())
    uitgifte = soup.find_all(string=re.compile('Uitgifte'))
    print(uitgifte[0])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
