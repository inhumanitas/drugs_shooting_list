#!/usr/bin/env python

import logging

from telegram import Bot

from drugs_shooting_list.settings import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Bot(TOKEN)
