from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import stop_context, start_keyboard
from collections import defaultdict
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv
import base64
import os
import re
from aiogram.utils import markdown
from openai import OpenAI
from kandinsky import Kandinsky
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from main import bot


load_dotenv()


rt = Router()
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
DEEPSEEK_API_KEy = os.getenv('DEEPSEEK_API_KEY')

class chatKandin(StatesGroup):
    kandinski_chat = State()


client_deepseek = OpenAI(api_key=DEEPSEEK_API_KEy, base_url="https://api.deepseek.com")


configure(api_key=GEMINI_API_KEY)
model_gemini = GenerativeModel("gemini-pro")

user_session = defaultdict(lambda: None)
user_context = defaultdict(list)

def ekranirovaniye(text: str) -> str:
    pattern = r"([_*\[\]()~`>#+-=|{}.!\\])"
    return re.sub(pattern, r"\\\1", text)


async def get_deepseek_response(user_id):
    try:
        response = client_deepseek.chat.completions.create(
            model="deepseek-chat",
            messages=user_context[user_id]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при генерации ответа: {e}"



async def get_gemini_response(user_id):
    try:
        messages = [
            {"role": "user", "parts": [msg["content"]]} if msg["role"] == "user"
            else {"role": "model", "parts": [msg["content"]]}
            for msg in user_context[user_id]
        ]
        response = model_gemini.generate_content(messages)
        return response.text if response else "Ошибка при получении ответа"
    except Exception as e:
        return f"Ошибка при генерации ответа: {e}"


@rt.message(F.text == "DeepSeek")
async def start_deepseek(msg: Message):
    user_session[msg.from_user.id] = 'deepseek'
    await msg.answer("Задайте вопрос для DeepSeek", reply_markup=stop_context)


@rt.message(F.text == 'Gemini')
async def start_gemini(msg: Message):
    user_session[msg.from_user.id] = "gemini"
    await msg.answer("Задайте вопрос для Gemini", reply_markup=stop_context)
    

@rt.message(F.text == 'Kandinsky')
async def start_kandinsky(msg: Message, state: FSMContext):
    await msg.answer("Напишите описание картинки")
    await state.set_state(chatKandin.kandinski_chat)
    
    
@rt.message(chatKandin.kandinski_chat)
async def send_picture(msg: Message, state: FSMContext):
    async with ChatActionSender(bot=bot, chat_id=msg.from_user.id, action="upload_video"):
        await msg.answer("Генерация изображения занимает от 30 сек\.\.\.")
        prompt = msg.text
        api = Kandinsky()
        uuid = api.generate(prompt)
        images = api.check_generation(uuid)
        if images:
            image_base64 = images[0]
            image_data = base64.b64decode(image_base64)
            
            dir = f"./media/{uuid}.jpg"
            with open(dir, "wb") as file:
                file.write(image_data)
            
            file = FSInputFile(dir)
            caption = f"Изображение по запросу: {msg.text} сгенерировано!"
            formatted_response = markdown.text(
                markdown.markdown_decoration.quote(
                    caption
                )
            )
            await msg.answer_photo(photo=file, caption=formatted_response)
            os.remove(dir)
        else:
            await msg.answer("Что-то пошло не так, пробую еще раз")
    

    
@rt.callback_query(F.data == 'stop')
async def clear_context(call: CallbackQuery):
    user_session[call.message.from_user.id] = None
    await call.message.answer("Вы закончили диалог", reply_markup=start_keyboard)
    
    
@rt.message()
async def handle_neuro(msg: Message):
    user_id = msg.from_user.id
    model = user_session[user_id]
    
    if model is None:
        await msg.answer("Выберите, пожалуйста, одну из предложенных моделей")
        return
    
    
    user_context[user_id].append({"role": "user", "content": msg.text})
    if model == 'deepseek':
        response = await get_deepseek_response(user_id)
    elif model == "gemini":
        response = await get_gemini_response(user_id)
    else:
        response = "Выберите модель"
    user_context[user_id].append({"role": "assistant", "content": response})
    
    formatted_response = markdown.text(
        markdown.markdown_decoration.quote(
            response
        )
    )
    
    await msg.answer(formatted_response, reply_markup=stop_context)