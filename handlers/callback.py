from aiogram import Bot
from aiogram.types import CallbackQuery, InputFile
from handlers.stat import *
from utility.callbackdata import DocInfo, ColInfo, StatInfo
from utility.user_data import  collect_doc_info 
from aiogram.fsm.context import FSMContext
import html
from keyboards.inline import * 
import io

async def chose_file_from_storage(call: CallbackQuery, callback_data: DocInfo):
    
    
    collect_doc_info(callback_data.name, callback_data.action)
    if DocInfo.action == 'select':
        await call.message.answer(f"You've chosen file: <b>{DocInfo.name}</b>", 
                                  parse_mode='html', 
                                  reply_markup=get_inline_doc_keyboard())

    elif DocInfo.action == 'delete':
        file_path = f"{UserData.folder_path}/{DocInfo.name}"
        os.remove(file_path)
        UserData.file_count -= 1
        print(UserData.file_count == 0)
        if UserData.file_count == 0:
            await call.message.answer(f"""File <b>{DocInfo.name}</b> has been deleted.\n There're no any file to analyse. \n Load new:""",
                                  parse_mode= 'html',
                                  reply_markup=get_file_menu())
        else:
            await call.message.answer(f"""File <b>{DocInfo.name}</b> has been deleted.\n Choose any file to analyse: \n Load new:""",
                                  parse_mode= 'html',
                                  reply_markup=get_file_menu())
            await call.message.answer(f"""Or load new:""",
                                  parse_mode= 'html',
                                  reply_markup=get_file_menu())
            


async def select_doc_option(call: CallbackQuery, callback_data: DocInfo):
    DocInfo.name = callback_data.name
    print(callback_data.choice)
    if callback_data.choice == "show_col":
        await call.message.answer(f"<b>Columns of data in file {DocInfo.name} are:</b>", 
                                  parse_mode="html", reply_markup=get_inline_doc_columns_keyboard())
        
    elif callback_data.choice == "descr":
        await call.message.answer(f"<b>Description of data {DocInfo.name}:</b>", 
                                  parse_mode="html")
        image_data = description_print(DocInfo.name)
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{DocInfo.name}_Table.png")
        await call.message.answer_photo(buffered_input_file)
        
        """
        await call.message.answer(f"{description_print(DocInfo.name)}")
        """
         
    elif callback_data.choice == "doc_info":
        await call.message.answer(f"<b>Data information from file {DocInfo.name}:</b>", 
                                  parse_mode="html")
        await call.message.answer(f"Info: \n {html.escape(info_print(DocInfo.name))}")
        #await call.answer()

    else:
        await call.answer(f"Houston, we have a problem!")

async def select_col_option(call: CallbackQuery, callback_data: ColInfo):
    if (callback_data.type == 'float64') | (callback_data.type == 'int64'):
        await call.message.answer(f"<b>You've chosen <b>{callback_data.col_name}</b>. Data of this column is numerical, You have access to these options:</b>", 
                                  parse_mode='html', 
                                  reply_markup=get_inline_doc_column_num_keyboard())
        
    elif callback_data.type == 'object':
        await call.message.answer(f"<b>You've chosen <b>{callback_data.col_name}</b>. Data of this column is text or categories, You have access to these options:</b>", 
                                  parse_mode='html', 
                                  reply_markup=get_inline_doc_column_cat_keyboard())
    else:
        await call.answer(f"Houston, we have a problem with new function!")
    ColInfo.col_name = callback_data.col_name
    
async def choice_col_option(call: CallbackQuery, callback_data: StatInfo):
    
    #Quantitative Variables:
    
    if callback_data.stat_option == 'mean':
        await call.message.answer(f"<b>Mean</b> of variable {ColInfo.col_name} is equal <b>{round(mean_count(DocInfo.name, ColInfo.col_name), 4)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'median':
        await call.message.answer(f"<b>Median</b> of variable {ColInfo.col_name} is equal <b>{round(median_count(DocInfo.name, ColInfo.col_name), 4)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'mode':
        await call.message.answer(f"<b>Mode</b> of variable {ColInfo.col_name} is \n <b>{mode_count(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_trmean':
        # Сделать возможность выбора процентов
        await call.message.answer(f"<b>Trimmed Mean 10%</b> of variable {ColInfo.col_name} is equal <b>{round(trim_mean_10_count(DocInfo.name, ColInfo.col_name), 4)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_range':
        await call.message.answer(f"<b>Range</b> of variable {ColInfo.col_name} is equal <b>{range_count(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_iqrange':
        await call.message.answer(f"<b>Interquartile Range</b> of variable {ColInfo.col_name} is equal <b>{iqrange_count(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_var':
        await call.message.answer(f"<b>Variance</b> of variable {ColInfo.col_name} is equal <b>{round(var_count(DocInfo.name, ColInfo.col_name), 4)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_stdev':
        await call.message.answer(f"<b>Standard Deviation</b> of variable {ColInfo.col_name} is equal <b>{round(std_dev_count(DocInfo.name, ColInfo.col_name), 4)}</b>", parse_mode="html")
    elif callback_data.stat_option == 'col_mad':
        await call.message.answer(f"<b>Mean Absolute Deviation</b> of variable {ColInfo.col_name} is equal <b>{mad_count(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")    
    elif callback_data.stat_option == 'col_all':
        await call.message.answer(f"""<b>Descriptive Statistics </b> of {ColInfo.col_name}: \n         
    \t Mean:                                         {round(mean_count(DocInfo.name, ColInfo.col_name), 4)}
    \t Median:                                    {round(median_count(DocInfo.name, ColInfo.col_name), 4)}
    \t Mode:                                        {mode_count(DocInfo.name, ColInfo.col_name)}
    \t Trimmed Mean:                      {round(trim_mean_10_count(DocInfo.name, ColInfo.col_name), 4)}
    \t Range:                                        {range_count(DocInfo.name, ColInfo.col_name)}
    \t Interquartile Range:              {iqrange_count(DocInfo.name, ColInfo.col_name)}
    \t Variance:                                   {round(var_count(DocInfo.name, ColInfo.col_name), 4)}   
    \t Standard Deviation:              {round(std_dev_count(DocInfo.name, ColInfo.col_name), 4)}
    \t Mean Absolute Deviation:   {mad_count(DocInfo.name, ColInfo.col_name)}""", parse_mode="HTML", reply_markup=get_return_keyboard())
        
        #Visualisation Variable:
    elif callback_data.stat_option == 'dis_plot_num':
        image_data = dis_plot_num(DocInfo.name, ColInfo.col_name)
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_pie_chart.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    elif callback_data.stat_option =='box_plot_num':
        image_data = box_plot(DocInfo.name, ColInfo.col_name)    
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_box_plot.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    elif callback_data.stat_option =='strip_plot_num':
        image_data = strip_plot(DocInfo.name, ColInfo.col_name)    
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_strip_plot.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    elif callback_data.stat_option =='swarm_plot_num':
        image_data = swarm_plot(DocInfo.name, ColInfo.col_name)    
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_swarm_plot.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    elif callback_data.stat_option =='violin_plot_num':
        image_data = violin_plot(DocInfo.name, ColInfo.col_name)    
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_violin_plot.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    #Categorical Variables:
    elif callback_data.stat_option == 'col_count_unique':
        await call.message.answer(f"<b>Unique Count</b> of variable {ColInfo.col_name} is equal <b>{unique_count(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")    
        
    elif callback_data.stat_option == 'col_unique':
        await call.message.answer(f"<b>Uniques</b> of variable {ColInfo.col_name} is equal <b>{unique(DocInfo.name, ColInfo.col_name)}</b>", parse_mode="html")        
    elif callback_data.stat_option == 'col_valcount_norm':
        await call.message.answer(f"<b>Value Counts (%)</b> of variable <b>{ColInfo.col_name}</b>:", parse_mode="html")
        await call.message.answer(f"{round(value_counts_count(DocInfo.name, ColInfo.col_name), 2)}")
        #Visualisation Categorical:
    elif callback_data.stat_option == 'col_pie_chart':
        image_data = pie_chart(DocInfo.name, ColInfo.col_name)
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_pie_chart.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    elif callback_data.stat_option =='col_count_plot':
        image_data = count_plot(DocInfo.name, ColInfo.col_name)    
        image_binary = base64.b64decode(image_data)
        buffered_input_file = BufferedInputFile(image_binary, filename=f"{ColInfo.col_name}_pie_chart.png")
        await call.message.answer_photo(buffered_input_file, reply_markup=get_return_keyboard())
    else:
        await call.message.answer(f"Other options are not realized, but flying in the creator's mind and plans ;)", reply_markup=get_return_keyboard())
        