from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.keyboards import reply as rp
from app.bot.handlers.materials import get_categories_start
from app.bot.handlers.video import get_video_start
from app.bot.handlers.common import about_bot

from app.core.config import settings

cmd_router = Router()



@cmd_router.message(Command("about"), StateFilter('*'))
async def about_cmd(message: Message, state: FSMContext):
    await state.clear()
    await about_bot(message)
    
    
@cmd_router.message(Command("contacts"), StateFilter('*'))
async def contacts_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'По всем вопросам обращайтесь к моему создателю: @bratisman\n\n' +
                         f'Наш канал: @simplephysics_polyteh')
        
    
@cmd_router.message(Command("materials"), StateFilter('*'))
async def materials_cmd(message: Message, state: FSMContext):
    await state.clear()
    await get_categories_start(message, state)


@cmd_router.message(Command("videos"), StateFilter('*'))
async def videos_cmd(message: Message, state: FSMContext):
    await state.clear()
    await get_video_start(message, state)
    
    
@cmd_router.message(Command("menu"), StateFilter('*'))
async def menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in (settings.ADMIN_ID, settings.WRITER_ID):
        await message.answer("Меню", reply_markup=rp.start_admin)
    else:
        await message.answer("Меню", reply_markup=rp.start)