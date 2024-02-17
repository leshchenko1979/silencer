# This telegram bots receives updates from a telegram channel and silences all new members dor three days.
# So, a new member will be allowed to send messages only after three days since his joining.
# Also, if a new member has managed to post something between the time he joined and the bot ran,
# the bot should remove all the messages from this new member.

import json
import os

import dotenv
from aiogram import Bot

from handlers import dp
from yandex_logging import logger

dotenv.load_dotenv()
bot = Bot(token=os.environ["TOKEN"])


async def yandex_function_handler(event, context):
    update = json.loads(event["body"])

    logger.info("Incoming update", extra={"update": update})

    await dp.feed_raw_update(bot, update)

    logger.debug("Finished successfully")

    return {"statusCode": 200, "body": "ok"}
