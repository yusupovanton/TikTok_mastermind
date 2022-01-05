import time

from aiogram import types
from aiogram.dispatcher.webhook import SendDocument
from aiogram import Bot, Dispatcher, types
from dispatcher import dp, log
from config import API_TOKEN, NEWS_CHANNEL_ID
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


async def broadcaster(message, video):

    await bot.send_video(chat_id=CHANNEL_ID, video=video)

    if await send_message(user_id=NEWS_CHANNEL_ID,
                          text=message):
        print('News post successful')


