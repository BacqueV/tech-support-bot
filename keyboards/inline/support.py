from aiogram.utils.callback_data import CallbackData

from data.config import support_agents
from random import shuffle, choice
from loader import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_callback = CallbackData('ask_question', 'messages', 'user_id', 'as_user')
cancel_support_callback = CallbackData('cancel_support', 'user_id')


async def check_support_available(agent_id):
    state = dp.current_state(chat=agent_id, user=agent_id)
    state_str = str(
        await state.get_state()
    )
    if state_str == 'in_support':
        return
    return agent_id


async def get_support_manager():
    shuffle(support_agents)
    for agent in support_agents:
        agent = await check_support_available(agent)
        if agent:
            return agent
    return


async def support_keyboard(messages, user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Answer user'
    else:
        contact_id = await get_support_manager()
        as_user = 'yes'
        if messages == 'many' and contact_id is None:
            return False
        elif messages == 'one' and contact_id is None:
            contact_id = choice(support_agents)

        if messages == 'one':
            text = 'Ask one question'
        else:
            text = 'Connect to operator'
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages,
                user_id=contact_id,
                as_user=as_user
            )
        )
    )

    if messages == 'many':
        keyboard.add(
            InlineKeyboardButton(
                text='Cancel session',
                callback_data=cancel_support_callback.new(user_id=contact_id)
            )
        )
    return keyboard


def cancel_support(user_id):
    btn_cancel_session = InlineKeyboardButton(
        'Cancel session',
        callback_data=cancel_support_callback.new(
            user_id=user_id
        )
    )
    markup_cancel_session = InlineKeyboardMarkup().add(btn_cancel_session)
    return markup_cancel_session
