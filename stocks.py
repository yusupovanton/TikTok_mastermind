import asyncio

from handlers.dispatcher import *

EXCHANGE = 'ME'
if not os.path.exists("images"):
    os.mkdir("images")


API_KEY = "c62iqiaad3iad17mv92g"
finnhub_client = finnhub.Client(API_KEY)
pairs = {}
dict = {}
app = dash.Dash(__name__)

# print('enter a ticker and metrics')
# usrinput = list(map(str, input().split()))

company = 'gazprom'
ticker = 'GAZP'
fromdate = "2022-01-01"
todate = "2022-01-01"


def symbol_lookup(user_input):

    df = pd.DataFrame(columns=['description', 'symbol'])

    stocks = finnhub_client.symbol_lookup(user_input)['result']

    if stocks:
        col = 0

        for stock in stocks:
            description = stock['description']
            symbol = stock['symbol'].split('.')[0]
            df.loc[col] = [description, symbol]
            col += 1

        return df


def get_available_stocks(SE):
    available_stocks = finnhub_client.stock_symbols(SE)

    df = pd.DataFrame(columns=['description', 'displaySymbol', 'symbol', 'type'])
    col = 0

    for stock in available_stocks:

        description = stock['description']
        display_symbol = stock['displaySymbol']
        symbol = stock['symbol']
        type = stock['type']

        df.loc[col] = [description, display_symbol, symbol, type]
        col += 1
    df_file_name = f"stocksAvailable/stocksavailable{SE}.html"
    df.to_html(df_file_name)

    return df_file_name


async def get_general_news():
    """GETS NEWS FROM FINNHUB IO"""

    while True:
        news_list = []

        logger.info(f"Getting stock news...")
        with open('news/last_id.txt', 'r') as file:
            id_ = file.read()

        news = finnhub_client.general_news('general', min_id=id_)

        for item in news:

            hashtag = item['category']
            text = item['headline']
            img_url = item['image']
            url = item['url']
            id_ = item['id']
            dict_ = {'id': id_,
                     'hashtag': hashtag,
                     'text': text,
                     'img_url': img_url,
                     'url': url}

            news_list.append(dict_)

        last_id = id_

        with open('news/last_id.txt', 'w') as file:
            file.write(f'{last_id} \n')

        with open('news/news_register.txt', 'w') as file:
            for item in news_list:
                file.write(f"{str(item)} \n")

        await asyncio.sleep(600)


def get_company_news(ticker, fromdate, todate):

    news = finnhub_client.company_news(ticker, _from=fromdate, to=todate)
    for item in news:
        headline = item['headline']
        image = item['image']
        summary = item['summary']
        url = item['url']


def get_basic_financials(ticker):
    financials = finnhub_client.company_basic_financials(ticker, 'all')
    if financials['metric']:
        df = pd.DataFrame.from_dict(financials['metric'], orient='index')
        df.columns = ['value']
        df_file_name = f"metricsTables/{ticker.upper()}metrics.html"
        df.to_html(df_file_name)
        return df_file_name
    else:
        return False


def main(user_input=None):
    pass
    print(get_general_news())


if __name__ == '__main__':
    main()
