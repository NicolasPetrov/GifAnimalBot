# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging
from config import TELEGRAM_TOKEN
from handlers import (
    send_welcome, process_start, process_animal_choice,
    process_more_gif, process_choose_another, send_stats
)
from keyboards import ANIMAL_QUERIES
from gif_manager import load_used_gifs
from aiogram.exceptions import TelegramNetworkError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot=bot)
used_gifs = load_used_gifs()
gif_cache = {query: [] for query in ANIMAL_QUERIES.values()}

@dp.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    await send_welcome(message, bot)

@dp.message(Command(commands=["stats"]))
async def stats_handler(message: types.Message):
    await send_stats(message, bot)

@dp.callback_query(lambda c: c.data == "start_choice")
async def start_callback_handler(callback: types.CallbackQuery):
    await process_start(callback, bot)

@dp.callback_query(lambda c: c.data.startswith("animal_"))
async def animal_choice_handler(callback: types.CallbackQuery):
    await process_animal_choice(callback, bot, used_gifs, gif_cache)

@dp.callback_query(lambda c: c.data.startswith("more_"))
async def more_gif_handler(callback: types.CallbackQuery):
    await process_more_gif(callback, bot, used_gifs, gif_cache)

@dp.callback_query(lambda c: c.data == "choose_another")
async def choose_another_handler(callback: types.CallbackQuery):
    await process_choose_another(callback, bot)

async def main():
    logger.info("Starting bot polling...")
    max_retries = 5
    for attempt in range(max_retries):
        try:
            await dp.start_polling(bot)
            break
        except TelegramNetworkError as e:
            logger.error(f"Network error: {str(e)}. Retrying {attempt + 1}/{max_retries}...")
            if attempt < max_retries - 1:
                await asyncio.sleep(5)  # Wait 5 seconds before retrying
            else:
                logger.error("Max retries reached. Exiting.")
                raise

if __name__ == "__main__":
    asyncio.run(main())