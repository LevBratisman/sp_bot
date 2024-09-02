from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.filters import AdminFilter
from app.common.repository.video_repository import VideoRepository
from app.bot.keyboards.builder import get_videos_for_delete, VideoDeleteCallBack


video_settings_router = Router()


class AddVideo(StatesGroup):
    name = State()
    file = State()
    caption = State()

class DeleteVideo(StatesGroup):
    name = State()

# ---------- ADD VIDEO ----------

@video_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Добавить видео')
async def add_video_start(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(AddVideo.name)
    await message.answer("Напишите название видео")
    
    
@video_settings_router.message(AddVideo.name, F.text)
async def add_video_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddVideo.file)
    await message.answer("Отправьте видео")
    
    
@video_settings_router.message(AddVideo.file, F.video)
async def add_video_content(message: Message, state: FSMContext):
    await state.update_data(file=message.video.file_id)
    await state.set_state(AddVideo.caption)
    await message.answer("Введите описание")
    
    
@video_settings_router.message(AddVideo.caption, F.text)
async def add_video_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    data = await state.get_data()

    await VideoRepository.add(**data)
    await message.answer('Видео успешно добавлено!')
    await state.clear()
    


# ---------- DELETE VIDEO ----------

@video_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Удалить видео')
async def del_video_start(message: Message, state: FSMContext):
    await state.clear()

    video_kb = await get_videos_for_delete()

    if not video_kb:
        await message.answer('Вы еще не опубликовали видео')
        await state.clear()
        return
    
    await message.answer("Выберите видео:", reply_markup=video_kb)
    
    
@video_settings_router.callback_query(VideoDeleteCallBack.filter(), F.data)
async def del_video_name(callback: CallbackQuery, callback_data: VideoDeleteCallBack):
    if callback_data.action == 'cancel':
        await callback.answer('Отмена')
        await callback.message.edit_text('Действие отменено')
    else:
        await VideoRepository.delete(model_id=callback_data.id)

        await callback.answer('Удалено')
        await callback.message.edit_text(f"Видео успешно удалено!")
    
    
    
    