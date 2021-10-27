import logging
from app.bot import Bot
from app.utils.timer import time

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    time("start", keep=True)
    bot: Bot = Bot(prefix='=')
    bot.run()
