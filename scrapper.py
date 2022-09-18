from bs4 import BeautifulSoup
from requests import get
import time
import random
from db_config import host, user, password, db_name
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from dataclasses import dataclass

meta = MetaData()
ads_table = Table('Ads_table', meta,
                  Column('id', Integer, autoincrement=True, nullable=False, unique=True, primary_key=True),
                  Column('image', String(256)),
                  Column('title', String(516)),
                  Column('date_posted', String(32)),
                  Column('location', String(32)),
                  Column('beds', String(16)),
                  Column('description', String(1024)),
                  Column('currency', String(4)),
                  Column('price', String(32))
                  )

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}', echo=True)
meta.create_all(engine)
conn = engine.connect()


@dataclass
class Flat:
    """
    Stores ads parameters
    """
    image: str
    title: str
    date_posted: str
    location: str
    beds: str
    description: str
    currency: str
    price: str

    def __str__(self):
        return self.title


def create_flats(images: list, titles: list, dates_posted: list, locations: list, beds: list, descriptions: list,
                 prices: list):
    """
    Creates a list of flats
    """
    flats_list = []
    currency_list = ['$', '€', '£', '¥', '₣', '₹', 'د.ك', 'د.إ', '﷼',
                     '₻', '₽', '₾', '₺', '₼', '₸', '₴', '₷', '원', '₫',
                     '₮', '₯', '₱', '₳', '₵', '₲', '₪', '₰']
    for i in range(len(titles)):
        if prices[i][0] not in currency_list:
            price = prices[i]
            currency = 'None'
        else:
            price = prices[i][1:]
            currency = prices[i][0]
        flat = Flat(images[i], titles[i], dates_posted[i], locations[i], beds[i], descriptions[i],
                    currency, price)
        print(prices[i])
        flats_list.append(flat)
    return flats_list


def insert_into_db(flats_list: list):
    """
    Inserts into DB
    """
    for flat in flats_list:
        flat_query = ads_table.insert().values(image=flat.image, title=flat.title, date_posted=flat.date_posted,
                                               location=flat.location, beds=flat.beds, description=flat.description,
                                               currency=flat.currency, price=flat.price)
        conn.execute(flat_query)


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
# Ads iterator
while count_houses <= 3770:  # type any integer you want to parse curtain amount of ads
    info = houses[int(count_houses)]

    # IMAGE
    images_list = []
    for c in info.find_all('div', class_='image'):
        for i in c.find_all('img'):
            images_list.append(str(i.get('data-src')))

    # PRICE & CURRENCY
    prices_list = []
    for price in info.find_all('div', class_='price'):
        print(price.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", ''))
        prices_list.append(price.get_text().replace('\n', '').replace(' ', '').replace('"', '').replace("'", ''))

    # TITLE
    titles_list = []
    for title in info.find_all('a', class_='title'):
        title = title.get_text().replace('\n', '').replace('"', '').replace("'", '').strip()
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
        description = description.get_text().replace('\n', '').replace('"', '').replace("'", '').strip()
        print(description)
        descriptions_list.append(description)

    # LOCATION
    locations_list = []
    for location in info.find_all('span', class_=''):
        location = location.get_text().replace('\n', '').replace('"', '').replace("'", '').strip()
        print(location)
        locations_list.append(location)

    # POSTDATE
    dates_posted_list = []
    for date_posted in info.find_all('span', class_='date-posted'):
        date_posted = date_posted.get_text().replace('\n', '').replace('/', '-').replace('"', '').replace("'",
                                                                                                          '').strip()
        print(date_posted)
        dates_posted_list.append(date_posted)

    flats_list = create_flats(images_list, titles_list, dates_posted_list, locations_list, beds_list, descriptions_list,
                              prices_list)
    insert_into_db(flats_list)
    print()
    count_houses += 1
