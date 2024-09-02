import asyncio, os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import reply as rp

base_router = Router()

@base_router.message()
async def echo(message: Message):
    await message.answer("Я не понимаю")