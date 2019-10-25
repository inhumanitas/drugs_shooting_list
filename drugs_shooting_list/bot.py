#!/usr/bin/env python

import logging

from telegram import Bot, ParseMode

from drugs_shooting_list.settings import TOKEN, ADMIN_UID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Bot(TOKEN)


def notify_admin(text, admin_uid=ADMIN_UID, parse_mode=ParseMode.HTML):
    bot.send_message(
        admin_uid,
        text,
        disable_web_page_preview=True,
        parse_mode=parse_mode,
    )
