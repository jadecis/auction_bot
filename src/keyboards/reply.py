from aiogram.types import ReplyKeyboardMarkup

main_menu= ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

main_menu.add(
    '🎮 Аукционы', '🏦 Баланс', '⚙️ Профиль',
                'ℹ️ О боте'
)