import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DataBase
from config import TOKEN, correct_password
import pathlib
import string 
from base64 import b64decode
from datetime import datetime
import asyncio


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
db = DataBase('userdb.db')

password=State()
data =[]
filename = ''

def get_df():
    try:
        global filename
        filename = f'{datetime.now().strftime("%m_%d_%Y")}.json'
        with open(filename, encoding='utf-8') as file:
            global data
            data=json.load(file)
    except:
        filename=''
        data=[]


@dp.message_handler(commands=['start'],state=None)
async def process_start_command(msg: types.Message):
    print(db.user_exists(msg.from_user.id))
    if not db.user_exists(msg.from_user.id):
        await password.set()
        await bot.send_message(msg.from_user.id,"Введите пароль")
    else:
        await bot.send_message(msg.from_user.id,"Привет!\nНапиши мне адрес!")


@dp.message_handler(state=password)
async def set_password(msg:types.Message,state:FSMContext):
    if not db.user_exists(msg.from_user.id):
        if msg.text == correct_password:
            db.add_user(msg.from_user.id)
            await bot.send_message(msg.from_user.id,"Привет!\nНапиши мне адрес!")
            await state.finish()
        else:
            await bot.send_message(msg.from_user.id,"Неверный пароль")
    else:
        global filename
        if filename != f'{datetime.now().strftime("%m_%d_%Y")}.json':
            try:
                get_df()
            except:
                await bot.send_message(msg.from_user.id,"Нет информации о заказах на сегодня\n")
        global data
        if data!=[]:
            print(filename.translate(str.maketrans('', '', string.punctuation)))
            print(set(msg.text.lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split()))
            for index, item in enumerate(data):
                if len(set(msg.text.lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split()) & set(item.get("Адрес").lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split())) == len(set(msg.text.lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split())):
                    print(set(item.get("Адрес").lower().replace('-',' ').translate(str.maketrans('', '', string.punctuation)).split()))
                    caption = f"Дата файла: {filename.split('.')[0].replace('_','.')}\n{item.get('Адрес')}\n{item.get('Получатель')}\n{item.get('Телефон')}\n{item.get('Код')}\n{item.get('Товар')}"
                    await bot.send_photo(chat_id=msg.from_user.id,photo=b64decode(item.get('qr')),caption=caption)
            

if __name__ == '__main__':
    print("Start work")
    executor.start_polling(dp)