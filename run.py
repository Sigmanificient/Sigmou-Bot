import logging
from app.bot import Bot

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    bot: Bot = Bot(prefix='=')
    bot.run()
