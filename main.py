from aiogram import Bot, Dispatcher, F      #F -- для фильтрации контента.
import asyncio
from aiogram.types import Message, ContentType
from settings import settings
from handlers.basic import get_start, get_photo, get_hello, get_info, get_help, get_file_req, get_help_1, get_csv, choose_file
import logging
from aiogram.filters import Command, CommandStart
import os
from handlers.callback import select_doc_option, select_col_option, choice_col_option, chose_file_from_storage
from utility.callbackdata import DocInfo, ColInfo, StatInfo


#Administrative commands for bot status
async def start_bot(bot: Bot):                                                  #Sends a message that the bot is operational
    await bot.send_message(settings.bots.admin_id, text = "Bot is activaded, my Lord.")

async def stop_bot(bot:Bot):                                                    #Sends a message that the bot is disabled
    await bot.send_message(settings.bots.admin_id, text = "My Lord, The bot is disactivated.")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")    #For logging purposes
    bot = Bot(settings.bots.bot_token, parse_mode = "HTML") #Parse mode describes the format of the message; it is necessary for editing
    


    dp = Dispatcher() #An object responsible for receiving objects
    #Registration of handlers.
    dp.startup.register(start_bot)  
    dp.shutdown.register(stop_bot)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_hello, F.text.lower() == "hi")
    dp.message.register(get_start, Command(commands=['start', 'run'])) 
    dp.message.register(get_info, Command(commands = ['info']))
    dp.message.register(get_help, Command(commands = ['help']))
    dp.message.register(get_file_req, F.text == "Load File")
    dp.callback_query.register(get_file_req, F.data == 'load_file')
    dp.message.register(get_csv, F.document.file_name[-4:] == ".csv" )
    dp.callback_query.register(chose_file_from_storage, DocInfo.filter(F.action))
    dp.callback_query.register(select_doc_option, DocInfo.filter(F.choice))
    dp.callback_query.register(select_col_option, ColInfo.filter())
    dp.callback_query.register(select_col_option, F.data == 'show_col')
    dp.callback_query.register(choice_col_option, StatInfo.filter())
    dp.message.register(get_help_1, F.text == "Help")
    dp.message.register(choose_file, F.text == "Select File")
    dp.callback_query.register(choose_file, F.data == "back_to_files")
    dp.message.register(get_start, Command) 
    
    

    try:
        await dp.start_polling(bot)  #Starts receiving updates.
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try: #Handles the error that occurs when the bot is forcibly shut down
        asyncio.run(start())        #Starts the start function.
    except KeyboardInterrupt:
        pass

    