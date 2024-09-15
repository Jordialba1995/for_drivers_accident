from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from _datetime import *

from keyboards import make_row_keyboard
from bot_functions import make_dir_my, validate_fio, comments

hello_message = 'Здравствуйте вас приветствует "Бот помощник при ДТП".\nДанный бот помогает зафиксировать повреждения автотранспортного средства.\nПо вопросам работы бота прошу обращаться:\n' + \
    '-Малышев Валерий Петрович\n-Невзоров Андрей Дмитриевич\n-Федоров Владимир Александрович.\n' + \
        'Данный продукт разработан ООО "ГСП-ЦЕНТР".'

bye_message = 'После отправки материалов в "Бот помощник при ДТП" прошу обратиться к специалисту отвечающему за страховой случай' + \
    ' в вашем подразделении и оповестить его о произошедшей ситуации.\n' + \
        'Номер телефона специалиста: (60) 23-51;\ne-mail: Nevzorovad@gsp-center.ru'

# items for keyboards
next_step = ['Далее']
y_n = ['Да', 'Нет']

# texts
instruction = 'ИНСТРУКЦИЯ'

router = Router()

# file_dir = "C:\\Users\\Dmitry\\Downloads\\bot_photos\\"
# file_dir = r'D:\test'


class Driver_Info(StatesGroup):
    # 0
    zero_state = State()
    # otpravlyaem instr po dokam i foto
    send_instruction = State()
    # zapisivaem fio
    driver_name = State()
    # zagruzka foto 1
    repeat_fio = State()
    save_fio = State()
    # photo 1
    photo_1 = State()
    uploading_photo_1 = State()
    uploaded_photo_1 = State()
    com_1 = State()
    # photo 2
    photo_2 = State()
    uploading_photo_2 = State()
    uploaded_photo_2 = State()
    com_2 = State()
    # photo 3
    photo_3 = State()
    uploading_photo_3 = State()
    uploaded_photo_3 = State()
    com_3 = State()
    # photo 4
    photo_4 = State()
    uploading_photo_4 = State()
    uploaded_photo_4 = State()
    com_4 = State()
    # loading end
    the_end = State()


# nachalnoe vhojdenie
@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Driver_Info.zero_state)
    await message.answer(
        text=hello_message + '\n\nНажмите кнопку "Далее" для продолжения работы  с ботом.',
        reply_markup=make_row_keyboard(['Далее'])
    )
    await state.set_state(Driver_Info.send_instruction)
    

# send instruction
@router.message(
    Driver_Info.send_instruction,
    F.text == next_step[0])
async def send_instruction(message: Message, state: FSMContext):
    await message.answer(text=instruction)
    await message.answer(
        text='Введите Фамилию, Имя, Отчество ЧЕРЕЗ ПРОБЕЛ\nПример: Иванов Иван Иванович', 
        parse_mode='HTML', 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Driver_Info.driver_name)


# zapisivaem fio
@router.message(Driver_Info.driver_name)
async def vvod_fio(message: Message, state: FSMContext):
    
    if validate_fio(message.text):    
        # fio zapisivaem
        await state.update_data(fio=message.text.title())
        await message.answer(
            text=f'Ваше ФИО: {message.text.title()}',
            reply_markup=make_row_keyboard(y_n))
        await state.set_state(Driver_Info.repeat_fio)
    else:
        await message.answer(
            text='Введите КОРРЕКТНУЮ Фамилию, Имя, Отчество через пробел\nПример: Иванов Иван Иванович', parse_mode='HTML')
        await state.set_state(Driver_Info.driver_name)


# failed FIO
@router.message(Driver_Info.repeat_fio,
                F.text == y_n[1])
async def fio_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text='Введите ФИО еще раз',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Driver_Info.driver_name)


# successed FIO
@router.message(Driver_Info.repeat_fio,
                F.text == y_n[0])
async def fio_correctly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    path = make_dir_my(user_data['fio'])  # только вызов функции ???
    await state.update_data(path_to_f=path)

    await message.answer(
        text='Теперь приложите фото ДТП с 4 разных сторон.\nПожалуйста, загружайте фото поэтапно, следуя кнопкам.\nСначала нажмите кнопку, потом приложите фото.',
        reply_markup=make_row_keyboard(['Фото 1', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_1)


# check for text
@router.message(Driver_Info.repeat_fio)
async def repeat_fio_check_text(message: Message):
    await message.answer(
        text='Вы попытались ввести текст, сначала нажмите кнопку.',
        reply_markup=make_row_keyboard(['Фото 1', 'Отмена'])
        )


# photo1 cancel FIO
@router.message(Driver_Info.photo_1,
                F.text == 'Отмена')
async def photo_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# succed photo1
@router.message(Driver_Info.photo_1,
                F.text == 'Фото 1')
async def photo1_wait(message: Message, state: FSMContext):
    await message.answer(
        text='Теперь загрузите Фото 1.',
        reply_markup=make_row_keyboard(['Отмена'])
    )
    await state.set_state(Driver_Info.uploaded_photo_1)


# hz photo1
@router.message(Driver_Info.photo_1)
async def photo1_incorrect(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"К сожалению, я Вас не понял.\nСначала нажмите кнопку, потом приложите фото.",
        reply_markup=make_row_keyboard(['Фото 1', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_1)


# cancel uploaded photo1
@router.message(Driver_Info.uploaded_photo_1,
                F.text == 'Отмена')
async def photo1_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# photo 1 OK
@router.message(Driver_Info.uploaded_photo_1,
                F.content_type == 'photo')
async def photo1_loaded_correctly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    photo_filename = user_data['path_to_f'] + '\\' + datetime.today().strftime('%d%m%Y_%H%M%S') + '_photo1.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=photo_filename)
    await state.update_data(photo1_filename=photo_filename)
    await message.answer(
        text='Вы загрузили Фото 1.\nТеперь введите комментарий к фото.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Driver_Info.com_1)


# check for text photo 1
@router.message(Driver_Info.uploaded_photo_1)
async def photo1_check_text(message: Message):
    await message.answer(
        text='Загрузите фото 1, вы попытались ввести текст',
        reply_markup=make_row_keyboard(['Отмена'])
        )


# com 1
@router.message(Driver_Info.com_1,
                F.text)
async def com_1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    comments(user_data['fio'], user_data['photo1_filename'], message.text)
    await message.answer(
        text='Вы загрузили комментарий 1.\nТеперь загрузите Фото 2.',
        reply_markup=make_row_keyboard(['Фото 2', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_2)


# cancel photo2 before just uploading
@router.message(Driver_Info.photo_2,
                F.text == 'Отмена')
async def photo1_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# photo 2
@router.message(Driver_Info.photo_2,
                F.text == 'Фото 2')
async def photo2_privet(message: Message, state: FSMContext):
    await message.answer(
        text='Отправьте Фото 2.',
        reply_markup=make_row_keyboard(['Отмена'])
    )
    await state.set_state(Driver_Info.uploading_photo_2)


# photo 2 cancel
@router.message(Driver_Info.uploading_photo_2,
                F.text == 'Отмена')
async def photo2_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# hz photo2
@router.message(Driver_Info.photo_2)
async def photo2_incorrect(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"К сожалению, я Вас не понял.\nСначала нажмите кнопку, потом приложите фото.",
        reply_markup=make_row_keyboard(['Фото 2', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_2)


# check for text photo 2
@router.message(Driver_Info.uploading_photo_2,
                F.text)
async def photo2_check_text(message: Message, state: FSMContext):
    await message.answer(
        text='Загрузите фото 2, вы попытались ввести текст',
        reply_markup=make_row_keyboard(['Отмена'])
        )
    await state.set_state(Driver_Info.uploading_photo_2)


@router.message(Driver_Info.uploading_photo_2,
                F.content_type == 'photo')
async def photo2_loaded_correctly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    photo_filename = user_data['path_to_f'] + datetime.today().strftime('%d%m%Y_%H%M%S') + '_photo2.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=photo_filename)
    await state.update_data(photo2_filename=photo_filename)
    await message.answer(
        text='Вы загрузили Фото 2.\nвведите комментарий к фото.',
        reply_markup=ReplyKeyboardRemove()

        # reply_markup=make_row_keyboard(['Фото 3', 'Отмена'])
    )
    await state.set_state(Driver_Info.com_2)


# com 2
@router.message(Driver_Info.com_2,
                F.text)
async def com_2(message: Message, state: FSMContext):
    user_data = await state.get_data()
    comments(user_data['fio'], user_data['photo2_filename'], message.text)
    await message.answer(
        text='Вы загрузили комментарий 2.\nТеперь загрузите Фото 3.',
        reply_markup=make_row_keyboard(['Фото 3', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_3)


# photo 2 loaded cancel
@router.message(Driver_Info.photo_3,
                F.text == 'Отмена')
async def photo2_loaded_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# photo 3 OK
@router.message(Driver_Info.photo_3,
                F.text == 'Фото 3')
async def photo3_privet(message: Message, state: FSMContext):
    await message.answer(
        text='Отправьте Фото 3.',
        reply_markup=make_row_keyboard(['Отмена'])
    )
    await state.set_state(Driver_Info.uploading_photo_3)


# hz photo3
@router.message(Driver_Info.photo_3)
async def photo3_incorrect(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"К сожалению, я Вас не понял.\nСначала нажмите кнопку, потом приложите фото.",
        reply_markup=make_row_keyboard(['Фото 3', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_3)


# check for text photo 3
@router.message(Driver_Info.uploading_photo_3,
                F.text)
async def photo3_check_text(message: Message, state: FSMContext):
    await message.answer(
        text='Загрузите фото 3, вы попытались ввести текст',
        reply_markup=make_row_keyboard(['Отмена'])
        )
    await state.set_state(Driver_Info.uploading_photo_3)


# photo 3 OK
@router.message(Driver_Info.uploading_photo_3,
                F.content_type == 'photo')
async def photo3_loaded_correctly(message: Message, state: FSMContext):
    
    user_data = await state.get_data()
    photo_filename = user_data['path_to_f'] + datetime.today().strftime('%d%m%Y_%H%M%S') + '_photo3.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=photo_filename)
    await state.update_data(photo3_filename=photo_filename)
    await message.answer(
        text='Вы загрузили Фото 3.\nТеперь введите комментарий к фото.',
        reply_markup=ReplyKeyboardRemove()
        # reply_markup=make_row_keyboard(['Фото 4', 'Отмена'])
    )
    await state.set_state(Driver_Info.com_3)


# com 3
@router.message(Driver_Info.com_3,
                F.text)
async def com_3(message: Message, state: FSMContext):
    user_data = await state.get_data()
    comments(user_data['fio'], user_data['photo3_filename'], message.text)
    await message.answer(
        text='Вы загрузили комментарий 3.\nТеперь загрузите Фото 4.',
        reply_markup=make_row_keyboard(['Фото 4', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_4)


# photo 3 loaded cancel
@router.message(Driver_Info.photo_4,
                F.text == 'Отмена')
async def photo3_loaded_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# photo 3 OK
@router.message(Driver_Info.photo_4,
                F.text == 'Фото 4')
async def photo4_privet(message: Message, state: FSMContext):
    await message.answer(
        text='Отправьте Фото 4.',
        reply_markup=make_row_keyboard(['Отмена'])
    )
    await state.set_state(Driver_Info.uploading_photo_4)


# hz photo4
@router.message(Driver_Info.photo_4)
async def photo2_incorrect(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"К сожалению, я Вас не понял.\nСначала нажмите кнопку, потом приложите фото.",
        reply_markup=make_row_keyboard(['Фото 4', 'Отмена'])
    )
    await state.set_state(Driver_Info.photo_4)


# photo 4 cancel
@router.message(Driver_Info.uploading_photo_4,
                F.text == 'Отмена')
async def photo4_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# check for text photo 4
@router.message(Driver_Info.uploading_photo_4,
                F.text)
async def photo4_check_text(message: Message, state: FSMContext):
    await message.answer(
        text='Загрузите фото 4, вы попытались ввести текст',
        reply_markup=make_row_keyboard(['Отмена'])
        )
    await state.set_state(Driver_Info.uploading_photo_4)


# photo 4 OK
@router.message(Driver_Info.uploading_photo_4,
                F.content_type == 'photo')
async def photo4_loaded_correctly(message: Message, state: FSMContext):
    
    user_data = await state.get_data()
    photo_filename = user_data['path_to_f'] + datetime.today().strftime('%d%m%Y_%H%M%S') + '_photo4.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=photo_filename)
    await state.update_data(photo4_filename=photo_filename)
    await message.answer(
        text='Вы загрузили Фото 4.\nТеперь введите комментарий к фото.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Driver_Info.com_4)


# com 4
@router.message(Driver_Info.com_4,
                F.text)
async def com_4(message: Message, state: FSMContext):
    user_data = await state.get_data()
    comments(user_data['fio'], user_data['photo1_filename'], message.text)
    await message.answer(
        text='Вы загрузили комментарий 4.\nЗагрузка фото завершена',
        reply_markup=make_row_keyboard(['В начало'])
    )
    await state.set_state(Driver_Info.the_end)


# photo 4 cancel
@router.message(Driver_Info.photo_3,
                F.text == 'Отмена')
async def photo4_loaded_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Загрузка фотографий отменена.\nПожалуйста подтвердите Ваше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)


# photo 4 OK
@router.message(Driver_Info.the_end,
                F.text == 'В начало')
async def photo4_loaded_correctly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"{bye_message}\nВаше ФИО: {user_data['fio']}",
        reply_markup=make_row_keyboard(y_n)
    )
    await state.set_state(Driver_Info.repeat_fio)
