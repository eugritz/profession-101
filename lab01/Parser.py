import re
import requests
from bs4 import BeautifulSoup
from functools import cached_property

def parse():
    url = 'https://www.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    raw_cards = soup.find_all('article', attrs={'data-name': 'CardComponent'})
    for rc in raw_cards:
        card = CardComponent.raw(rc)
        # TODO: serialization (output everything in .xlsx file)

class CardComponent:
    def __init__(self, data):
        content = data.find_all('div', class_=re.compile(r'--content--'))[0].find_all('div', recursive=False)
        self.general = CardGeneral.raw(content[0])
        self.side = CardSide.raw(content[1])

    @staticmethod
    def raw(data):
        return CardComponent(data)

class CardGeneral:
    def __init__(self, data):
        self.__data = data

    @staticmethod
    def raw(data):
        return CardGeneral(data)

    @cached_property
    def title(self):
        return self.__data.find('span', attrs={'data-mark': 'OfferTitle'}).span.string

    @cached_property
    def subtitle(self):
        return self.__data.find('span', attrs={'data-mark': 'OfferSubtitle'}).string

    @cached_property
    def housing(self):
        return self.__data.find('div', attrs={'data-name': 'SpecialGeo'}).find_previous_sibling('div').a.string

    @cached_property
    def special_geo(self):
        return self.__data.find('div', attrs={'data-name': 'SpecialGeo'}).a.find_all('div')[2].string

    @cached_property
    def labels(self):
        labels = self.__data.find('div', class_=re.compile(r'--labels--')).find_all('a')
        return ', '.join([l.string for l in labels])

    @cached_property
    def price(self):
        return self.__data.find('span', attrs={'data-mark': 'MainPrice'}).span.string

    @cached_property
    def price_per_meter(self):
        return self.__data.find('p', attrs={'data-mark': 'PriceInfo'}).string

class CardSide:
    def __init__(self, data):
        self.__data = data

    @staticmethod
    def raw(data):
        return CardSide(data)

    @cached_property
    def agent(self):
        return self.__branding[2].string

    @cached_property
    def __branding(self):
        return self.__data.find('div', attrs={'data-name': 'BrandingLevelWrapper'}).find_all('span')
