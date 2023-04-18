from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.dispatcher import FSMContext
from src.keyboards.reply import main_menu
from loader import dp, run

@dp.message_handler(CommandStart(), state="*")
async def start_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer(f"""
🏆Стань победителем аукциона!🥸 
👥Соревнуйся с друзьями! 
🚴 Обгоняй конкурентов! 
💰 Забирай общий банк от всех ставок и зарабатывай на этом!🏦""", reply_markup=main_menu)
    
@dp.message_handler(commands='off', state="*")
async def start_handler(msg: Message, state: FSMContext):
    print(run.RUN_BOT)
    await state.finish()
    run.off()

@dp.message_handler(commands='on', state="*")
async def start_handler(msg: Message, state: FSMContext):
    await state.finish()
    run.on()
    
@dp.callback_query_handler(text_contains='acceptwith_')
async def acceptout_handler(call: CallbackQuery):
    bill_id= call.data.replace('acceptwith_', '')
    print(bill_id)
    await call.message.edit_text(f'{call.message.text}\n\n'
                                 +f"✅ Вывод ПОДТВЕРЖДЕН")