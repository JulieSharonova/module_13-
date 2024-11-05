from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKENURBAN

api = TOKENURBAN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['/start'])
async def start(message):
    await message.answer('Привет! Я - бот помогающий твоему здоровью.', reply_markup=kb)


# @dp.message_handler()
# async def all_messages(message):
#     await message.answer('Введите команду /start, чтобы начать общение.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)

kb2 = InlineKeyboardMarkup()
but = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(but)
kb2.add(but2)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я - бот, рассчитывающий норму ккал по упрощенной формуле Миффлина-Сан Жеора.')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(f'Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    try:
        age = float(data['age'])
        growth = float(data['growth'])
        weight = float(data['weight'])
    except:
        await message.answer('Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return

    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {calories} ккал в день')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)