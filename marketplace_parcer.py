import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
class Scraper:

    """Scraping marketplaces"""

    def __init__(self):
        self.soup = []
        self.url = {'yandex': 'https://market.yandex.ru/catalog--elektronika/54440',
                    'ozon': 'https://www.ozon.ru/category/elektronika-15500/',
                    'wb': 'https://www.wildberries.ru/catalog/elektronika'}

        # for item in self.url:
        #
        #     self.markup = requests.get(self.url[item]).text
        #     self.soup.append(BeautifulSoup(self.markup, 'html.parser'))
        #     with open(f'{item}.html', 'w') as file:
        #         file.write(str(self.soup))

    def yandex(self):

        url = self.url['yandex']
        self.markup = requests.get(url='https://market.yandex.ru/catalog--smartfony/26828310/list?hid=91491&onstock=0&local-offers-first=0', headers=headers).text
        self.soup = BeautifulSoup(self.markup, 'html.parser')
        print(self.soup)
        items = self.soup.findAll('article', {'data-zone-name': 'snippet-card'})
        for item in items:
            print(str(item) + '\n')


if __name__ == '__main__':
    Scraper().yandex()
