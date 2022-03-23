from handlers.dispatcher import *
from handlers.config import *
from bot import stock_news
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(**kwargs):
    while True:
        for key, value in kwargs.items():

            if key == 'tiktok_video':
                await bot.send_video(chat_id=TIKTOK_CHANNEL_ID, video=value)
                print('TikTok video post successful. Going to sleep now...')
                time_sleep = 600
                time.sleep(time_sleep)

            elif key == 'stocks_news_text':
                if await send_message(user_id=STOCKS_NEWS_CHANNEL_ID, text=value):
                    print('Stock news post successful. Going to sleep now...')
                    time_sleep = 600
                    time.sleep(time_sleep)

            elif key == 'reg_news_text':
                if await send_message(user_id=REG_NEWS_CHANNEL_ID, text=value):
                    print('News post successful. Going to sleep now...')

                    time_sleep = 600
                    time.sleep(time_sleep)
            else:
                print(f'Wrong name in the description of the variable passed {key}')


async def background_on_start(**kwargs) -> None:
    """background task which is created when bot starts"""
    while True:

        await broadcaster(**kwargs)


async def background_on_action() -> None:
    """background task which is created when user asked"""
    for _ in range(20):
        await asyncio.sleep(3)
        print("Action!")


async def background_task_creator(message: types.Message) -> None:
    """Creates background tasks"""
    asyncio.create_task(background_on_action())
    await message.reply("Another one background task create")


async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    """List of actions which should be done before bot start"""
    news_text = stock_news()
    asyncio.create_task(background_on_start(stocks_news_text=news_text))


def create_bot_factory(**kwargs) -> None:
    # bot endpoints block:
    dp.register_message_handler(
        background_task_creator,
        commands=['start']
    )
    # start bot
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)
