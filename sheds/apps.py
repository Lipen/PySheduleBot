from django.apps import AppConfig

from . import utils

import logging


class ShedsConfig(AppConfig):
    name = 'sheds'

    def ready(self):
        logging.basicConfig(filename='all.log', level=logging.DEBUG, format='@%(levelname)s %(asctime)s %(message)s', datefmt='[%d.%m.%y] [%I:%M:%S %p]')
        utils.setup_logger('telegram.bot.requests', 'requests_raw.log', stream=False)
        utils.setup_logger('telegram.bot.conversation', 'conversation.log', fmt='%(asctime)s %(message)s')
