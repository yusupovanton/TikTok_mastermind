import random
import time

from aiogram import Bot, Dispatcher, types
from dispatcher import dp, log
from config import *
from stocks import get_general_news
from tiktok import *
from aiogram.types import InputFile
from aiogram.utils import exceptions, executor
import logging
import asyncio

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
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(**kwargs):
    for key, value in kwargs.items():

        if key == 'tiktok_video':
            await bot.send_video(chat_id=TIKTOK_CHANNEL_ID, video=value)
            print('TikTok video post successful. Going to sleep now...')
            time_sleep = random.randint(800, 1200)
            time.sleep(time_sleep)

        elif key == 'stocks_news_text':
            if await send_message(user_id=STOCKS_NEWS_CHANNEL_ID, text=value):
                print('Stock news post successful. Going to sleep now...')
                time_sleep = random.randint(800, 1200)
                time.sleep(time_sleep)

        elif key == 'reg_news_text':
            if await send_message(user_id=REG_NEWS_CHANNEL_ID, text=value):
                print('News post successful. Going to sleep now...')

                time_sleep = random.randint(800, 1200)
                time.sleep(time_sleep)
        else:
            print(f'Wrong name in the description of the variable passed {key}')




