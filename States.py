from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    CryptoAsk = State()
    RememberAsk = State()
    budget_summa = State()
    budget_name = State()