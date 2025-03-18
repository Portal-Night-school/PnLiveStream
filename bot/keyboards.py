from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🐳 DeepSeek"), KeyboardButton(text="✨ Gemini"), KeyboardButton(text="🖼️ Kandinsky")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажимая на соответствующую кнопку, ты сразу попадаешь в чат с нейросетью и можешь начинать с ней работы"
)

stop_context = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Завершить диалог", callback_data="stop")
        ]
    ]
)

stop_kandinsky = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Завершить генерацию", callback_data="stop_generation")
        ]
    ]
)

rmk = ReplyKeyboardRemove()