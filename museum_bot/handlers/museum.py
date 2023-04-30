from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard

router = Router()

ENTRY_MESSAGE = "Добро пожаловать!\n" \
                "Пожалуйста, сдайте верхнюю одежду в гардероб!"
EXIT_MESSAGE = "Всего доброго!\n" \
               "Не забудьте забрать верхнюю одежду в гардеробе!"
MESSAGE = "В данном зале представлено "

DESCRIPTIONS = ['искусство Ренессанса',
                'богатство и разнообразие',
                'историческое наследие',
                'полотно Айвазовского']


class MuseumObject(StatesGroup):
    zero_point = State()
    entry_point = State()
    second_point = State()
    third_point = State()
    exit_point = State()

    translating_text = State()


@router.message(MuseumObject.zero_point)
async def cmd_museum(message: Message, state: FSMContext):
    await message.answer(
        text=f"{ENTRY_MESSAGE}\n"
             f"Ниже представлены возможные комнаты:",
        reply_markup=make_row_keyboard(['Комната 2\n'
                                        f'{DESCRIPTIONS[1]}'])
    )
    # Устанавливаем пользователю состояние "вошел в музей"
    await state.set_state(MuseumObject.entry_point)


@router.message(MuseumObject.entry_point)
async def second_room(message: Message, state: FSMContext):
    await message.answer(
        text=f"Ниже представлены возможные комнаты:",
        reply_markup=make_row_keyboard(['Комната 3\n'
                                        f'{DESCRIPTIONS[2]}'])
    )
    # Устанавливаем пользователю состояние "вошел во вторую комнату"
    await state.set_state(MuseumObject.second_point)


@router.message(MuseumObject.second_point)
async def third_room(message: Message, state: FSMContext):
    await message.answer(
        text=f"Ниже представлены возможные комнаты:",
        reply_markup=make_row_keyboard(['Комната 1\n'
                                        f'{DESCRIPTIONS[0]}',
                                        'Комната 4\n'
                                        f'{DESCRIPTIONS[3]}'])
    )
    await state.set_state(MuseumObject.third_point)


@router.message(MuseumObject.third_point)
async def fourth_room(message: Message, state: FSMContext):
    if message.text.split('\n')[-1] in DESCRIPTIONS[0]:
        await state.set_state(MuseumObject.zero_point)
    else:
        await message.answer(
            text=f"Ниже представлены возможные комнаты:",
            reply_markup=make_row_keyboard(['Комната 1\n'
                                            f'{DESCRIPTIONS[0]}', 'Выход'])
        )
        await state.set_state(MuseumObject.exit_point)


@router.message(MuseumObject.exit_point)
async def cmd_exit(message: Message, state: FSMContext):
    if message.text.split('\n')[-1] in DESCRIPTIONS[0]:
        await state.set_state(MuseumObject.zero_point)
    else:
        await message.answer(
            text=f"{EXIT_MESSAGE}",
            reply_markup=ReplyKeyboardRemove()
        )
        # Устанавливаем пользователю состояние "ушел из музея"
        await state.clear()
