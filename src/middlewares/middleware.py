from loader import db, run
from aiogram.dispatcher.middlewares import BaseMiddleware  # класс Middleware от Aiogram
from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.dispatcher.handler import CancelHandler 
from config import admin_ids

class ResetUsername(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        if run.RUN_BOT:
            try:
                db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
            except:
                db.up_username(message.from_user.id, message.from_user.username, message.from_user.full_name)
        else:
            if message.text == '/on':
                run.on()
            else:
                await message.answer(
                    '<b>К сожалению, бот времено не работает</b>'
                    )       
                raise CancelHandler()
            
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        if run.RUN_BOT:
            try:
                db.add_user(call.from_user.id, call.from_user.username, call.from_user.full_name)
            except:
                db.up_username(call.from_user.id, call.from_user.username, call.from_user.full_name)
        else:
            await call.answer(
                '<b>К сожалению, бот времено не работает</b>',
                show_alert=True
                )
            raise CancelHandler()

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        if run.RUN_BOT:
            try:
                db.add_user(query.from_user.id, query.from_user.username, query.from_user.full_name)
            except:
                db.up_username(query.from_user.id, query.from_user.username, query.from_user.full_name)
        else:
            await query.answer(
                '<b>К сожалению, бот времено не работает</b>',
                show_alert=True
                )
            raise CancelHandler()
    