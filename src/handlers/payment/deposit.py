from loader import dp, db, y_pay, bot
from src.state.states import Deposit
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import uuid
from config import YOOMONEY_WALLET
from yoomoney import Quickpay
from src.keyboards.inline import payment_menu


@dp.callback_query_handler(text_contains='cash_pay')
async def pay_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🏦 Пополнить счёт (Комиссия 3%)\n\n"
                                 +"📌 Минимум: <b>100 💲</b>\n"
                                 +"📌 Максимум: <b>5000 💲</b>\n\n"
                                +f"<i>Отправь сумму пополнения:</i>")
    await Deposit.sum.set()     

@dp.message_handler(content_types=['text'], state=Deposit.sum)
async def dep_sum_handler(msg: Message, state: FSMContext):
    try:
        price = float(msg.text)
        if 5000 >= price >= 10:
            bill_id= str(uuid.uuid4())
            bill = Quickpay(
                receiver=YOOMONEY_WALLET,
                quickpay_form='shop',
                targets='Photo bot',
                paymentType='SB',
                sum=price,
                label=bill_id)
        await msg.answer(text=f'📍 <b>Счет для оплаты готов</b> 📍\n\n<i>Для оплаты нажмите кнопку ниже 💳\n\nПосле оплаты нажмите на кнопку «Проверить платеж», для проверки платежа</i>',
                        reply_markup=payment_menu(url=bill.redirected_url,
                                                 bill_id=bill_id))
    except Exception as ex:
        print(ex)
        await msg.answer(text=f"❌ <b>НЕВЕРНАЯ СУММА</b> ❌\n\n"
                         +f"📌 Минимум: <b>10 💲</b>\n"
                        +f"📌 Максимум: <b>5000 💲</b>\n\n"
                         +f"<i>Отправь новую сумму пополнения:</i>")
       
@dp.callback_query_handler(text_contains='check_bill', state= "*")
async def check_bill_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    bill_id= call.data.replace('check_bill', "")
    history = y_pay.operation_history(label=bill_id)
    try:
        result= history.operations[-1]
        status=result.status
        if status== 'PAID' or status == 'success' or status == 'paid':
            print(result)
            db.up_balance(
                call.message.chat.id,
                result.amount
            )
            await call.message.edit_text("Оплата прошла успешно!")
            await state.finish()
    except Exception as ex:
        print(ex)
        await bot.answer_callback_query(call.id, "❌ Оплата не прошла!\nПовторите попытку!", show_alert=True)