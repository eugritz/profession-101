from typing import Optional, Self, overload
from bs4 import BeautifulSoup
import requests


MAX_SEARCH_RESULTS_COUNT = 20


class SearchOptions:
    def __init__(self, city: str, page: int = 1):
        self.city = city
        self.page = page


class SearchItem:
    name: str
    manufacturer: str
    price: str
    id: str
    preview_image_source: str
    href: str

    def __init__(self, name: str, manufacturer: str, price: str):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price

        self.id = ''
        self.preview_image_source = ''
        self.href = ''


class SearchResults:
    query: str
    options: SearchOptions
    page_count: int
    count: int
    data: list[SearchItem]


    def __init__(self, query: str, options: SearchOptions):
        self.query = query
        self.options = options
        self.page_count = options.page
        self.count = 0
        self.data = []


    def next_page(self) -> Self:
        options = self.options
        options.page += 1
        return search(self.query, self.options)


    def prev_page(self) -> Self:
        options = self.options
        options.page -= 1
        return search(self.query, self.options)


    def __len__(self) -> int:
        return len(self.data)


    def __list__(self) -> list[SearchItem]:
        return self.data


    def __iter__(self):
        return SearchResultsIterator(self)


    @overload
    def __getitem__(self, key: int) -> SearchItem: ...
    @overload
    def __getitem__(self, key: slice) -> list[SearchItem]: ...
    def __getitem__(self, key: int | slice) -> SearchItem | list[SearchItem]:
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.data)))
            return [self.data[i] for i in indices]
        return self.data[key]


class SearchResultsIterator:
    def __init__(self, results: SearchResults):
        self._index = 0
        self._results = results


    def __iter__(self) -> Self:
        return self


    def __next__(self) -> SearchItem:
        if self._index < len(self._results):
            item = self._results[self._index]
            return item
        raise StopIteration


class SearchItemParser:
    @staticmethod
    def parse(raw) -> SearchItem:
        head, body = raw.div.find_all(recursive=False)
        title, desc = body.div.find_all(recursive=False)

        image_source = head.div.img['src']
        name = title.div.a.text
        manufacturer = title.div.span.text
        price = desc.div.text.strip()

        href = title.div.a['href']
        item = SearchItem(name, manufacturer, price)
        item.id = href[href.rfind('/') + 1:]
        item.preview_image_source = image_source
        item.href = href
        return item


class FacilityOptions:
    def __init__(self, city: str, price_type: int = 0):
        self.city = city
        self.price_type = price_type


class Facility:
    name: str
    address: str
    local_price: str
    in_stock: bool

    def __init__(self, name, address, price):
        self.name = name
        self.address = address
        self.local_price = price
        self.in_stock = False


class FacilityResults:
    id: str
    options: FacilityOptions
    count: int
    data: list[Facility]


    def __init__(self, id: str, options: FacilityOptions):
        self.id = id
        self.options = options
        self.count = 0
        self.data = []


    def __len__(self) -> int:
        return len(self.data)


    def __list__(self) -> list[Facility]:
        return self.data


    def __iter__(self):
        return FacilityResultsIterator(self)


    @overload
    def __getitem__(self, key: int) -> Facility: ...
    @overload
    def __getitem__(self, key: slice) -> list[Facility]: ...
    def __getitem__(self, key: int | slice) -> Facility | list[Facility]:
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.data)))
            return [self.data[i] for i in indices]
        return self.data[key]


class FacilityResultsIterator:
    def __init__(self, results: FacilityResults):
        self._index = 0
        self._results = results


    def __iter__(self) -> Self:
        return self


    def __next__(self) -> Facility:
        if self._index < len(self._results):
            item = self._results[self._index]
            self._index += 1
            return item
        raise StopIteration


class ItemParser:
    @staticmethod
    def parse_facility(raw) -> Facility:
        title, desc = raw.div.find_all(recursive=False)

        name = title.a.text
        address = title.span.text.strip()
        local_price = desc.div.find(class_='item-row-price').text

        status_raw = desc.div.find(class_='m-result-btn').text
        in_stock = status_raw.strip().lower() == 'в наличии'

        facility = Facility(name, address, local_price)
        facility.in_stock = in_stock
        return facility 


def search(query: str, options: SearchOptions) -> SearchResults:
    origin = f'https://{options.city}.vapteke.ru'
    page = requests.get(f'https://{options.city}.vapteke.ru/search?s={query}&page={options.page}')
    if page.status_code != 200:
        return SearchResults(query, options)

    soup = BeautifulSoup(page.text, 'html.parser')
    section = soup.find('section', class_='m-result')
    if section == None:
        return SearchResults(query, options)
    raw_items = section.find_all('div', class_='m-result-item')
    
    items = []
    for raw_item in raw_items:
        parsed = SearchItemParser.parse(raw_item)
        parsed.preview_image_source = origin + parsed.preview_image_source
        items.append(parsed)
    if len(items) == 0:
        return SearchResults(query, options)

    summary = section.find('div', class_='summary')
    item_count = int(summary.find_all()[-1].text)

    pagination = section.find('ul', class_='pagination')
    last_page = int(pagination.find('li', class_='last').a['data-page']) + 1

    results = SearchResults(query, options)
    results.data = items
    results.count = item_count
    results.page_count = last_page
    return results


def get_facilities(id: str, options: FacilityOptions) -> FacilityResults:
    price_type = ''
    if options.price_type > 0:
        price_type = '&PriceType=' + str(options.price_type)
    page = requests.get(f'https://{options.city}.vapteke.ru/search/item/{id}?page=all{price_type}')
    if page.status_code != 200:
        return FacilityResults(id, options)

    soup = BeautifulSoup(page.text, 'html.parser')
    section = soup.find('div', class_='m-result')
    if section == None:
        return FacilityResults(id, options)
    raw_facs = section.find_all('div', class_='m-result-item')

    items = []
    for raw_facility in raw_facs:
        items.append(ItemParser.parse_facility(raw_facility))
    if len(items) == 0:
        return FacilityResults(id, options)

    summary = section.find('div', class_='summary')
    item_count = int(summary.find_all()[-1].text)

    results = FacilityResults(id, options)
    results.data = items
    results.count = item_count
    return results
