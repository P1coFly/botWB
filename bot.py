from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DataBase
from config import TOKEN, correct_password


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
db = DataBase('userdb.db')

password=State()




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
    print(msg)
    if not db.user_exists(msg.from_user.id):
        if msg.text == correct_password:
            db.add_user(msg.from_user.id)
            await bot.send_message(msg.from_user.id,"Привет!\nНапиши мне адрес!")
            await state.finish()
        else:
            await bot.send_message(msg.from_user.id,"Неверный пароль")
    else:
        await bot.send_message(msg.from_user.id, msg.text)


    

if __name__ == '__main__':
    print("Start work")
    executor.start_polling(dp)