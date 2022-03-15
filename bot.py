from tiktok import *
from stocks import *
from news import *
from csgo import *
from dash_actions import dash_main_function

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

    dash_main_function()
    cs_go_main_function(sleep_time=300)
    

if __name__ == '__main__':
    main()
