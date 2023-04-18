from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from src.keyboards.inline import bet_menu
from loader import dp, db, bot
from datetime import datetime
from src.state.states import Game


@dp.callback_query_handler(text_contains= "game_")
async def game_handler(call: CallbackQuery, state: FSMContext):
    auction_id=call.data.replace('game_', '')
    au_info= db.get_game_Byid(auction_id)
    if au_info:
        count= db.count_users(auction_id)
        info_2= db.last_bet(auction_id)
        view_date= int(au_info[5]-datetime.timestamp(datetime.now()))
        view_date= view_date if view_date >= 0 else 0
        hour= view_date // 3600 if (view_date // 3600) > 9 else f"0{view_date // 3600}"
        minute= (view_date - (view_date // 3600) * 3600) // 60 if (view_date - (view_date // 3600) * 3600) // 60 > 9 else f"0{(view_date - (view_date // 3600) * 3600) // 60}"
        user= db.get_user(info_2[1])
        name= f"@{user[2]}" if user[2] else f"<b>{user[4]}</b>"
        balance= round(db.user_bal(call.message.chat.id), 1)
        await call.message.edit_text(f"""
👨🏻‍⚖️ Аукцион <code>#{auction_id}</code>
💵 Ваш баланс: {balance} ₽

<b>▫️ Статус:</b> проходит
<b>⏱ Осталось:</b> {hour}:{minute}
<b>💰 Банк аукциона:</b> {au_info[3]} рублей
<b>🔨 Количество ставок:</b> {count}

👑 <b>Лидер:</b> {name} поставил <b>{info_2[2]} рублей!</b>

👇 <i>Выберете количество рублей для повышения ставки:</i>""",
reply_markup= bet_menu(info_2[2], auction_id))
    else:
        await call.message.edit_text("Аукцион уже закончен!")
    
    
@dp.callback_query_handler(text_contains= "bet_")
async def bet_handler(call: CallbackQuery, state: FSMContext):
    res= call.data.split('_')
    bet=int(res[1])
    auction_id= res[2]
    if not(db.get_game_Byid(auction_id)) or bet- db.last_bet(auction_id)[3] > 0:
        await call.message.edit_text("<b>Устаревшие ставки, перезайдите в аукцион еще раз!</b>")
        return
    info_2= db.last_bet(auction_id)
    if call.message.chat.id == info_2[1]:
        await call.message.edit_text("<b>Пользователь не может сделать более одной ставки подряд</b>")
        return
    
    if bet <= db.user_bal(call.message.chat.id):
        db.up_balance(call.message.chat.id, -bet)
        db.new_bet(data= {
            'name' : auction_id,
            'user_id' : call.message.chat.id,
            'bet' : bet,
            'date' : datetime.timestamp(datetime.now())
        })
        au_info= db.get_game_Byid(auction_id)
        view_date= int(au_info[5]-datetime.timestamp(datetime.now()))
        hour= view_date // 3600 if (view_date // 3600) > 9 else f"0{view_date // 3600}"
        minute= (view_date - (view_date // 3600) * 3600) // 60 if (view_date - (view_date // 3600) * 3600) // 60 > 9 else f"0{(view_date - (view_date // 3600) * 3600) // 60}"
        count= db.count_users(auction_id)
        name= f"@{call.message.chat.username}" if call.message.chat.username else f"<b>{call.message.chat.full_name}</b>"
        balance= round(db.user_bal(call.message.chat.id), 1)
        
        await call.message.edit_text(f"""
👨🏻‍⚖️ Аукцион <code>#{auction_id}</code>
💵 Ваш баланс: {balance} ₽

<b>▫️ Статус:</b> проходит
<b>⏱ Осталось:</b> {hour}:{minute}
<b>💰 Банк аукциона:</b> {au_info[3]} рублей
<b>🔨 Количество ставок:</b> {count}

👑 <b>Лидер:</b> {name} поставил <b>{db.last_bet(auction_id)[2]} рублей!</b>

👇 <i>Выберете количество рублей для повышения ставки:</i>""",
reply_markup=bet_menu(db.last_bet(auction_id)[2], auction_id))
        db.add_desc(auction_id)
    else:
        await call.message.edit_text('Недостаточно средств')