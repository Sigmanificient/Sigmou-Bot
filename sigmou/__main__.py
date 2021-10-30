from sigmou.bot import Bot
from sigmou.utils.timer import time

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    time("start", keep=True)
    bot: Bot = Bot(prefix='=')
    bot.run()
