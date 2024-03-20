from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utility.callbackdata import DocInfo, ColInfo, StatInfo, UserData
from handlers.basic import Message
from handlers.stat import columns_print
import os

def get_file_menu():
    
    try:
        list_of_files = os.listdir(f"data_bases/{UserData.id}")
        UserData.file_count = len(list_of_files)
    except:
        print("Press /Start.  ")
    
    keyboard_builder = InlineKeyboardBuilder()
    
    if UserData.file_count == 0:
            keyboard_builder.button(text=f'Upload File', callback_data = 'load_file')
            keyboard_builder.adjust(1)
            
    else:
        for file in list_of_files:
            keyboard_builder.button(text=f"{file}", callback_data=DocInfo(name=f"{file}", choice = '', action=f"select"))
            keyboard_builder.button(text=f"\U0000274C", callback_data= DocInfo(name=f"{file}", choice = '', action =f"delete"))
            keyboard_builder.adjust(2)
            
    return keyboard_builder.as_markup()


def get_inline_doc_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Show Columns', callback_data=DocInfo(name = f'{DocInfo.name}', choice='show_col', action=f""))
    keyboard_builder.button(text='Show Description', callback_data=DocInfo(name = f'{DocInfo.name}', choice='descr', action=f""))
    keyboard_builder.button(text='Show Info', callback_data=DocInfo(name = f'{DocInfo.name}', choice='doc_info', action=f""))

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def get_inline_doc_columns_keyboard():

    keyboard_builder = InlineKeyboardBuilder()
    
    for column_keys, column_values in columns_print(DocInfo.name).items():
        keyboard_builder.button(text=f"{column_keys} -- {column_values}", callback_data=ColInfo(col_name = f'{column_keys}', type=f"{column_values}"))
        
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_inline_doc_column_num_keyboard():

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text = 'Mean', callback_data=StatInfo(stat_option="mean"))
    keyboard_builder.button(text = 'Median', callback_data=StatInfo(stat_option="median"))
    keyboard_builder.button(text = 'Mode', callback_data=StatInfo(stat_option="mode"))
    keyboard_builder.button(text = 'Trimmed Mean 10%', callback_data=StatInfo(stat_option="col_trmean"))
    keyboard_builder.button(text = 'Range', callback_data=StatInfo(stat_option="col_range"))
    keyboard_builder.button(text = 'Interquartile Range', callback_data=StatInfo(stat_option="col_iqrange"))
    keyboard_builder.button(text = 'Variance', callback_data=StatInfo(stat_option="col_var"))
    keyboard_builder.button(text = 'Standard Deviation', callback_data=StatInfo(stat_option="col_stdev"))
    keyboard_builder.button(text = 'MAD', callback_data=StatInfo(stat_option="col_mad"))
    keyboard_builder.button(text= 'Show all Stats', callback_data=StatInfo(stat_option="col_all"))
    keyboard_builder.button(text='Histogram', callback_data=StatInfo(stat_option="dis_plot_num"))
    keyboard_builder.button(text='Box Plot', callback_data=StatInfo(stat_option="box_plot_num"))
    keyboard_builder.button(text='Strip Plot', callback_data=StatInfo(stat_option="strip_plot_num"))
    keyboard_builder.button(text='Swarm Plot', callback_data=StatInfo(stat_option="swarm_plot_num"))
    keyboard_builder.button(text='Violin Plot', callback_data=StatInfo(stat_option="violin_plot_num"))
    keyboard_builder.adjust(3,3,3,1,1,1,1,1,1)
    return keyboard_builder.as_markup()
    

def get_inline_doc_column_cat_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text = 'Count_unique', callback_data=StatInfo(stat_option="col_count_unique"))
    keyboard_builder.button(text = 'Unique', callback_data=StatInfo(stat_option="col_unique"))
    keyboard_builder.button(text = 'Value Counts, Normalized', callback_data=StatInfo(stat_option="col_valcount_norm"))
    keyboard_builder.button(text = 'Pie Chart', callback_data=StatInfo(stat_option="col_pie_chart"))
    keyboard_builder.button(text = 'Count Bar Plot', callback_data=StatInfo(stat_option="col_count_plot"))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_return_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text = 'Back to Columns', callback_data=DocInfo(name = f'{DocInfo.name}', choice='show_col', action=f""))
    keyboard_builder.button(text = 'Back to Files', callback_data='back_to_files')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()