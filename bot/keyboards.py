from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="DeepSeek"), KeyboardButton(text="Gemini"), KeyboardButton(text="Kandinsky")
        ]
    ],
    resize_keyboard=True
)

stop_context = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Завершить диалог", callback_data="stop")
        ]
    ]
)

