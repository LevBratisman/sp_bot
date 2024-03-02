from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


keyboard_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            
            KeyboardButton(text="Учебные материалы🔥")
        ],
        [
            KeyboardButton(text="Расскажи о себе🤔")
        ]
    ],
    resize_keyboard=True
)


# INLINE


materials_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Конспекты", 
                            callback_data="conspects")
    ],
    [
        InlineKeyboardButton(text="Теория в карточках", 
                            callback_data="cards_theory")
    ],
    [
        InlineKeyboardButton(text="Все формулы для ЕГЭ", 
                            callback_data="formulas")
    ],
    [
        InlineKeyboardButton(text="Исторические справки",
                            callback_data="historical_references")
    ],
])

conspect_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Статика", 
                            callback_data="static")
    ],
    [
        InlineKeyboardButton(text="Ньютон", 
                            callback_data="nuton")
    ],
    [
        InlineKeyboardButton(text="Вернуться назад", 
                            callback_data="back_to_materials")
    ]
])

cards_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вернуться назад", 
                            callback_data="back_to_materials")
    ]
])

formulas_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вернуться назад", 
                            callback_data="back_to_materials")
    ]
])

references_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Галилео", 
                            callback_data="galileo")
    ],
    [
        InlineKeyboardButton(text="Тесла", 
                            callback_data="tesla")
    ],
    [
        InlineKeyboardButton(text="Вернуться назад", 
                            callback_data="back_to_materials")
    ]
])