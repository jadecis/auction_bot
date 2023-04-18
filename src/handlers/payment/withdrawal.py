from loader import dp, db, bot
from src.state.states import CashOut
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from src.keyboards.inline import cashout_menu, accept_menu, acceptOut_menu
from src.keyboards.reply import main_menu
from datetime import datetime
from config import admin_chat
import uuid



@dp.callback_query_handler(text_contains='cash_out')
async def out_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("📤 Вывод средств\n\n"
                                 +f"📌 Комиссия: <b>5 %</b>\n"
                                 +f"📌 Минимум: <b>100💲</b>\n"
                                 +f"📌 Максимум: <b>1000💲</b>\n\n"
                                +f"<i>Отправь сумму вывода:</i>")
    await CashOut.sum.set()


@dp.message_handler(content_types=['text'], state=CashOut.sum)
async def cash_sum_handler(msg: Message, state: FSMContext):
    try:
        sum = float(msg.text)
        if 100 <= sum <= db.get_user(msg.chat.id)[3] and sum <= 1000:
            await state.update_data(sum=float(msg.text))
            await  msg.answer(text=f"Выбери способ вывода:", 
                              reply_markup=cashout_menu)
            await CashOut.system.set() 
        else:
            raise Exception
    except Exception as ex:
        await msg.answer(text=f"❗️<b>Некорректная сумма</b>❗️\n\n"
                             +f"📌 Комиссия: <b>5 %</b>\n"
                             +f"📌 Минимум: <b>100💲</b>\n"
                             +f"📌 Максимум: <b>1000💲</b>\n\n"
                             +f"🏦 Ваш баланс: <b>{db.get_user(msg.chat.id)[3]}💲</b>\n\n"
                             +f"<i>Отправь новую сумму вывода:</i>")
        await CashOut.sum.set()
        
@dp.callback_query_handler(text_contains= "out_", state=CashOut.system)      
async def out_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(system=call.data.split('_')[1])
    if call.data== 'out_Qiwi' or call.data == 'out_Yoomoney':
        await call.message.edit_text("Введи номер телефона привязанный к кошельку:\n\n"
                                     +f"Пример: 79001234567")
        await CashOut.data.set()
    else:
        await call.message.edit_text("Введи номер карты:\n\n"
                                     +f"Пример: 1234567890123456")
        await CashOut.data.set()
        
@dp.message_handler(content_types=['text'], state= CashOut.data)
async def cash_data_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    date= datetime.timestamp(datetime.now())
    sum= data.get('sum')
    system= data.get('system')
    request={
        'sum' : sum,
        'sumw' : sum - (sum * 0.05),
        'system' : system,
        'date' : date,
        'wallet' : msg.text
    }
    await state.update_data(request=request)
    if system== 'card':
        system = "Банковская карта"
    await msg.answer(f"♻️ <b>{system}:</b> <code>{msg.text}</code>\n"
                     +f"🔻 <b>Сумма вывода:</b> <code>{sum}</code>💲\n"
                     +f"🔻 <b>Сумма вывода с комиссией:</b> <code>{sum - (sum * 0.05)}</code>💲\n"
                     +f"🔻 <b>Дата:</b> <code>{datetime.fromtimestamp(date).strftime('%d.%m.%Y %H:%M')}</code>\n\n"
                     +f"<b>Все верно?</b>",
                      reply_markup= accept_menu)
    await CashOut.accept.set()
    
@dp.callback_query_handler(text_contains='decide_', state=CashOut.accept)
async def decide_handler(call: CallbackQuery, state: FSMContext):
    if call.data == 'decide_edit':
        await call.message.edit_text("📤 Вывод средств\n\n"
                                     +f"📌 Комиссия: <b>5 %</b>\n"
                                     +f"📌 Минимум: <b>100💲</b>\n"
                                     +f"📌 Максимум: <b>5000💲</b>\n\n"
                                     +f"<i>Отправь сумму вывода:</i>")
        await CashOut.sum.set()
    elif call.data == 'decide_cancel':
        await state.finish()
        await call.message.edit_text("Вот главное меню 👇", reply_markup=main_menu)
        await state.finish()
    else:
        data= await state.get_data()
        request= data.get('request')
        bill_id= str(uuid.uuid4())
        msg_id= await bot.send_message(chat_id=admin_chat,
                               text=f"<b>Заявка на вывод</b>\n\n"
                     +f"🔻 <b>User ID:</b> <code>{call.message.chat.id}</code>\n"
                     +f"♻️ <b>{request['system']}:</b> <code>{request['wallet']}</code>\n"
                     +f"🔻 <b>Сумма вывода:</b> <code>{request['sum']}</code>💲\n"
                     +f"🔻 <b>Сумма вывода с комиссией:</b> <code>{request['sumw']}</code>💲\n"
                     +f"🔻 <b>Дата:</b> <code>{datetime.fromtimestamp(request['date']).strftime('%d.%m.%Y %H:%M')}</code>\n\n"
                     +f"🔻 <b>ID:</b> <code>{bill_id}</code>",
                     reply_markup=acceptOut_menu(bill_id)
                     )
        
        # bill={
        #     'id' : bill_id,
        #     'msg_id' : msg_id.message_id,
        #     'wallet' : request['wallet'],
        #     'system' : request['system'],
        #     'sum' : request['sumw'],
        #     'date' : request['date']}
        
        # db.add_out(
        #     user_id=call.message.chat.id,
        #     bill=bill)
        # db.add_bill(
        #     user_id=call.message.chat.id,
        #     bill_id=bill_id,
        #     typep='withdrawal')
        db.up_balance(
            user_id=call.message.chat.id,
            sum=-int(request['sum']))
        
        
        await call.message.edit_text(f"<b>Заявка на вывод</b>\n\n"
                    +f"♻️ <b>{request['system']}:</b> <code>{request['wallet']}</code>\n"
                     +f"🔻 <b>Сумма вывода:</b> <code>{request['sum']}</code>💲\n"
                     +f"🔻 <b>Сумма вывода с комиссией:</b> <code>{request['sumw']}</code>💲\n"
                     +f"🔻 <b>Дата:</b> <code>{datetime.fromtimestamp(request['date']).strftime('%d.%m.%Y %H:%M')}</code>\n\n"
                     +f"🔻 <b>ID:</b> <code>{bill_id}</code>"
                    #  reply_markup=cancelOut_menu(bill_id)
                     )
        
        await call.message.answer(f"<b>Ваша заявка отправлена администраторам!</b>\n"
                                  "<i><b>Обработка заявок по регламенту проекта - до 24 часов.</b></i>",
                                  reply_markup=main_menu)
        await state.finish()