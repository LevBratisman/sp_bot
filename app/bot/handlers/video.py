from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.keyboards import reply as rp
from app.bot.keyboards import inline as inl
from app.bot.keyboards.builder import VideoCallBack, get_videos
from app.common.repository.video_repository import VideoRepository

from app.core.config import settings

video_router = Router()


class Videos(StatesGroup):
    file = State()
    to_menu = State()


# ------------ GET VIDEOS start ----------


@video_router.message(F.text == "🎥Видео-контент", StateFilter("*"))
async def get_video_start(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(Videos.file)
    video_kb = await get_videos()
    if not video_kb:
        await message.answer("Пусто...")
        await state.clear()
        return
    await message.answer("Выберите видео", reply_markup=video_kb)


@video_router.callback_query(Videos.file, VideoCallBack.filter())
async def choose_video(
    callback: CallbackQuery, callback_data: VideoCallBack, state: FSMContext, bot: Bot
):
    if callback_data.action == "back":
        await callback.answer(f"Меню")
        await state.clear()
        await callback.message.edit_text("Вы вышли из 'Видео-контент'")
    else:

        video = await VideoRepository.get_by_id(callback_data.id)
        if not video:
            await callback.answer("Видео не найдено")
            return
        else:
            try:
                await bot.send_video(
                    chat_id=callback.message.chat.id,
                    video=video.file,
                    caption=video.caption,
                )
            except Exception as e:
                await callback.answer("Видео не найдено")
                return

            await callback.answer("Видео-контент получен")
            await callback.message.delete()
            video_kb = await get_videos()
            if not video_kb:
                await callback.answer("Пусто...")
                await state.clear()
                return
            await callback.message.answer("Выберите видео", reply_markup=video_kb),
