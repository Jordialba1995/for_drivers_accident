from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state

from keyboards import make_row_keyboard

hello_message = 'чат бот для водителя\nНажмите далее для отображения инструкции и списка документов'

# items for keyboards
next_step = ['Далее']
y_n = ['Да', 'Нет']

# texts
instruction = 'ИНСТРУКЦИЯ'

router = Router()


class driver_info(StatesGroup):
    # 0
    zero_state = State()
    # otpravlyaem instr po dokam i foto
    send_instruction = State()
    # zapisivaem fio
    driver_name = State()
    # zagruzka foto 1
    repeat_fio = State()
    save_fio = State()
    upload_photo_2 = State()


# nachalnoe vhojdenie
@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(driver_info.zero_state)
    await message.answer(
        text=hello_message,
        reply_markup=ReplyKeyboardRemove()
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(driver_info.send_instruction)

@router.message(StateFilter(None), Command(commands=['cancel']))
@router.message(default_state, F.text.lower() == 'отмена')
async def cmd_cancel_no_state(messsage:Message, state: FSMContext):
    await state.set_state({})
    await messsage.answer(
        text='Нечего менять',
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )

# send instruction
@router.message(
    driver_info.send_instruction,
    F.text.in_(next_step))
async def send_instruction(message: Message, state: FSMContext):
    await message.answer(text=instruction)
    await message.answer(
        text='Введите Фамилию, Имя, Отчество ЧЕРЕЗ ПРОБЕЛ\nПример: Иванов Иван Иванович', parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(driver_info.driver_name)


# zapisivaem fio
@router.message(driver_info.driver_name
                # F.text.in_ #                                ????
                )
async def vvod_fio(message: Message, state: FSMContext):
    await message.answer(
        text=f'Ваше ФИО: {message.text.title()}',
        reply_markup=make_row_keyboard(y_n))
    # await state.set_state(driver_info.repeat_fio)
    await state.set_state(driver_info.repeat_fio)


@router.message(driver_info.repeat_fio,
                F.text.in_(y_n[1]))
async def fio_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text='Введите ФИО еще раз',
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(driver_info.driver_name)


@router.message(driver_info.save_fio,
                F.text.in_(y_n[0]))
async def upload_1(message: Message, state: FSMContext):
    await state.update_data(driver_fio=message.text.title())
    await message.answer(
        text='teper zagruzite foto 2'
    )
    await state.set_state((driver_info.upload_photo_2))




