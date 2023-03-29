import re
import requests
import xlsxwriter
from bs4 import BeautifulSoup

def parse():
    url = 'https://www.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/'
    page = requests.get(url)

    workbook = xlsxwriter.Workbook('Квартиры.xlsx')
    cell_format = workbook.add_format({ 'font_name': 'Liberation Sans' })
    worksheet = workbook.add_worksheet('Лист 1')

    soup = BeautifulSoup(page.text, "html.parser")
    raw_cards = soup.find_all('article', attrs={'data-name': 'CardComponent'})

    header_ready = False

    row = 0
    for rc in raw_cards:
        general, side = rc.find_all('div', class_=re.compile(r'--content--'))[0].find_all('div', recursive=False)
        parsed = __parse_general(general)
        parsed.update(__parse_side(side))

        col = 0
        if not header_ready:
            for k in parsed.keys():
                worksheet.write(row, col, k, cell_format)
                col += 1
            header_ready = True
            row += 1
            col = 0

        for v in parsed.values():
            worksheet.write(row, col, v, cell_format)
            col += 1
        row += 1

    workbook.close()

def __parse_general(data):
    parsed = {}
    parsed['Название'] = data.find('span', attrs={'data-mark': 'OfferTitle'}).span.string
    parsed['Квартира'] = data.find('span', attrs={'data-mark': 'OfferSubtitle'}).string

    special_geo = data.find('div', attrs={'data-name': 'SpecialGeo'})
    parsed['Расположение'] = special_geo.a.find_all('div')[2].string

    housing = ''
    geo_info_len = len(special_geo.find_parent('div'))
    if geo_info_len > 2:
        while geo_info_len > 3:
            special_geo = special_geo.find_previous_sibling('div')
            geo_info_len -= 1
        housing = special_geo.find_previous_sibling('div').a.string
    parsed['Жилой комплекс'] = housing

    parsed['Адрес'] = ', '.join([l.string for l in data.find('div', class_=re.compile(r'--labels--')).find_all('a')])
    parsed['Цена'] = data.find('span', attrs={'data-mark': 'MainPrice'}).span.string
    parsed['Цена за м²'] = data.find('p', attrs={'data-mark': 'PriceInfo'}).string
    return parsed

def __parse_side(data):
    branding = data.find('div', attrs={'data-name': 'BrandingLevelWrapper'}).find_all('span')

    parsed = {}
    parsed['Застройщик'] = branding[2].string
    return parsed

