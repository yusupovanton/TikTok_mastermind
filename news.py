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
        self.captcha_encounter = ''

    def most_popular_news(self) -> set:
        captcha = self.soup.findAll('div', {"class": "CheckboxCaptcha"})

        if captcha:
            self.captcha_encounter = 'Captcha encountered'
            print(self.captcha_encounter)

        self.markup = requests.get(self.url).text
        if self.markup:
            links = self.soup.findAll('a', {"class": "mg-card__link"})
            if links:
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


def get_news(get_categories=False):
    result_set = set()

    if get_categories:
        categories = ScraperYandex().get_categories()[0]

    try:
        news_set = ScraperYandex().most_popular_news()
        for link in news_set:
            link_trim = str(link).split('href="')[1].split('" rel')[0]
            result_set.add(link_trim)

    except Exception as ex:
        logger.error(ex)


def sort_news(links_set) -> set:

    """SORTS THE GIVEN SET OF LINKS BASED ON THE REGISTER OF LINKS THAT THE BOT HAS ALREADY SENT"""
    logger.info('Sorting links...')

    if links_set:
        with open('links_register.txt', 'r') as file:

            links_reg = ast.literal_eval(file.read())
            result_set = links_set.difference(links_reg)
    else:
        logger.error(f"Empty set was given to sort. That is not going to work!")
        result_set = set()

    return result_set


def write_news_to_file(links_set: set, file_name1='news_links.txt', file_name2='links_register.txt', write_only_sorted=True):
    """WRITES THE GIVEN LINKS TO A CORRESPONDING FILE"""

    logger.info('Writing links to file...')

    if write_only_sorted:
        links_set = sort_news(links_set)

    with open(file_name1, 'w') as file:
        for item in links_set:
            item = str(item)
            file.write(item + '\n')

    with open(file_name2, 'w+') as file:
        file.write(str(links_set))


def get_link() -> str:

    links_list = open('news_links.txt').readlines()
    links_left = len(links_list)
    link_to_return = ""

    logger.info(f"Getting a link. The amount of links there are left: {links_left}")

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

        links_set = set()
        tries_count = 0
        time_increase = 0

        while not links_set:
            tries_count += 1
            time_increase += 5
            logger.warning(f'Trying to get news. This is my {tries_count} try...')

            links_set = ScraperYandex().most_popular_news()

            if not links_set:  # IF DIDN'T FIND LINKS - SEARCH AGAIN
                time_span = 2 + time_increase
                logger.warning(f'Try not successful :('
                               f'Going to sleep for {time_span} minutes')
                time.sleep(time_span * 60)
                links_set = ScraperYandex().most_popular_news()

            elif tries_count > 5 and not links_set:  # BREAK CONDITION
                logger.error(f"Getting news run unsuccessfully")
                link_to_return = ""
                break

            elif links_set:  # IF FOUND LINKS
                write_news_to_file(links_set)
                logger.info(f"Wrote {len(links_set)} links to file. Will try to get a link again.")
                get_link()

    return link_to_return


def main():

    li = ScraperYandex().most_popular_news()
    if li:
        write_news_to_file(li, write_only_sorted=True)
    else:
        time.sleep(30)
        main()


if __name__ == '__main__':
    main()

