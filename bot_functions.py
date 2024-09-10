import os

# sozdanie kataloga s fio
def make_dir_my(driver_fio):
    cwd = r'D:\test'
    path = os.path.join(cwd, driver_fio)
    return os.mkdir(path)



