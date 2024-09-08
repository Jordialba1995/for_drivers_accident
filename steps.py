from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state

from keyboards import make_row_keyboard


hello_message = 'чат бот для водителя\nНажмите далее для отображения инструкции и списка документов'

# items for keyboards
next_step = ['Далее']

# texts
instruction = 'ИНСТРУКЦИЯ'


router = Router()


class CheckExist(StatesGroup):
    # 0
    zero_state = State()
    # otpravlyaem instr po dokam i foto
    send_instruction = State()
    # zapisivaem fio
    driver_name = State()
    # zagruzka foto 1
    upload_photo_1 = State()


# nachalnoe vhojdenie
@router.message(StateFilter(None), Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(CheckExist.zero_state)
    await message.answer(
        text=hello_message, parse_mode='HTML',
        reply_markup=make_row_keyboard(next_step)

    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CheckExist.send_instruction)


# send instruction
@router.message(
    CheckExist.send_instruction,
    F.text.in_(next_step)
)
async def send_instruction(message: Message, state: FSMContext):
    await message.answer(text=instruction)
    await message.answer(
        text='Введите Фамилию, Имя, Отчество ЧЕРЕЗ ПРОБЕЛ\nПример: Иванов Иван Иванович', parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )
    if message.text is None:
        await message.answer(
            text='неправильное введено\n'
                 'vvedi zanovo fio')
    await state.set_state(CheckExist.driver_name)


# zapisivaem fio
@router.message(
    CheckExist.driver_name,
    F.text.in_(driver)
)
async def vvod_fio(message: Message, state: FSMContext):

    # await state.update_data(driver_name=message.text.title())
    await message.answer(
        text='Теперь загрузите фото одно за другим',
        reply_markup=make_row_keyboard(next_step)
    )
    await state.set_state(CheckExist.upload_photo_1)

# @router.message(CheckExist.driver_name)
# async def vvod_fio_incorrectly(message:Message):
#     await message.answer(
#         text='неправильное введено\n'
#             'vvedi zanovo fio',
#
#         reply_markup=make_row_keyboard(next_step)
#     )







