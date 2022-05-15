import asyncio

from handlers.dispatcher import *

'''HTML Scraping (news)'''


class ScraperYandex:
    def __init__(self):
        self.url = 'https://yandex.ru/news/'
        self.markup = requests.get(self.url).text
        self.saved_links = set()
        self.available_themes = []
        self.available_themeslinks = []
        self.soup = BeautifulSoup(self.markup, 'html.parser')
        self.reason = ''

    async def most_popular_news(self) -> set:
        """ACCESSES YANDEX AND SCRAPES FOR NEWS. RETURNS A SET OF LINKS FOR THE NEWS"""

        logger.info(f"Accessing Yandex...")
        captcha = self.soup.findAll('div', {"class": "CheckboxCaptcha"})
        request_try = 0

        while captcha:
            request_try += 1
            self.reason = f'Captcha encountered at Yandex for the {request_try} time'
            logger.warning(self.reason)
            await asyncio.sleep(600)
            self.markup = requests.get(self.url).text
            self.soup = BeautifulSoup(self.markup, 'html.parser')
            captcha = self.soup.findAll('div', {"class": "CheckboxCaptcha"})

        links = self.soup.findAll('a', {"class": "mg-card__link"})

        if links:
            logger.info(f"Success! Found {len(links)} links at Yandex!")
            for item in links:
                link = str(item).split('href="')[1].split('" rel')[0]
                self.saved_links.add(link)
        else:
            print(f'No links found. (Links are: {links})')

        return self.saved_links

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


async def get_news(get_categories=False):
    result_set = set()

    if get_categories:
        categories = ScraperYandex().get_categories()[0]

    try:
        news_set = await ScraperYandex().most_popular_news()
        for link in news_set:
            link_trim = str(link).split('href="')[1].split('" rel')[0]
            result_set.add(link_trim)

    except Exception as ex:
        logger.error(ex)


def sort_news(links_set: set) -> set:

    """SORTS THE GIVEN SET OF LINKS BASED ON THE REGISTER OF LINKS THAT THE BOT HAS ALREADY SENT"""
    logger.info('Sorting links...')

    result_set = set()

    with open('news/yandex_links_register.txt', 'r') as file:
        links_reg_set = ast.literal_eval(file.read())

        for link in links_set:
            persistent_id = link.split("persistent_id=")[1].split("&amp")[0]
            if persistent_id not in links_reg_set:
                result_set.add(link)
            links_reg_set.add(persistent_id)

    with open('news/yandex_links_register.txt', 'w') as file:
        file.write(str(links_reg_set))

    return result_set


def write_news_to_file(links_set: set, file_name1='news_links.txt', file_name2='yandex_links_register.txt', write_only_sorted=True):
    """WRITES THE GIVEN LINKS TO A CORRESPONDING FILE"""

    logger.info('Writing links to file...')
    if write_only_sorted:
        links_set = sort_news(links_set)

    with open(file_name1, 'a') as file:
        for item in links_set:
            item = str(item)
            file.write(item + '\n')

    with open(file_name2, 'w+') as file:
        file.write(str(links_set))


async def get_link() -> str:

    links_list = open('news_links.txt').readlines()
    links_left = len(links_list)
    link_to_return = ""

    logger.info(f"Getting a Yandex link from the file. The amount of Y-links there are left: {links_left}")

    if links_list:
        links_list = open('news_links.txt', 'r').readlines()
        link_to_return = links_list[0]
        links_list.pop(0)

        with open('news_links.txt', 'w') as file:
            for item in links_list:
                item = str(item)
                file.write(item)

    else:
        logger.info('Zero links left in the file! Need to go set some news...')
        await asyncio.sleep(600)

    return link_to_return


async def get_yandex_news_and_write_them_to_file():
    """Gets Yandex news and writes them to a dedicated file"""

    logger.info("Entered coroutine for searching and writing Y-news.")

    while True:

        li = await ScraperYandex().most_popular_news()
        if li:
            write_news_to_file(li, write_only_sorted=True)
            logger.info(f"Successfully wrote the links to the file!")
            await asyncio.sleep(600)

        else:
            logger.error(f"Error in getting and writing Yandex news!")


if __name__ == '__main__':
    get_yandex_news_and_write_them_to_file()

