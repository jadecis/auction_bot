from loader import dp
from aiogram import executor
from aiogram.types import BotCommand
from src.commands import start 
from src.handlers import main, game
from src.handlers.payment import deposit, withdrawal
from src.middlewares.middleware import ResetUsername
from src.notify import scheduler
import asyncio

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "restart bot")
    ])

async def start(dp):
    await set_default_commands(dp)
    asyncio.create_task(scheduler())
    

dp.middleware.setup(ResetUsername())
executor.start_polling(dp, skip_updates=False, on_startup=start)