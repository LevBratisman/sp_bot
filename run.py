from aiogram import Dispatcher, Bot, F
from aiogram.types import CallbackQuery
from aiogram.types.input_file import FSInputFile

from dotenv import find_dotenv, load_dotenv
import asyncio
import os
import logging

from app.handlers import router
from app import keyboards
from app.cmd_list import private

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

 
 


@dp.callback_query()
async def get_materials(callback_query: CallbackQuery):
    if callback_query.data == 'conspects':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Конспекты:', 
                               reply_markup=keyboards.conspect_list)
    elif callback_query.data == 'cards_theory':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Теория в карточках:',
                               reply_markup=keyboards.cards_list)
    elif callback_query.data == 'formulas':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Формулы для ЕГЭ', 
                               reply_markup=keyboards.formulas_list)
    elif callback_query.data == 'historical_references':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Исторические справки', 
                               reply_markup=keyboards.references_list)
    elif callback_query.data == 'back_to_materials':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Назад к учебным материалам:', 
                               reply_markup=keyboards.materials_list)
    elif callback_query.data == 'static':
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Конспект по статике:')
        await bot.send_document(callback_query.from_user.id, 
                                document='BQACAgIAAx0Cd9gAAe8AAwdl21P-AW-DjVEQfEgWfOpj6kWgowACXUkAAkF72UrmepebYkJD7zQE')
        await bot.send_message(chat_id=callback_query.from_user.id, 
                               text='Конспекты:', 
                               reply_markup=keyboards.conspect_list)
        


async def main():
    
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(private)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")
    