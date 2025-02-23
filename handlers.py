# handlers.py
from aiogram import types
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import get_animal_keyboard, get_action_keyboard, ANIMAL_QUERIES
from gif_manager import get_random_gif
import logging

logger = logging.getLogger(__name__)
stats = {"total": 0, "by_animal": {}}

async def send_welcome(message: types.Message, bot: Bot):
    """Handler for the /start command with a 'Start' button."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start_choice")]
    ])
    await message.reply("Hello! Press 'Start' to choose an animal for GIFs!", reply_markup=keyboard)

async def send_stats(message: types.Message, bot: Bot):
    """Handler for the /stats command to show usage statistics."""
    if stats["total"] == 0:
        await message.reply("You haven’t received any GIFs yet!")
    else:
        stats_text = f"Total GIFs: {stats['total']}\n"
        for animal, count in stats["by_animal"].items():
            stats_text += f"{animal}: {count}\n"
        await message.reply(stats_text)

async def process_start(callback: types.CallbackQuery, bot: Bot):
    """Handler for the 'Start' button."""
    await callback.message.reply(
        "Choose an animal, and I’ll send you GIFs with it!",
        reply_markup=get_animal_keyboard()
    )
    await callback.answer()

async def process_animal_choice(callback: types.CallbackQuery, bot: Bot, used_gifs: dict, gif_cache: dict):
    """Handler for animal selection."""
    query = callback.data.split("_")[1]
    animal_name = [k for k, v in ANIMAL_QUERIES.items() if v == query][0]
    loading_msg = await callback.message.reply("Loading...")
    gif_url = await get_random_gif(query, used_gifs, gif_cache)
    await bot.delete_message(callback.message.chat.id, loading_msg.message_id)
    if gif_url:
        try:
            await bot.send_animation(callback.message.chat.id, gif_url)
            await callback.message.reply(
                f"Here’s your GIF with {animal_name.lower()}!",
                reply_markup=get_action_keyboard(query)
            )
            stats["total"] += 1
            stats["by_animal"][animal_name] = stats["by_animal"].get(animal_name, 0) + 1
        except TelegramBadRequest as e:
            logger.error(f"Telegram failed to send GIF: {gif_url} - {str(e)}")
            await callback.message.reply(
                "Couldn’t send the GIF due to a Telegram error. Try again!",
                reply_markup=get_action_keyboard(query)
            )
    else:
        await callback.message.reply(
            "Couldn’t find a GIF. Try again!",
            reply_markup=get_animal_keyboard()
        )
    await callback.answer()

async def process_more_gif(callback: types.CallbackQuery, bot: Bot, used_gifs: dict, gif_cache: dict):
    """Handler for the 'More' button."""
    query = callback.data.split("_")[1]
    animal_name = [k for k, v in ANIMAL_QUERIES.items() if v == query][0]
    loading_msg = await callback.message.reply("Loading...")
    gif_url = await get_random_gif(query, used_gifs, gif_cache)
    await bot.delete_message(callback.message.chat.id, loading_msg.message_id)
    if gif_url:
        try:
            await bot.send_animation(callback.message.chat.id, gif_url)
            await callback.message.reply(
                f"Another GIF with {animal_name.lower()}!",
                reply_markup=get_action_keyboard(query)
            )
            stats["total"] += 1
            stats["by_animal"][animal_name] = stats["by_animal"].get(animal_name, 0) + 1
        except TelegramBadRequest as e:
            logger.error(f"Telegram failed to send GIF: {gif_url} - {str(e)}")
            await callback.message.reply(
                "Couldn’t send the GIF due to a Telegram error. Try again!",
                reply_markup=get_action_keyboard(query)
            )
    else:
        await callback.message.reply(
            "Couldn’t find another GIF. Try later!",
            reply_markup=get_action_keyboard(query)
        )
    await callback.answer()

async def process_choose_another(callback: types.CallbackQuery, bot: Bot):
    """Handler for the 'Another Animal' button."""
    await callback.message.reply(
        "Choose another animal!",
        reply_markup=get_animal_keyboard()
    )
    await callback.answer()