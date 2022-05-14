import random

from handlers.dispatcher import *
from handlers.config import *
from bot import stock_news, regular_news
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


async def broadcaster(task: str) -> None:

    if task == 'tiktok_video':
        pass

    elif task == 'stocks_news':
        successful_msg = 0
        while True:
            news_text = stock_news()  # Getting a link from Finnhub
            if await send_message(user_id=STOCKS_NEWS_CHANNEL_ID, text=news_text):
                successful_msg += 1
                time_sleep = random.randint(360, 720)
                logger.info(f'Stock news post successful. Going to sleep for ({time_sleep}s).\nSuccessful stock news sent: '
                            f'{successful_msg}')
                await asyncio.sleep(time_sleep)

    elif task == 'reg_news':
        successful_msg = 0
        while True:
            news_text = regular_news()  # Getting a link from the register
            if await send_message(user_id=REG_NEWS_CHANNEL_ID, text=news_text):
                successful_msg += 1
                time_sleep = random.randint(360, 720)
                logger.info(f'News post successful. Going to sleep for ({time_sleep}s).\nSuccessful yandex news sent: '
                            f'{successful_msg}')
                await asyncio.sleep(time_sleep)

    else:
        print(f'Wrong task name passed: {task}')


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

    task1 = asyncio.create_task(background_on_start(task="stocks_news"))
    task2 = asyncio.create_task(background_on_start(task="reg_news"))

    logger.debug(f"{task1}, {task2}")


def create_bot_factory(**kwargs) -> None:
    # bot endpoints block:
    dp.register_message_handler(
        background_task_creator,
        commands=['start']
    )
    # start bot
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)
