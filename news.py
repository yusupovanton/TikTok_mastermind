from handlers.config import FILE_NAME
from handlers.imports import *


'''Logging'''

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


'''HTML Scraping (news)'''


class ScraperYandex:
    def __init__(self):
        self.url = 'https://yandex.ru/news/'
        self.markup = requests.get(self.url).text
        self.saved_links = set()
        self.available_themes = []
        self.available_themeslinks = []
        self.soup = BeautifulSoup(self.markup, 'html.parser')
        self.captcha_encounter = ''

    def most_popular_news(self):
        captcha = self.soup.findAll('div', {"class": "CheckboxCaptcha"})

        if captcha:
            self.captcha_encounter = 'Captcha encountered'
            print(self.captcha_encounter)

        self.markup = requests.get(self.url).text
        if self.markup:
            links = self.soup.findAll('a', {"class": "mg-card__link"})
            if links:
                for item in links:
                    print(item)
                    link = str(item).split('href="')[1].split('" rel')[0]
                    self.saved_links.add(link)
                print(self.saved_links)
                return self.saved_links
            else:
                print(f'No links found. (Links are: {links})')

    def get_categories(self):
        captcha = self.soup.findAll('div', {"class": "CheckboxCaptcha"})

        if captcha:
            print("captcha encounter!")

        themes_spans = self.soup.findAll('span', {"class": "news-navigation-menu__title"})
        themes_links = self.soup.findAll('a', {"class": "news-navigation-menu__item"})
        dictionary = {}

        for item in themes_spans:
            item = str(item)
            theme_name = item.split('>')[1].split('<')[0]
            self.available_themes.append(theme_name)

        for item in themes_links:
            item = str(item)
            theme_link = item.split('href="')[1].split('" rel')[0]
            self.available_themeslinks.append(theme_link)

        i = 0
        for item in self.available_themes:
            dictionary.update({item: self.available_themeslinks[i]})
            i += 1

        if len(self.available_themes) != len(themes_links):
            print("error in lengths of arrays. Not able to create categories dictionary!")
            return Exception
        return self.available_themes, dictionary


def get_tags():
    tags_list = []
    try:
        tags_url = 'https://ria.ru/tags/?page=1'
        markup = requests.get(tags_url).text
        soup = BeautifulSoup(markup, 'html.parser')

        tags = soup.findAll('a', {'class': 'tags__list-item'})
        for item in tags:
            item = str(item)
            tags_trim = item.split('>')[1].split('</')[0]
            tags_list.append(tags_trim)
        top10 = tags_list[:10]
        return top10
    except Exception as ex:
        print(ex)


def get_news(get_categories=False):
    result_set = set()

    if get_categories:
        categories = ScraperYandex().get_categories()[0]
        print(f'Категории: {categories}')

    try:
        news_set = ScraperYandex().most_popular_news()
        for link in news_set:
            link_trim = str(link).split('href="')[1].split('" rel')[0]
            result_set.add(link_trim)

    except Exception as ex:
        print(ex)


def sort_news(links_set, sort_duplicates=True):
    print('sorting links...')
    if sort_duplicates:
        with open('links_register.txt', 'r') as file:
            if file.read():
                links_reg = ast.literal_eval(file.read())
                result_set = links_set.difference(links_reg)
                return result_set
            else:
                print(f'The register is empty. Have nothing to compare to')
                return links_set


def write_news_to_file(links_set, file_name1='news_links.txt', file_name2='links_register.txt', write_only_sorted=True):
    print('starting to write links')

    if write_only_sorted:
        links_set = sort_news(links_set)

    with open(file_name1, 'w') as file:
        for item in links_set:
            print(item)
            item = str(item)
            file.write(item + '\n')

    with open(file_name2, 'w+') as file:
        file.write(str(links_set))


'''Main function (maintenance)'''


def get_link():

    links_list = open('news_links.txt').readlines()
    links_left = len(links_list)

    print(f"Getting a link. The amount of links there are left: {links_left}")

    if links_list:
        links_list = open('news_links.txt', 'r').readlines()

        link_to_return = links_list[0]

        links_list.pop(0)

        with open('news_links.txt', 'w') as file:
            for item in links_list:
                item = str(item)
                file.write(item)

    else:
        print('Need to go set some news...')

        links_set = set()
        tries_count = 0
        while not links_set:
            tries_count += 1
            print(f'Trying to get news. This is my {tries_count} try...')

            links_set = ScraperYandex().most_popular_news()

            if not links_set:
                print(f'Try not successful :('
                      f'Going to sleep for 10 minutes')
                time.sleep(600)

            if tries_count >= 5:
                print(f"Getting news run unseccessfully")
                break

        write_news_to_file(links_set)

        links_list = open('news_links.txt').readlines()
        link_to_return = links_list[0]

    return link_to_return

