import logging

from . import Bot

logging.basicConfig(level=logging.DEBUG)


def main():
    bot = Bot()
    bot.setup_events()
    bot.run()


if __name__ == "__main__":
    main()
