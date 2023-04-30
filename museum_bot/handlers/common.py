from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from WEB.Bots.Telegram.museum_bot.handlers.museum import MuseumObject

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Привет, я бот-экскурсовод.\n"
             "По запросу /museum вы можете начать свое путешествие в музее.\n",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MuseumObject.zero_point)
