from tiktok import *
from stocks import *
from news import *

from aiogram import executor
from dispatcher import dp

from handlers.personal_actions import broadcaster
from config import VIDS_FOLDER
import bs4


def tiktok(folder=VIDS_FOLDER):
    if are_vids_low(folder):

        get_tiktok_vids(30, folder)

    file = getrandom_fromos(folder)[0]
    file_name = getrandom_fromos(folder)[1]
    video = file
    return video, file_name


def stock_news():
    news_list = get_general_news()
    print(news_list)
    if news_list:
        item = news_list[0]

        hashtag = item['hashtag']
        text = item['text']
        img_url = item['img_url']
        url = item['url']
        first_word = text.split(' ', 1)[0]
        text_after = text.split(' ', 1)[1]

        news_list.pop(0)

        message = f"<a href='{url}'>{first_word}</a> {text_after} \n#{hashtag}"
        return message


def regular_news():
    link = get_link()
    print(link)
    markup = requests.get(link).text
    soup = bs4.BeautifulSoup(markup, 'html.parser')

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

    video = tiktok()[0]
    stock_news_ = stock_news()
    regular_news_ = regular_news()

    if video and stock_news_ and regular_news_:
        executor.start(dp, broadcaster(tiktok_video=video, stocks_news_text=stock_news_, reg_news_text=regular_news_))
        print('News post successful!')
    else:
        print(f'A variable is missing. video: {tiktok()[1]}, stock_news: {stock_news_}, regular_news: {regular_news_}')

    filedelete(folder, tiktok()[1])


if __name__ == '__main__':
    main()
