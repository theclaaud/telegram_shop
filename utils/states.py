from aiogram.fsm.state import StatesGroup, State

class AddCategory(StatesGroup):
    title = State()

class AddLot(StatesGroup):
    title = State()
    description = State()
    price = State()
    category = State()
    image = State()