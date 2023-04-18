from aiogram import Bot, Dispatcher, types
from config import TOKEN_BOT, Run
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.database.db import Database
import logging
from yoomoney import Client
from config import YOOMONEY_TOKEN


bot = Bot(token=TOKEN_BOT, parse_mode=types.ParseMode.HTML)#<- &lt; >- &gt; &- &amp;
logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
dp= Dispatcher(bot, storage=MemoryStorage())
y_pay = Client(YOOMONEY_TOKEN)
run= Run()
db= Database("src/database/database.db")