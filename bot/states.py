from aiogram.fsm.state import State, StatesGroup

class Wallet(StatesGroup):
    wallet_name = State()
    wallet_address = State()
    
class DeleteWallet(StatesGroup):
    id_wallet = State()

class WatchWallet(StatesGroup):
    id_wallet = State()

class TokenWatch(StatesGroup):
    id_token = State()

class UserState(StatesGroup):
    some_state = State()