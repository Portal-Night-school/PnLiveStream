from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboards import start_keyboard

rt = Router()


@rt.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer("Привет\! Это агрегатор нейросетей прямо в Telegram \(никогда такого не было\. И вот опять\)\n\nВыбери нейросеть",
                     reply_markup=start_keyboard)
