from aiogram import Bot, F, exceptions
from aiogram.types import Message, CallbackQuery
from settings import settings
from keyboards.reply import get_reply_keyboard 
from keyboards.inline import get_inline_doc_keyboard, get_file_menu
from utility.callbackdata import DocInfo, UserData
from utility.user_data import collect_general_data 
import os


# Command Maintenance:
async def get_start(message: Message, bot: Bot):    #Receiving messages from the bot
    #Starting work, loading the primary menu:
    collect_general_data(message.from_user.id, message.from_user.first_name)
    
    if message.from_user.id == settings.bots.admin_id:
        await bot.send_message(UserData.id, f"<b>Greetings, my Lord!</b>", reply_markup= get_reply_keyboard())
    else:
        await message.answer(f"Hi, {UserData.name}. The first step is going to finish, see ya on github soon!.", reply_markup= get_reply_keyboard())
    
async def get_help_1(message: Message, bot:Bot):
    await message.answer(f"Load .csv file: ")

async def get_info(message: Message, bot: Bot):
    try:
        with open('handlers/texts/info.txt', 'r', encoding='utf-8') as info_data:
            info_text = info_data.read()

        await bot.send_message(message.from_user.id, info_text, parse_mode='HTML')
    except FileNotFoundError:
         await message.reply(f"File Not Found")

async def get_help(message: Message, bot: Bot):
    try:
        with open('handlers/texts/help.txt', 'r', encoding='utf-8') as help_data:
            help_text = help_data.read()
        await bot.send_message(message.from_user.id, help_text, parse_mode='HTML')
    except FileNotFoundError:
        await message.reply(f"File Not Found")    


#File import
        
async def get_file_req(message:Message, bot: Bot):
    
    await bot.send_message(message.from_user.id, f"<b>Upload file here: </b>")


#Data import service      

async def get_csv(message: Message, bot: Bot):

    try:
        file = await bot.get_file(message.document.file_id)

        if len(str(message.document.file_name)) > 30:
            file_name = f"{str(message.document.file_name)[:29]}_.csv"
        else:
            file_name = (message.document.file_name)

        collect_general_data(message.from_user.id, message.from_user.first_name)
        DocInfo.name = file_name
        

        if not os.path.exists(UserData.folder_path):
            os.makedirs(UserData.folder_path)
            await bot.download_file(file.file_path, f'{UserData.folder_path}/{file_name}')
            UserData.file_count += 1
        
        
        else:
            if os.path.exists(f"{UserData.folder_path}/{file_name}"):
                await bot.send_message(message.from_user.id, f"You already have this file. You have {UserData.file_count} files, check it!", parse_mode='html', reply_markup=get_file_menu())
            
            else:    
                await bot.download_file(file.file_path, f'{UserData.folder_path}/{file_name}')
                UserData.file_count += 1
                await message.answer(f"I've saved your file. Chose the option:", reply_markup=get_inline_doc_keyboard())
    except exceptions.TelegramBadRequest:
        await bot.send_message(message.from_user.id, f"This file is too big, load smaller file (max 18MB), pls ;)")
        

    
async def choose_file(message: Message, bot: Bot):
    
    collect_general_data(message.from_user.id, message.from_user.first_name)
    if not os.path.exists(f"data_bases/{message.from_user.id}"):
        await bot.send_message(UserData.id, f"<b>You can't select smth not exist</b> \n Firstly upload any .csv file.", parse_mode="html", reply_markup=get_file_menu())    
    else:
        try:
            UserData.folder_path = f"data_bases/{message.from_user.id}"
            await bot.send_message(UserData.id, f"Select File: ", reply_markup=get_file_menu())    
        except AttributeError:
            await bot.send_message(UserData.id, f"Press /Start")




async def get_hello(message: Message, bot: Bot):
    await message.answer(f'Hello too!')