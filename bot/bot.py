from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id,"Привет!\nНапиши мне адрес!")

    
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    

if __name__ == '__main__':
    print("Start work")
    executor.start_polling(dp)