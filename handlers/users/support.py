from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from keyboards.inline.support import support_keyboard, support_callback


@dp.message_handler(Command('ask_question'))
async def ask_question(message: types.Message):
    text = 'Got questions? You can ask them by clicking the button below!'
    keyboard = await support_keyboard(messages='one')
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='one'))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get('user_id'))

    await call.message.answer('Please, try to explain information in 1 message.')
    await state.set_state('wait_for_support_message')
    await state.update_data(second_id=user_id)


@dp.message_handler(state='wait_for_support_message', content_types=types.ContentTypes.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get('second_id')

    await bot.send_message(second_id, 'User has problems and wrote to you. Please answer!')
    keyboard = await support_keyboard(messages='one', user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer('We have sent your message, now you have to wait.')
    await state.reset_state()
