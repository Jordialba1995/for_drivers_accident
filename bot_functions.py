import os

#  создает новую папку по указанному пути, при условии, что все указанные промежуточные (вложенные) директории уже существуют.
def make_dir_my(driver_fio):
    cwd = r'D:\test'
    path = os.path.join(cwd, driver_fio)
    isdir_my = os.path.isdir(path)
    if isdir_my is False:
        return os.mkdir(path)
    # возвращает путь до каталога уже существующего
    if isdir_my is True:
        return path

def validate_fio(string_fio: str):
    fio_regex = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', string_fio)
    if len(fio_regex) > 0:
        return True
    else:
        return False