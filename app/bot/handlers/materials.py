from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.keyboards import reply as rp
from app.bot.keyboards import inline as inl
from app.bot.keyboards.builder import (
    get_categories,
    CategoryCallBack,
    get_materials,
    MaterialCallBack,
)
from app.common.repository.material_repository import MaterialRepository

from app.core.config import settings

materials_router = Router()


class Materials(StatesGroup):
    category_id = State()
    material = State()
    to_menu = State()


# ------------ GET MATERIALS ----------


@materials_router.message(F.text == "📖Материалы", StateFilter("*"))
async def get_categories_start(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(Materials.material)
    category_kb = await get_categories()
    if not category_kb:
        await message.answer("Пусто...")
        await state.clear()
        return
    await message.answer("Выберите категорию", reply_markup=category_kb)


@materials_router.callback_query(Materials.material, CategoryCallBack.filter())
async def choose_category(
    callback: CallbackQuery, callback_data: CategoryCallBack, state: FSMContext
):
    if callback_data.action == "back":
        await callback.answer(f"Меню")
        await state.clear()
        await callback.message.edit_text("Вы вышли из 'Материалы'")
    else:
        material_kb = await get_materials(callback_data.id)
        if not material_kb:
            await callback.answer("Пусто...")
            return
        else:
            await callback.answer("Выбор материала")
            await state.update_data(category_id=callback_data.id)
            await state.set_state(Materials.material)

            await callback.message.edit_text(
                "Выберите материал:", reply_markup=material_kb
            )


@materials_router.callback_query(Materials.material, MaterialCallBack.filter())
async def get_material(
    callback: CallbackQuery, callback_data: MaterialCallBack, state: FSMContext
):
    if callback_data.action == "back":
        await callback.answer("Категории")
        await state.set_state(Materials.material)
        await callback.message.edit_text(
            "Выберите категорию:", reply_markup=await get_categories()
        )
    else:
        material = await MaterialRepository.get_by_id(model_id=callback_data.id)
        if not material:
            await callback.answer("Материал не найден")
            return
        else:
            await state.update_data(material=callback_data.id)
            file = material.file
            try:
                await callback.message.answer_document(file)
            except Exception as e:
                await callback.answer("Материал не найден")
                return

            await callback.message.delete()
            await callback.answer("Материал получен!")
            data = await state.get_data()
            material_kb = await get_materials(data["category_id"])

            await callback.message.answer(
                "Выберите материал:", reply_markup=material_kb
            )
