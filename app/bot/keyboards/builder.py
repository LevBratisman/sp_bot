import asyncio

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from app.common.repository.category_repository import CategoryRepository
from app.common.repository.material_repository import MaterialRepository
from app.common.repository.video_repository import VideoRepository


class MaterialCallBack(CallbackData, prefix="material"):
    id: int | None = None
    name: str | None = None
    action: str | None = None

class MaterialDeleteCallBack(CallbackData, prefix="material_delete"):
    id: int | None = None
    action: str | None = None


class CategoryCallBack(CallbackData, prefix="category"):
    id: int | None = None
    action: str | None = None

class CategoryDeleteCallBack(CallbackData, prefix="category_delete"):
    id: int | None = None
    action: str | None = None


class VideoCallBack(CallbackData, prefix="video"):
    id: int | None = None
    action: str | None = None

class VideoDeleteCallBack(CallbackData, prefix="video_delete"):
    id: int | None = None
    action: str | None = None



# ---------Categories keyboard----------

async def get_categories():
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=CategoryCallBack(action="back").pack()))
    
    categories = await CategoryRepository.get_all()

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=CategoryCallBack(id=category.id, action='show').pack()))
        
    if not categories:
        return None

    return keyboard.adjust(1, 2).as_markup()



async def get_categories_for_delete():
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=CategoryDeleteCallBack(action="cancel").pack()))
    
    categories = await CategoryRepository.get_all()

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=CategoryDeleteCallBack(id=category.id, action='delete').pack()))
        
    if not categories:
        return None

    return keyboard.adjust(1, 2).as_markup()
    
    

# ---------Materials keyboard----------

async def get_materials(category_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=MaterialCallBack(action="back").pack()))
    
    materials = await MaterialRepository.get_all(category_id=category_id)

    for material in materials:
        keyboard.add(InlineKeyboardButton(text=material.name, callback_data=MaterialCallBack(id=material.id, name=material.name, action='show').pack()))

    if not materials:
        return None
        
    return keyboard.adjust(1, 2).as_markup()



async def get_materials_for_delete(category_id: int):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=MaterialDeleteCallBack(action="cancel").pack()))
    
    materials = await MaterialRepository.get_all(category_id=category_id)

    for material in materials:
        keyboard.add(InlineKeyboardButton(text=material.name, callback_data=MaterialDeleteCallBack(id=material.id, action='delete').pack()))
        
    if not materials:
        return None

    return keyboard.adjust(1, 2).as_markup()
    
    
    
# ---------Videos keyboard----------

async def get_videos():
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="<< Назад", callback_data=VideoCallBack(action="back").pack()))
    
    videos = await VideoRepository.get_all()

    for video in videos:
        keyboard.add(InlineKeyboardButton(text=video.name, callback_data=VideoCallBack(id=video.id, action='show').pack()))

    if not videos:
        return None
        
    return keyboard.adjust(1, 2).as_markup()



async def get_videos_for_delete():
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=VideoDeleteCallBack(action="cancel").pack()))
    
    videos = await VideoRepository.get_all()

    for video in videos:
        keyboard.add(InlineKeyboardButton(text=video.name, callback_data=VideoDeleteCallBack(id=video.id, action='delete').pack()))
        
    if not videos:
        return None
        
    return keyboard.adjust(1, 2).as_markup()