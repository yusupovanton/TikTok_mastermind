from news import *
from stocks import *
from tiktok import *
from handlers.personal_actions import *
import ast


def stock_news():
    """"""
    with open('news/news_register.txt', 'r') as file:

        news_list = file.readlines()
        if len(news_list) <= 2:
            get_general_news()
    print(news_list)
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


def regular_news():
    link = get_link()
    print(link)
    markup = requests.get(link).text
    soup = BeautifulSoup(markup, 'html.parser')

    article_text = soup.findAll('h1', {'class': 'mg-story__title'})

    while not article_text:
        print('Try to get header attempted, but not successful. Going to sleep for 10 minutes')
        time.sleep(600)
        article_text = soup.findAll('h1', {'class': 'mg-story__title'})

    if article_text:
        tags = str(article_text[0])
        tags = tags.split('target="_blank">')[1]
        new_tags = tags.split('</')[0]
        word = new_tags.split(' ')[0]

        after_word = new_tags.split(' ', 1)[1:]
        text = f"<a href='{link}'>{word}</a> {after_word[0]}"
        return text


def main():

    create_bot_factory()
    pass
    

if __name__ == '__main__':

    main()
