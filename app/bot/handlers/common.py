import asyncio, os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.common.repository.user_repository import UserRepository
from app.bot.keyboards import reply as rp
from app.bot.keyboards import inline as inl
from app.bot.common.text import text_about
from app.core.config import settings

common_router = Router()

@common_router.message(CommandStart(), StateFilter('*'))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await UserRepository.add(telegram_id=message.from_user.id, username=message.from_user.username)
    
    await message.answer_sticker(sticker="CAACAgIAAxkBAAOfZdtFktnm8G3UklmN5pZy7Yv1VpoAAtQMAAJ6i6BIni8iJJQzvJs0BA")
    await asyncio.sleep(1)
    await message.answer(f'Добро пожаловать, {message.from_user.full_name}!')
    if message.from_user.id in (settings.WRITER_ID, settings.ADMIN_ID):
        await message.answer(f'Я бот проекта <b>SIMPLE PHYSICS!</b>', parse_mode='HTML', reply_markup=rp.start_admin)
        await message.answer("Вы вошли как администратор!")
    else:
        await message.answer(f'Я бот проекта <b>SIMPLE PHYSICS!</b>', parse_mode='HTML', reply_markup=rp.start)
        
        
@common_router.message(F.text == "🤖Информация о боте", StateFilter('*'))
async def about_bot(message: Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAPUZdtMgrKCGWN1hGG7sC9lB1Ob2nIAAhsTAAJakthIYwemdV7Qq5c0BA")
    await asyncio.sleep(1)
    await message.answer(text_about, reply_markup=inl.web_app_info)
