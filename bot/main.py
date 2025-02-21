from aiogram import Bot, Dispatcher
import asyncio 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
import os
import handlers
import commands
import logging


load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Бот запущен')


async def main():
    dp.include_routers(
        commands.rt,
        handlers.rt
    )
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())