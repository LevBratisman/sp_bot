from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.bot.filters import AdminFilter
from app.common.repository.material_repository import MaterialRepository
from app.bot.keyboards.builder import CategoryDeleteCallBack, MaterialDeleteCallBack, get_categories_for_delete, get_materials_for_delete

from app.bot.keyboards import reply as rp
from app.bot.keyboards import inline as inl

material_settings_router = Router()


class AddMaterial(StatesGroup):
    category_id = State()
    name = State()
    file = State()
    

class DeleteMaterial(StatesGroup):
    category_id = State()
    name = State()


# ---------- ADD MATERIAL ----------

@material_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Добавить материал')
async def add_material_start(message: Message, state: FSMContext):
    await state.clear()

    category_kb = await get_categories_for_delete()

    if not category_kb:
        await message.answer('Вы еще не добавили категорий')
        return
    
    await state.set_state(AddMaterial.category_id)

    await message.answer("Выберите категорию:", reply_markup=category_kb)
    
    
@material_settings_router.callback_query(AddMaterial.category_id, CategoryDeleteCallBack.filter())
async def add_material_catalog(callback: CallbackQuery, callback_data: CategoryDeleteCallBack, state: FSMContext):
    if callback_data.action == 'cancel':
        await callback.answer('Отмена')
        await callback.message.edit_text('Действие отменено')
        await state.clear()
    else:
        await state.update_data(category_id=callback_data.id)
        await state.set_state(AddMaterial.name)

        await callback.answer()
        await callback.message.edit_text("Введите название материала")
    
    
@material_settings_router.message(AddMaterial.name)
async def add_material_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMaterial.file)
    await message.answer("Отправьте материал")


@material_settings_router.message(AddMaterial.file, F.document)
async def add_material_file(message: Message, state: FSMContext):
    await state.update_data(file=message.document.file_id)
    data = await state.get_data()
    await MaterialRepository.add(**data)
    await message.answer('Материал успешно добавлен!')

    await state.clear()
    
    

# ---------- DELETE MATERIAL ----------

@material_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Удалить материал')
async def del_material_start(message: Message, state: FSMContext):
    await state.clear()

    category_kb = await get_categories_for_delete()

    if not category_kb:
        await message.answer('Вы еще не добавили категорий')
        return
    
    await state.set_state(DeleteMaterial.category_id)

    await message.answer("Выберите категорию:", reply_markup=category_kb)
    
    
@material_settings_router.callback_query(DeleteMaterial.category_id, CategoryDeleteCallBack.filter(), F.data)
async def del_material_catalog(callback: CallbackQuery, callback_data: CategoryDeleteCallBack, state: FSMContext):
    if callback_data.action == 'cancel':
        await callback.answer('Отмена')
        await callback.message.edit_text('Действие отменено')
        await state.clear()
    else:
        materials_kb = await get_materials_for_delete(category_id=callback_data.id)

        if not materials_kb:
            await callback.message.edit_text('В данной категории нет материалов')
            await callback.answer('Действие отменено')
            await state.clear()
            return
        
        await callback.answer()
        
        await state.set_state(DeleteMaterial.name)
        
        await callback.message.edit_text('Выберите материал:', reply_markup=materials_kb)
    
    
@material_settings_router.callback_query(DeleteMaterial.name, MaterialDeleteCallBack.filter(), F.data)
async def del_material_name(callback: CallbackQuery, callback_data: MaterialDeleteCallBack, state: FSMContext):
    if callback_data.action == 'cancel':
        await callback.answer('Отмена')
        await callback.message.edit_text('Действие отменено')
    else:
        await MaterialRepository.delete(model_id=callback_data.id)
        await callback.answer('Удалено')

        await callback.message.edit_text("Материал успешно удален!")
    await state.clear()
