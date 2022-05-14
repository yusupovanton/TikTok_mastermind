import urllib.request

from news import get_link
from stocks import *

from handlers.personal_actions import *
import ast


def stock_news():
    """"""
    with open('news/news_register.txt', 'r') as file:

        news_list = file.readlines()
        if len(news_list) <= 2:
            get_general_news()

    if news_list:
        item = ast.literal_eval(news_list[0])

        hashtag = item['hashtag']
        text = item['text']
        img_url = item['img_url']
        url = item['url']
        first_word = text.split(' ', 1)[0]
        text_after = text.split(' ', 1)[1]

        news_list.pop(0)

        message = f"<a href='{url}'>{first_word}</a> {text_after} \n#{hashtag}"

        with open('news/news_register.txt', 'w') as file:
            for item in news_list:
                file.write(f"{str(item)}")

        return message


def regular_news() -> str:

    """TAKES A LINK FROM THE REGISTER AND EXTRACTS TEXT FROM IT"""

    reason = ""
    link = get_link()

    markup = requests.get(link).text
    soup = BeautifulSoup(markup, 'html.parser')

    article_text = soup.findAll('h1', {'class': 'mg-story__title'})
    captcha = soup.findAll('div', {"class": "CheckboxCaptcha"})

    if captcha:
        reason = "Captcha Encounter!"

    try_count = 0

    while not article_text:

        try_count += 1
        print(f'{try_count} tries to get article header attempted, but not successful. Reason: {reason}. '
              f'Going to sleep for 6 minutes')
        time.sleep(360)
        markup = requests.get(link).text
        article_text = soup.findAll('h1', {'class': 'mg-story__title'})

    if article_text:

        # HANDLING THE HTML FORMAT
        tags = str(article_text[0])
        tags = tags.split('target="_blank">')[1]
        new_tags = tags.split('</')[0]
        word = new_tags.split(' ')[0]

        after_word = new_tags.split(' ', 1)[1:]
        text = f"<a href='{link}'>{word}</a> {after_word[0]}"
    else:
        text = ""

    return text


def main():

    create_bot_factory()
    pass
    

if __name__ == '__main__':

    main()
