import os
import re
import csv

#  создает новую папку по указанному пути, при условии, что все указанные промежуточные (вложенные) директории уже существуют.
def make_dir_my(driver_fio):
    # cwd need to change after finished
    cwd = r'C:\\Users\\Dmitry\\Downloads\\bot_photos\\'
    path = os.path.join(cwd, driver_fio)
    isdir_my = os.path.isdir(path)
    if isdir_my is False:
        os.mkdir(path)
        return path + '\\'
    # возвращает путь до каталога уже существующего
    if isdir_my is True:
        return path + '\\'


def validate_fio(string_fio: str):
    fio_regex = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', string_fio)
    if len(fio_regex) > 0:
        return True
    else:
        return False


def comments(*args):
    args = [list(args)]
    with open('com.csv', 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(args)
        #print(args)




