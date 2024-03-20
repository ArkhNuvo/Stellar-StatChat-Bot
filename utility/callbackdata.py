from aiogram.filters.callback_data import CallbackData

class UserData:
    name: str
    id: str
    folder_path: str
    file_count = 0

class DocInfo(CallbackData, prefix='doc'):
    name: str
    choice: str
    action: str

class ColInfo(CallbackData, prefix='col'):
    col_name: str
    type: str

class StatInfo(CallbackData, prefix='stat'):
    stat_option: str

