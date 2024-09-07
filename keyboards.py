from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# def begin_button():
#     kb = [
#         [
#             KeyboardButton(text="Далее")
#         ]
#     ]
#     return ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Нажмите далее"
#     )

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


sklads = ['Смидович п/о', 'Усть-Кут', 'Хабаровск', 'Новобурейский п/о', 'Ямал', 'Алдан', 'Сахалин',
          'Показать по всем складам']


def make_sklad_keyboard():
    row1 = [KeyboardButton(text=sklads[0]), KeyboardButton(text=sklads[1])]
    row2 = [KeyboardButton(text=sklads[2]), KeyboardButton(text=sklads[3])]
    row3 = [KeyboardButton(text=sklads[4]), KeyboardButton(text=sklads[5])]
    row4 = [KeyboardButton(text=sklads[6]), KeyboardButton(text=sklads[7])]
    row5 = [KeyboardButton(text='Вернуться')]
    return ReplyKeyboardMarkup(keyboard=[row1, row2, row3, row4, row5], resize_keyboard=True)

