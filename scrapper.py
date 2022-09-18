from bs4 import BeautifulSoup
from requests import get
import time
import random
from db_config import host, user, password, db_name
import mysql.connector


class Flat:
    def __init__(self, image, title, date_posted, location, beds, description, price):
        self.image = image
        self.title = title
        self.date_posted = date_posted
        self.location = location
        self.beds = beds
        self.description = description
        self.price = price

    def __str__(self):
        return self.title


try:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=db_name
    )
    print('MySQL: Successfully connected!')
    print('#' * 20)
    mycursor = mydb.cursor()
except Exception as ex:
    print('MySQL: Connection refused...')
    print(ex)


def create_flats(images: list, titles: list, dates_posted: list, locations: list, beds: list, descriptions: list,
                 prices: list):
    """
    Creates a list of flats
    """
    flats_list = []
    for i in range(len(titles)):
        flat = Flat(images[i], titles[i], dates_posted[i], locations[i], beds[i], descriptions[i], prices[i])
        flats_list.append(flat)
    return flats_list


def insert_into_db(flats_list: list):
    """
    Inserts into DB
    """
    for flat in flats_list:
        sqlFormula = f'INSERT INTO houses_db.houses_table(image, title, date, location, beds, description, price) VALUES ("' \
                     f'{flat.image}", "{flat.title}", "{flat.date_posted}", "{flat.location}", "{flat.beds}",' \
                     f' "{flat.description}", "{flat.price}")'
        mycursor.execute(sqlFormula)
        mydb.commit()


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
while count <= 95:  # type any integer you want to parse curtain amount of pages
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
        scaled_value = 1 + (value * 3)
        print(f"Sleeping time: {scaled_value}")
        time.sleep(scaled_value)
    else:
        print('EMPTY')
        break
    count += 1

n = int(len(houses)) - 1

count_houses = 0
while count_houses <= 3776:  # type any integer you want to parse curtain amount of ads
    info = houses[int(count_houses)]

    # IMAGE
    images_list = []
    for c in info.find_all('div', class_='image'):
        for i in c.find_all('img'):
            try:
                print(i['data-src'])
                images_list.append(i['data-src'])
            except KeyError:
                print('Image not found.')
                images_list.append('null')

    # PRICE
    prices_list = []
    for price in info.find_all('div', class_='price'):
        print(price.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", ''))
        prices_list.append(price.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", ''))

    # TITLE
    titles_list = []
    for title in info.find_all('a', class_='title'):
        title = title.get_text().replace('\n', '').replace('"', '').replace("'", '')
        title = title[clean(title):][::-1][clean(title[clean(title):][::-1]):][::-1]
        print(title)
        titles_list.append(title)

    # BEDS
    beds_list = []
    for beds in info.find_all('span', class_='bedrooms'):
        print(beds.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", '')[5:])
        beds_list.append(beds.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", '')[5:])

    # DESCRIPTION
    descriptions_list = []
    for description in info.find_all('div', class_='description'):
        description = description.get_text().replace('\n', '').replace('"', '').replace("'", '')
        description = description[clean(description):][::-1][clean(description[clean(description):][::-1]):][::-1]
        print(description)
        descriptions_list.append(description)

    # LOCATION
    locations_list = []
    for location in info.find_all('span', class_=''):
        location = location.get_text().replace('\n', '').replace('"', '').replace("'", '')
        location = location[clean(location):][::-1][clean(location[clean(location):][::-1]):][::-1]
        print(location)
        locations_list.append(location)

    # POSTDATE
    dates_posted_list = []
    for date_posted in info.find_all('span', class_='date-posted'):
        date_posted = date_posted.get_text().replace('\n', '').replace('/', '-').replace('"', '').replace("'", '')
        date_posted = date_posted[clean(date_posted):][::-1][clean(date_posted[clean(date_posted):][::-1]):][::-1]
        print(date_posted)
        dates_posted_list.append(date_posted)

    flats_list = create_flats(images_list, titles_list, dates_posted_list, locations_list, beds_list, descriptions_list,
                              prices_list)
    insert_into_db(flats_list)
    print()
    count_houses += 1
