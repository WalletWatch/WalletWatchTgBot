from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from text import GREETING, NO_WALLET, WALLET_LIST, ADD_WALLET_MESSAGE, WALLET_DOESNT_EXIST, WALLET_WRONG
from utils import wallet_list, create_wallet, delete_wallet
from states import Wallet, DeleteWallet
from kb import make_wallet_keyboard

router_wallet = Router()

@router_wallet.message(Command("wallets"))
async def wallets_handler(msg: Message):
    wallets = wallet_list()
    if len(wallets) == 0:
        await msg.answer(NO_WALLET)
    else:
        answer = WALLET_LIST
        for indx in range(len(wallets)):
            name = wallets[indx]['wallet_name']
            address = wallets[indx]['wallet_address']
            answer += f'    *{name}: *' + f'{address}'
    
        answer += ADD_WALLET_MESSAGE
        await msg.answer(text=answer,  parse_mode='Markdown')

@router_wallet.callback_query(F.data =="wallets")
async def wallets_handler(callback: CallbackQuery):
    wallets = wallet_list()
    if len(wallets) == 0:
        await callback.message.answer(NO_WALLET)
    else:
        answer = WALLET_LIST + "\n"
        for indx in range(len(wallets)):
            name = wallets[indx]['wallet_name']
            address = wallets[indx]['wallet_address']
            answer += f'    *{name}: *' + f'{address}\n\n'
                                        
        answer += ADD_WALLET_MESSAGE
        await callback.message.answer(text=answer, parse_mode='Markdown')


@router_wallet.message(Command("deletewallet"))
async def wallets_delete_handler(message: Message, state: FSMContext):
    await message.answer(f"Выберите кошелек, который вы хотите удалить:", reply_markup=make_wallet_keyboard(), parse_mode='Markdown')
    await state.set_state(DeleteWallet.id_wallet)

@router_wallet.callback_query(F.data == "deletewallet")
async def balance_delete_handler(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer(f"Выберите кошелек, который вы хотите удалить:", reply_markup=make_wallet_keyboard(), parse_mode='Markdown')
    await state.set_state(DeleteWallet.id_wallet)


@router_wallet.callback_query(DeleteWallet.id_wallet)
async def wallets_delete(callback: CallbackQuery, state: FSMContext):
    code = delete_wallet(callback.data)
    await state.clear()
    if (code == '204'):
        await callback.message.answer("Кошелёк удален!")
    else:
        await callback.message.answer("Что-то пошло не так!")


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

    response = create_wallet({"wallet_name": message.text, "wallet_address": user_data['inputed_wallet_address']})
    if response.status_code == 400:
        if response.text == "\"Wallet doesn't exist\"":
            await message.answer(WALLET_DOESNT_EXIST)
            await message.answer("Введите адресс кошелька, который хотите добавить: ")
            await state.clear()
            await state.set_state(Wallet.wallet_address)
        else:
            await message.answer(WALLET_WRONG)
            await message.answer("Введите адресс кошелька, который хотите добавить: ")
            await state.clear()
            await state.set_state(Wallet.wallet_address)
    else:
        await message.answer(
            text=f"Вы добавили кошелек с названием <b>{message.text}</b> и адресом <b>{user_data['inputed_wallet_address']}</b>. ", 
            parse_mode="HTML"
        )
        await state.clear()
