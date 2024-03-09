from functools import wraps
from fastapi import HTTPException

from telegram import Bot

from logger import logger
from tg_utils.constants import BOT_TOKEN

bot = Bot(BOT_TOKEN)

chat_id = 403060296


async def send_message(
    text: str,
    chat_id: int,
) -> None:
    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )


def send_message_on_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except HTTPException:
            raise

        except Exception as e:
            await send_message(
                text='Test Task system got critical error',
                chat_id=chat_id,
            )

            logger.error(f'GOT ERROR: {e}')

            raise

    return wrapper
