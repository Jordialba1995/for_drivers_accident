from aiogram.fsm.context import FSMContext
# from kb import make_row_keyboard, make_sklad_keyboard
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State

from keyboards import make_row_keyboard


hello_message = 'чат бот для водителя\nНажмите далее для отображения инструкции и списка документов'

# items for keyboards
begin_button = ['Далее']



router = Router()

class CheckExist(StatesGroup):
    # 0
    zero_state = State()
    choosing_some = State()
    # 1
    # otpravlyaem instr po dokam i foto
    send_instruction = State()


# nachalnoe vhojdenie
@router.message(StateFilter(None), Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(CheckExist.zero_state)
    await message.answer(
        text=hello_message, parse_mode='HTML',
        reply_markup= make_row_keyboard(begin_button)

    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CheckExist.choosing_some)








