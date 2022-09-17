from bs4 import BeautifulSoup
import requests
from requests import get
import time
import random


def clean(string: str):
    """
    Cleans useless chars in string
    """
    counter = 0
    for c in string:
        if c != ' ':
            break
        else:
            counter += 1
    return counter


url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
houses = []
count = 1

# Page iterator
while count <= 1:
    # Script that puts page number in link
    url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-' + str(count) + '/c37l1700273'
    print(url)
    response = get(url)
    # Enter text from browser to html-parser
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Random-requests-delay-generator
    house_data = html_soup.find_all('div', class_='clearfix')
    if house_data:
        houses.extend(house_data)
        value = random.random()
        scaled_value = 1 + (value * (9 - 5))
        print(f"Sleeping time: {scaled_value}")
        time.sleep(scaled_value)
    else:
        print('EMPTY')
        break
    count += 1

print()
n = int(len(houses)) - 1

count_houses = 0
while count_houses <= 1:
    info = houses[int(count)]

    # IMAGE
    # image = info.find('div', string='kijiji')

    # PRICE
    price = info.find('div', {'class': 'price'}).text
    price = price.replace(' ', '')
    price = price.replace('\n', '')

    # TITLE
    title = info.find('a', {'class': 'title'}).text
    title = title.replace('\n', '')
    title = title[clean(title):][::-1][clean(title[clean(title):][::-1]):][::-1]

    # BEDS
    beds = info.find('span', {'class': 'bedrooms'}).text
    beds = beds.replace('\n', '')
    beds = beds.replace(' ', '')

    # DESCRIPTION
    description = info.find('div', {'class': 'description'}).text
    description = description.replace('\n', '')
    description = description[clean(description):][::-1][clean(description[clean(description):][::-1]):][::-1]

    # LOCATION
    location = info.find('span', {"class": ''}).text
    location = location.replace('\n', '')
    location = location[clean(location):][::-1][clean(location[clean(location):][::-1]):][::-1]

    # POSTDATE
    post_date = info.find('span', {'class': 'date-posted'}).text
    post_date = post_date.replace('/', '-')

    print(f'{image=}\n{title=}\n{post_date=}\n{location=}\n{beds=}\n{description=}\n{price=}\n')
    count_houses += 1
