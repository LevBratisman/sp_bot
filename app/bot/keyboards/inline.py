from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

confirm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])


confirm_sendall = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отправить всем", callback_data="sendall"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])


back = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="<< Назад", callback_data="back"),
    ]
])


web_app_info = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [
        InlineKeyboardButton(text='Веб-приложение', web_app=WebAppInfo(url=f'https://simplephysics.ru/'))
    ]
])