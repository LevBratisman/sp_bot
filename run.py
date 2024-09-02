import asyncio, logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings

from app.bot.cmd_list import private
from app.bot.handlers.common import common_router
from app.bot.handlers.commands import cmd_router
from app.bot.handlers.admin.base import admin_router
from app.bot.handlers.admin.category_settings import category_settings_router
from app.bot.handlers.admin.material_settings import material_settings_router
from app.bot.handlers.admin.video_settings import video_settings_router
from app.bot.handlers.materials import materials_router
from app.bot.handlers.base import base_router
from app.bot.handlers.video import video_router

dp = Dispatcher()
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


async def main():
    
    # Include routers
    dp.include_router(cmd_router)
    dp.include_router(admin_router)
    dp.include_router(common_router)
    dp.include_router(category_settings_router)
    dp.include_router(material_settings_router)
    dp.include_router(video_settings_router)
    dp.include_router(materials_router)
    dp.include_router(video_router)
    dp.include_router(base_router)
    
        
    # Start bot
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(private)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")
        