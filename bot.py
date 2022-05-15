from news import get_link
from stocks import get_general_news
from handlers.personal_actions import *

logger.info(f"\nRUN STARTED ============================")


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

    reason = "N/A"
    link = get_link()

    markup = requests.get(link).text
    soup = BeautifulSoup(markup, 'html.parser')

    article_text = soup.findAll('h1', {'class': 'mg-story__title'})
    captcha = soup.findAll('div', {"class": "CheckboxCaptcha"})
    story_not_found = soup.findAll('div', {"class": "mg-story-not-found mg-grid__item"})

    try_count = 0

    while not article_text:
        try_count += 1

        if captcha:
            reason = "captcha encounter"
        elif story_not_found:
            reason = "story not found"
            logger.info(f"Will going to use a new link")
            link = get_link()  # Getting a new link since this does not work
        elif not captcha and not story_not_found:
            logger.error(f"Have not detected error type! Wrote soup to file...\nThe link is {link}")
            with open("error_soup_message.txt", 'w+') as error_file:
                error_file.write(soup.text)

        logger.warning(f'{try_count} tries to get article header attempted, but not successful. Reason: {reason}. '
                       f'Going to sleep for 10 minutes')
        time.sleep(600)

        logger.info(f"Attempting to reach the link again...")
        markup = requests.get(link).text
        soup = BeautifulSoup(markup, 'html.parser')
        article_text = soup.findAll('h1', {'class': 'mg-story__title'})

        if try_count >= 3:
            logger.error(f"Error in getting the article text for the link {link}")
            return ""

    logger.info(f"Have successfully found the article for the link.")

    # HANDLING THE HTML FORMAT
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
