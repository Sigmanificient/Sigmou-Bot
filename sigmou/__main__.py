import logging

from . import Bot
from sigmou.utils.timer import time

logging.basicConfig(level=logging.DEBUG)


def main():
    time("start", keep=True)
    bot: Bot = Bot(prefix='=')
    bot.run()


if __name__ == '__main__':
    main()
