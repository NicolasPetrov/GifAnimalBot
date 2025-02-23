# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ANIMALS = ["Cats", "Dogs", "Capybaras", "Parrots", "Pandas", "Otters"]
ANIMAL_QUERIES = {
    "Cats": "cat", "Dogs": "dog", "Capybaras": "capybara",
    "Parrots": "parrot", "Pandas": "panda", "Otters": "otter"
}

def get_animal_keyboard():
    """Creates a keyboard with animals in two columns."""
    buttons = []
    for i in range(0, len(ANIMALS), 2):
        row = [InlineKeyboardButton(text=ANIMALS[i], callback_data=f"animal_{ANIMAL_QUERIES[ANIMALS[i]]}")]
        if i + 1 < len(ANIMALS):
            row.append(InlineKeyboardButton(text=ANIMALS[i + 1], callback_data=f"animal_{ANIMAL_QUERIES[ANIMALS[i + 1]]}"))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_action_keyboard(query):
    """Creates a keyboard with actions after a GIF."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="More", callback_data=f"more_{query}"),
            InlineKeyboardButton(text="Another Animal", callback_data="choose_another")
        ]
    ])