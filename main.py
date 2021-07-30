import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from genuis import azlyrics

logging.basicConfig(level=logging.INFO)

API_TOKEN ='1924710903:AAFDQUeR8INuOA_VjNHro8CsHiZspejuGPU'


bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    singer = State()  # Will be represented in storage as 'Form:name'
    song = State()  # Will be represented in storage as 'Form:age'

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    # Set state
    await Form.singer.set()

    await message.reply("Tell me the name of the singer")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.singer)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['singer'] = message.text

    await Form.next()
    await message.reply("Now tell me the name of the song")

@dp.message_handler(state=Form.song)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(song=message.text)

    async with state.proxy() as data:
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(md.bold(f'{data["song"].title()} by {data["singer"].title()}'), md.text(azlyrics(artist=data['singer'], song=data['song']))),               
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Click /start to search for lyrics'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    await state.finish()

   


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)