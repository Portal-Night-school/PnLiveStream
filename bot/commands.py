from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboards import start_keyboard

rt = Router()


@rt.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer(f"Здравствуй, {msg.from_user.full_name}\! Добро пожаловать в агрегатор нейросетей\. Через этого бота у тебя есть возможность работать с различными нейросетями\.\n\n"\
                    "Агрегатор находится *в процессе разработки* и функционал будет добавляться\. Работа идёт в рамках проекта [Вечерняя школа](https://t.me/portal_energy/180)\. Если тебе интересна эта тема и есть желание учиться, то ты можешь *присоединиться к проекту и внести свой вклад его развитие\.*\n\n"\
                    "Наша задача не просто повторить функционал других аналогичных ботов, а *разобраться в теме ИИ* и научиться пользоваться всем многообразием инструментов и *научиться создавать свои\.*")
    
    await msg.answer("На данный момент реализована работа со следующими нейросетями", reply_markup=start_keyboard)
