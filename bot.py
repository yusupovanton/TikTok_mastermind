from aiogram import executor
from dispatcher import dp
import handlers
from handlers.personal_actions import broadcaster
from tiktok import *
from stocks import *
folder = VIDS_FOLDER

if __name__ == '__main__':
    message2 = ''

    if are_vids_low(folder):
        print('hello')
        get_tiktok_vids(30, folder)
        print('hello')

    file = getrandom_fromos(folder)[0]
    file_name = getrandom_fromos(folder)[1]
    video = file

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

        message2 = f"<a href='{url}'>{first_word}</a> {text_after}"

    executor.start(dp, broadcaster(video=video, message=message2))

    filedelete(folder, file_name)

    print('Video post successful')
    print('News post successful')
    print('Going to sleep now for 30 mins')

    time.sleep(60 * 30)
