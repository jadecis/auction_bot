from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from src.keyboards.inline import games_menu, cash_menu, create_button, bet_menu
from loader import dp, db
from datetime import datetime
from src.state.states import Game

@dp.message_handler(Text('⚙️ Профиль'), state="*")
async def profile_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer(f"""
🆔 ID: <code>{msg.chat.id}</code>
🌐 Nickname: @{msg.chat.username}
🏦 Баланс: <b>{db.user_bal(msg.chat.id)}</b> рублей""")
    
    
@dp.message_handler(Text('ℹ️ О боте'), state="*")
async def info_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("""Бот создан при поддержке @PlayMoney7xBot""")

@dp.message_handler(Text('🏦 Баланс'), state="*")
async def games_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer(f"<i>{msg.from_user.first_name}, твой Баланс:</i>"
                     +f" <b>{round(db.user_bal(msg.chat.id), 1)} ₽</b>",
                         reply_markup= cash_menu)


@dp.message_handler(Text('🎮 Аукционы'), state="*")
async def games_handler(msg: Message, state: FSMContext):
    await state.finish()
    rools= """
👨🏻‍⚖️ Аукцион:

Правила аукциона:
🔸Любой участник может начать аукцион ставкой от 10 рублей. 
🔸Аукцион может быть завершен при одной единственной ставке. 
🔸Любой участник может повысить предыдущую ставку и стать лидером. 
🔸Максимальный шаг повышения - 10 рублей. 
🔸После повышения стартовой, и каждой дальнейшей ставки аукцион продолжается 15 минут. 
🔸Как только таймер доходит до нуля, деньги зачисляются тому, кто сделал последнюю ставку. 
🔸Пользователь не может сделать более одной ставки подряд. 
🔸На момент завершения аукциона, победитель получает 90% суммы от всех ставок аукциона на счет для вывода. 
🔸Если ставка единственная (никто не перебил стартовую ставку) аукцион завершится через 1 час, открывшему начисляется 110%

"""
    if db.get_games():
        await msg.answer(f"{rools}🎲 <b>Создайте аукцион или выберите уже имеющийся:</b> 👇", reply_markup=games_menu())
    else:
        await msg.answer(f"{rools}🎲 <b>Создайте новый аукцион!</b>", reply_markup=create_button)
        
@dp.callback_query_handler(text='creategame')
async def creategame_handler(call: CallbackQuery, state: FSMContext):
    balance= round(db.user_bal(call.message.chat.id), 1)
    await call.message.edit_text(text=f"💵 Ваш баланс: {balance} ₽"
                            "💰 Введите сумму ставки от 10 до 5000₽")
    await Game.bet.set()

@dp.message_handler(content_types='text', state=Game.bet)
async def info_handler(msg: Message, state: FSMContext):
    try:
        sum= int(msg.text)
    except:
        await msg.answer("Ошибка ввода данных!")
        return
    if sum <= db.user_bal(msg.chat.id): 
        db.up_balance(msg.chat.id, -sum)
        td= datetime.timestamp(datetime.now())
        db.add_auction(
            data={
                'user_id' : msg.chat.id,
                'name' : str(int(td)),
                'bet' : sum,
                'date' : td,
                'end_date' : td + 3600
            }
        )
        name= f"@{msg.chat.username}" if msg.chat.username else f"<b>{msg.chat.full_name}</b>"
        balance= round(db.user_bal(msg.chat.id), 1)
        await msg.answer(f"""
👨🏻‍⚖️ Аукцион <code>#{str(int(td))}</code>
💵 Ваш баланс: {balance} ₽

<b>▫️ Статус:</b> проходит
<b>⏱ Осталось:</b> 01:00
<b>💰 Банк аукциона:</b> {sum} рублей
<b>🔨 Количество ставок:</b> 1

👑 <b>Лидер:</b> {name} поставил <b>{sum} рублей!</b>""", reply_markup=bet_menu(sum, str(int(td))))
    else:
        await msg.answer('Недостаточно средств')
    await state.finish()