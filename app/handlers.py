from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import asyncio

from app import keyboards


router = Router()


class AntiFlood(StatesGroup):
    generating_message = State()

@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAOfZdtFktnm8G3UklmN5pZy7Yv1VpoAAtQMAAJ6i6BIni8iJJQzvJs0BA")
    await asyncio.sleep(1)
    await message.answer("Добро пожаловать! Я бот проекта Simple Physics!")
    await asyncio.sleep(1)
    await message.answer("Что вы хотите?", reply_markup=keyboards.keyboard_start)
    
    
@router.message(Command("about"))
async def get_about_cmd(message: Message, state: FSMContext):
    await get_about_info(message, state)
    
@router.message(Command("contacts"))
async def get_about_cmd(message: Message):
    await message.answer("По всем вопросам обращайтесь к моему создателю: @bratisman")
    
    
@router.message(Command("faq"))
async def get_faq_cmd(message: Message):
    await message.answer("В разработке...")
    
    
@router.message(Command("materials"))
async def materials_cmd(message: Message):
    await message.answer("Подгружаю материалы...")
    await asyncio.sleep(1.5)
    await message.answer("Готово! Вот ссылки на материалы:", 
                         reply_markup=keyboards.materials_list)
    
@router.message(AntiFlood.generating_message)
async def anti_flood(message: Message, state: FSMContext):
    await asyncio.sleep(0.1)
    
@router.message(F.text=="Расскажи о себе🤔")
async def get_about_info(message: Message, state: FSMContext):
    await state.set_state(AntiFlood.generating_message)
    await message.answer_sticker(sticker="CAACAgIAAxkBAAPUZdtMgrKCGWN1hGG7sC9lB1Ob2nIAAhsTAAJakthIYwemdV7Qq5c0BA", 
                                 reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer("Моя основная задача - предоставлять вам учебные материалы по физике!")
    await asyncio.sleep(1)
    await message.answer("По сути, я являюсь хранилищем всего самого полезного, что создается командой Simple Physics")
    await asyncio.sleep(1)
    await message.answer("Если вы готовитесь к ЕГЭ по физике или просто хотите понять этот предмет, я и моя команда - именно то, что вам нужно!")
    await asyncio.sleep(2)
    await message.answer(f'Переходите на наш канал, где еженедельно выпускается много интересного и познавательного контента:\n\n https://t.me/simplephysics_polyteh', 
                         reply_markup=keyboards.keyboard_start)
    await state.clear()

@router.message(F.text=="Учебные материалы🔥")
async def get_list_materials(message: Message):
    await message.answer("Подгружаю материалы...")
    await asyncio.sleep(1.5)
    await message.answer("Готово! Вот ссылки на материалы:", 
                         reply_markup=keyboards.materials_list)
    

@router.message(F.content_type == ContentType.STICKER)
async def get_list_materials(message: Message):
    await message.answer(message.sticker.file_id)
    
    
@router.message(F.content_type == ContentType.DOCUMENT)
async def get_doc_id(message: Message):
    await message.answer(message.document.file_id)
    
@router.message()
async def echo(message: Message):
    await message.answer("Я еще не настолько умный🙈")
    await asyncio.sleep(0.5)
    await message.answer("Выберите ответ из предложенных ниже вариантов")