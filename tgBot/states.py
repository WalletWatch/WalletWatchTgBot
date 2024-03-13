from aiogram.fsm.state import State, StatesGroup

class Wallet(StatesGroup):
    wallet_name = State()
    wallet_address = State()
    
class DeleteWallet(StatesGroup):
    id_wallet = State()

class Balance(StatesGroup):
    asset_address = State()
    network = State()
    wallet = State()

class DeleteBalance(StatesGroup):
    id_balance = State()