from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from text import NO_WALLET, CHOOSE, ADD_WALLET_MESSAGE, WALLET_DOESNT_EXIST, WALLET_LIST
from states import Wallet, DeleteWallet, WatchWallet, TokenWatch
from db.db import Database
from utils import is_wallet_connected, createAsset
from kb import make_wallet_keyboard, make_token_keyboard, make_token_menu

router_wallet = Router()
db = Database()

# SHOW WALLET INFO
@router_wallet.message(Command("wallets"))
async def wallets_handler(msg: Message):
    user = msg.from_user.id
    wallets = db.get_user_wallets(user)

    if len(wallets) == 0:
        await msg.answer(NO_WALLET)
    else:
        answer = WALLET_LIST
        for wallet in wallets:
            answer += f"Wallet: {wallet[1]}\n\
Balance: {wallet[3]}\n\n"
        
        answer += ADD_WALLET_MESSAGE
        await msg.answer(text=answer, parse_mode='Markdown')

@router_wallet.callback_query(F.data =="wallets")
async def wallets_handler(callback: CallbackQuery):
    user = callback.from_user.id
    wallets = db.get_user_wallets(user)

    if len(wallets) == 0:
        await callback.message.answer(NO_WALLET)
    else:
        answer = WALLET_LIST
        for wallet in wallets:
            answer += f"Wallet: {wallet[1]}\n\
Balance: {wallet[3]}\n\n"
        
        answer += ADD_WALLET_MESSAGE
        await callback.message.answer(text=answer, parse_mode='Markdown')

# SHOW WALLET TOKENS

@router_wallet.message(Command("walletmenu"))
async def wallets_handler(msg: Message, state: FSMContext):
    user = msg.from_user.id
    wallets = db.get_user_wallets(user)

    if len(wallets) == 0:
        await msg.answer(NO_WALLET)
    else:
        await msg.answer(text="Выберите кошелёк: ", reply_markup=make_wallet_keyboard(user), parse_mode='Markdown')
        await state.set_state(WatchWallet.id_wallet)

@router_wallet.callback_query(F.data =="walletmenu")
async def wallets_handler(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user.id
    wallets = db.get_user_wallets(user)

    if len(wallets) == 0:
        await callback.message.answer(NO_WALLET)
    else:
        await callback.message.answer(text="Выберите кошелёк: ", reply_markup=make_wallet_keyboard(user), parse_mode='Markdown')
        await state.set_state(WatchWallet.id_wallet)

@router_wallet.callback_query(WatchWallet.id_wallet)
async def balance_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Выберите токен: ", reply_markup=make_token_keyboard(callback.data),  parse_mode='Markdown')
    await state.clear()

@router_wallet.callback_query(F.data.startswith("token"))
async def show_balance(callback: CallbackQuery):
    token_id = callback.data.split("_")[1]
    token = db.get_balance(int(token_id))
    network = db.get_network(token[8])

    answer = f"*Токен*: *{token[1]}*\n\
    - Количество: *{round(token[3], 2)}* {token[1]}\n\
    - Цена: *${round(token[4], 4)}* за 1 {token[1]}\n\
    - Сумма: *${round(token[3] * token[4], 2)}*\n\
    - Сеть: *{network[1]}*\n"
    
    await callback.message.answer(answer, parse_mode='Markdown')
    await callback.message.answer(text=CHOOSE, reply_markup=make_token_menu(token[0], token[6]))


# SETTIGNS FOR TOKENS
@router_wallet.callback_query(F.data.startswith("track"))
async def change_track_token(callback: CallbackQuery):
    token_id = callback.data.split("_")[1]
    token = db.get_balance(int(token_id))
    if (token[6]):
        await callback.message.answer("Теперь Вы не будете получаеть уведомления по этому токену.")
    else:
        await callback.message.answer("Теперь Вы будете получаеть уведомления по этому токену.")
    db.update_track_balance(token_id, not token[6])

@router_wallet.callback_query(F.data.startswith("delta"))
async def change_track_token(callback: CallbackQuery, state: FSMContext):
    token = callback.data.split("_")[1]
    await state.update_data(id_token=int(token))

    await callback.message.answer("Введите новое значение: ")
    await state.set_state(TokenWatch.delta)

@router_wallet.message(TokenWatch.delta, F.text)
async def input_delta(message: Message, state: FSMContext):
    try:
        value = float(message.text)
    except ValueError:
        await message.answer("Попробуйте ввести другое значение!")
        await state.set_state(TokenWatch.delta)
        return
    
    user_data = await state.get_data()
    db.update_delta_balance(user_data['id_token'], value)
    message.answer("Вы успешно поменяли значение!")
    await state.clear()


# DELETE WALLET

@router_wallet.message(Command("deletewallet"))
async def wallets_delete_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if len(db.get_user_wallets(user_id)) == 0:
        await message.answer(NO_WALLET)
        return 
    
    await message.answer(f"Выберите кошелек, который вы хотите удалить:", reply_markup=make_wallet_keyboard(user_id), parse_mode='Markdown')
    await state.set_state(DeleteWallet.id_wallet)

@router_wallet.callback_query(F.data == "deletewallet")
async def balance_delete_handler(calback: CallbackQuery, state: FSMContext):
    user_id = calback.from_user.id
    await calback.message.answer(f"Выберите кошелек, который вы хотите удалить:", reply_markup=make_wallet_keyboard(user_id), parse_mode='Markdown')
    await state.set_state(DeleteWallet.id_wallet)


@router_wallet.callback_query(DeleteWallet.id_wallet)
async def wallets_delete(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user.id
    db.delete_wallet(user_id=user, wallet_id=callback.data)
    await state.clear()
    await callback.message.answer("Кошелёк удален!")

# ADD WALLET

@router_wallet.message(StateFilter(None), Command("addwallet"))
async def add_wallet(message: Message, state: FSMContext):
    await message.answer("Введите *адресс кошелька,* который хотите добавить или /cancel, если захотите прекратить: ", parse_mode='Markdown')
    await state.set_state(Wallet.wallet_address)

@router_wallet.callback_query(F.data =="addwallet")
async def add_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите *адресс кошелька*, который хотите добавить или /cancel, если захотите прекратить: ", parse_mode='Markdown')
    await state.set_state(Wallet.wallet_address)


@router_wallet.message(Wallet.wallet_address, Command("cancel"))
async def cancel_wallet(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание прекращено!")

@router_wallet.message(Wallet.wallet_name, Command("cancel"))
async def cancel_wallet(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание прекращено!")

@router_wallet.message(Wallet.wallet_address, F.text)
async def add_wallet_address(message: Message, state: FSMContext):
    await state.update_data(inputed_wallet_address=message.text)
    await message.answer(f"Теперь задайте *название* для введённого адреса кошелька", parse_mode='Markdown')
    await state.set_state(Wallet.wallet_name)

@router_wallet.message(Wallet.wallet_name, F.text)
async def add_wallet_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = message.from_user.id

    if not is_wallet_connected(user_data['inputed_wallet_address']):
        await message.answer(WALLET_DOESNT_EXIST)
        await message.answer("Введите адресс кошелька, который хотите добавить: ")
        await state.clear()
        await state.set_state(Wallet.wallet_address)
        return
    
    if not db.check_wallet(user_data['inputed_wallet_address'], user):
        await message.answer("Кошелек с таким адресом уже добавлен.")
        await state.clear()
        return

    wallet_id = db.add_wallet(user, message.text, user_data['inputed_wallet_address'])
    await message.answer(
        text=f"Вы добавили кошелек с названием <b>{message.text}</b> и адресом <b>{user_data['inputed_wallet_address']}</b>. ", 
        parse_mode="HTML"
    )
    createAsset(wallet_address=user_data['inputed_wallet_address'], wallet_id=wallet_id, user=user)
    await state.clear()

    # except:
    #     await message.answer(WALLET_WRONG)
    #     await message.answer("Введите адресс кошелька, который хотите добавить: ")
    #     await state.clear()
    #     await state.set_state(Wallet.wallet_address)
