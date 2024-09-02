from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.filters import AdminFilter
from app.common.repository.category_repository import CategoryRepository
from app.common.repository.material_repository import MaterialRepository
from app.bot.keyboards.builder import CategoryDeleteCallBack
from app.bot.keyboards import builder


category_settings_router = Router()


class AddCategory(StatesGroup):
    name = State()
    

# ---------- ADD MATERIAL ----------

@category_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Добавить категорию')
async def add_category_start(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(AddCategory.name)
    await message.answer("Напишите название категории")
    
@category_settings_router.message(AddCategory.name, F.text)
async def add_category_name(message: Message, state: FSMContext):
    await CategoryRepository.add(name=message.text)
    await message.answer(f"Категория '{message.text}' успешно добавлена!")
    await state.clear()
    


# ---------- DELETE MATERIAL ----------

@category_settings_router.message(AdminFilter(), StateFilter('*'), F.text == 'Удалить категорию')
async def del_category_start(message: Message, state: FSMContext):
    await state.clear()

    category_kb = await builder.get_categories_for_delete()

    if not category_kb:
        await message.answer('Вы еще не добавили категорий')
        return
    
    await message.answer("Выберите категорию:", reply_markup=category_kb)

    
    
@category_settings_router.callback_query(StateFilter(None), CategoryDeleteCallBack.filter(), F.data)
async def del_category_name(callback: CallbackQuery, callback_data: CategoryDeleteCallBack, state: FSMContext):
    if callback_data.action == 'cancel':
        await callback.answer('Отмена')
        await callback.message.edit_text('Действие отменено')
    else:
        await MaterialRepository.delete_by(category_id=callback_data.id)
        await CategoryRepository.delete(model_id=callback_data.id)

        await callback.answer('Удалено')
        await callback.message.edit_text(f"Категория успешно удалена!")    
    