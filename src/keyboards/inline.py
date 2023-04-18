from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

cash_menu = InlineKeyboardMarkup(row_width= 2)

cash_menu.add(
    InlineKeyboardButton('📥 Пополнить', callback_data='cash_pay'),
    InlineKeyboardButton('📤 Вывести', callback_data='cash_out'),
)

cashout_menu = InlineKeyboardMarkup(row_width=1)

cashout_menu.add(
    InlineKeyboardButton('💵 Qiwi', callback_data='out_Qiwi'),
    InlineKeyboardButton('❇️ YooMoney', callback_data='out_Yoomoney'),
    #InlineKeyboardButton('💳 Visa, Mastercard, Мир', callback_data='out_card')
)



def payment_menu(url, bill_id= None):
    markup= InlineKeyboardMarkup()
    markup.insert(
    InlineKeyboardButton('💳 ОПЛАТИТЬ', url=url)
    )
    markup.add(
    InlineKeyboardButton('✅ Проверить платеж', callback_data=f"check_bill{str(bill_id)}")
    )
    return markup

def acceptOut_menu(bill_id):
    markup= InlineKeyboardMarkup(row_width=1)

    markup.add(
    InlineKeyboardButton('✅ Подтвердить вывод', callback_data='acceptwith_'+str(bill_id)),
    )
    return markup  

def games_menu():
    markup= InlineKeyboardMarkup(row_width=1)
    result=db.get_games()
    if result:
        for i in db.get_games():
            markup.add(
                InlineKeyboardButton(f'Игра #{i[0]} | {i[1]} ₽', callback_data=f'game_{i[0]}'),
            )
    markup.add(
        InlineKeyboardButton(f'🎲 Создать аукцион', callback_data=f'creategame'),
    )
        
    return markup

create_button= InlineKeyboardMarkup(row_width=1)

create_button.insert(
    InlineKeyboardButton('🎲 Создать аукцион', callback_data='creategame')
)

def bet_menu(bet, au_id):
    markup= InlineKeyboardMarkup(row_width=5)
    for i in range(bet+1, bet+11):
        markup.insert(
            InlineKeyboardButton(f'{i} ₽', callback_data=f"bet_{i}_{au_id}"),
            )
        
    
    return markup

accept_menu= InlineKeyboardMarkup(row_width=2)

accept_menu.add(
    InlineKeyboardButton('✅ Подтвердить заявку', callback_data='decide_accept'),
)
accept_menu.add(
    InlineKeyboardButton('✏️ Изменить заявку', callback_data='decide_edit'),
    InlineKeyboardButton(' Отменить заявку', callback_data='decide_cancel'),
)