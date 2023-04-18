from aiogram.dispatcher.filters.state import StatesGroup, State


class Deposit(StatesGroup):    
    sum = State()
    
class Game(StatesGroup):
    bet= State()
    
class CashOut(StatesGroup):    
    sum = State()
    system = State()
    data= State()
    accept= State()