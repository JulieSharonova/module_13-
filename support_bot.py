import asyncio
from mailbox import Message
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKENURBAN

api = TOKENURBAN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(Command('help'))
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



@dp.message_handler(CommandStart)
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


