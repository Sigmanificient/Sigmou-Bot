import logging

from sigmou.utils.timer import time

from . import Bot

logging.basicConfig(level=logging.DEBUG)


def main():
    time("start", keep=True)
    bot: Bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
