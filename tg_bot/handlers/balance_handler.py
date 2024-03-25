from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from utils import balance_list, create_balance, delete_balance
from states import Balance, DeleteBalance
from text import NO_BALANCE, BALANCE_LIST, ADD_BALANCE_MESSAGE, BALANCE_WRONG
from kb import make_wallet_keyboard, make_network_keyboard, make_token_keyboard

router_balance = Router()

@router_balance.message(Command("tokens"))
async def balance_handler(msg: Message):
    balances = balance_list()
    if len(balances) == 0:
        await msg.answer(NO_BALANCE)
    else:
        answer = BALANCE_LIST
        for indx in range(len(balances)):
            name = balances[indx]['asset']
            wallet = balances[indx]['wallet_name']
            network = balances[indx]['network_name']
            balance = balances[indx]['balance']
            price = balances[indx]['price']
            value = balance * price

            start_time = datetime.strptime(balances[indx]['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
            current_time = datetime.now()
            time_difference = current_time - start_time

            answer += f"*Кошелёк*: *{wallet}*\n\
*Токен*: *{name}*\n\
    - Количество: *{round(balance, 2)} {name}*\n\
    - Цена: *${round(price, 4)}* за 1 {name}\n\
    - Сумма: *${round(value, 2)}*\n\
    - Сеть: *{network}*\n\
    - Обновлено: *{time_difference}*\n"

        answer += ADD_BALANCE_MESSAGE
        await msg.answer(text=answer, parse_mode='Markdown')



@router_balance.callback_query(F.data =="tokens")
async def balance_handler(callback: CallbackQuery):
    balances = balance_list()
    if len(balances) == 0:
        await callback.message.answer(NO_BALANCE)
    else:
        answer = BALANCE_LIST + '\n'
        for indx in range(len(balances)):
            name = balances[indx]['asset']
            wallet = balances[indx]['wallet_name']
            network = balances[indx]['network_name']
            balance = balances[indx]['balance']
            price = balances[indx]['price']
            value = balance * price

            start_time = datetime.strptime(balances[indx]['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
            current_time = datetime.now()
            time_difference = current_time - start_time

            answer += f"*Кошелёк*: *{wallet}*\n\
*Токен*: *{name}*\n\
    - Количество: *{round(balance, 2)} {name}*\n\
    - Цена: *${round(price, 4)}* за 1 {name}\n\
    - Сумма: *${round(value, 2)}*\n\
    - Сеть: *{network}*\n\
    - Обновлено: *{time_difference}*\n\n"
        
        answer += ADD_BALANCE_MESSAGE
        await callback.message.answer(text=answer, parse_mode='Markdown')



@router_balance.message(StateFilter(None), Command("addtoken"))
async def add_balance(message: Message, state: FSMContext):
    await message.answer("Введите *адресс токена*, который хотите добавить или /cancel, если захотите прекратить: ", parse_mode='Markdown')
    await state.set_state(Balance.asset_address)

@router_balance.callback_query(F.data =="addtoken")
async def add_balance(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите *адресс токена*, который хотите добавить или /cancel, если захотите прекратить: ", parse_mode='Markdown')
    await state.set_state(Balance.asset_address)


@router_balance.message(Balance.asset_address, Command("cancel"))
async def cancel_balance(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание прекращено!")

@router_balance.message(Balance.wallet, Command("cancel"))
async def cancel_balance(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание прекращено!")

@router_balance.message(Balance.network, F.text == "cancel")
async def cancel_balance(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание прекращено!")


@router_balance.message(Balance.asset_address, F.text)
async def add_balance_address(message: Message, state: FSMContext):
    await state.update_data(asset_address=message.text)
    await message.answer(f"Теперь выберите *кошелёк*", reply_markup=make_wallet_keyboard(), parse_mode='Markdown')
    await state.set_state(Balance.wallet)

@router_balance.callback_query(Balance.wallet)
async def add_balance_network(callback: CallbackQuery, state: FSMContext):
    await state.update_data(wallet=callback.data)
    await callback.message.answer(f"Теперь выберите *сеть* для этого токена", reply_markup=make_network_keyboard(), parse_mode='Markdown')
    await state.set_state(Balance.network)

@router_balance.callback_query(Balance.network)
async def add_balance_serve(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    response = create_balance({
        "network_id": callback.data, 
        "wallet_id": user_data['wallet'],
        "asset_address": user_data['asset_address']
    })

    print(response.status_code)
    if response.status_code == 201:
        await callback.message.answer(
            text=f"Вы добавили токен с адресом <b>{user_data['asset_address']}</b>. ", 
            parse_mode="HTML"
        )
        await state.clear()
    else:
        await callback.message.answer(BALANCE_WRONG)
        await callback.message.answer("Введите адресс токена, который хотите добавить: ")
        await state.clear()
        await state.set_state(Balance.asset_address)
    


@router_balance.message(Command("deletetoken"))
async def balance_delete_handler(message: Message, state: FSMContext):
    await message.answer(f"Выберите токен, который вы хотите удалить:", reply_markup=make_token_keyboard(), parse_mode='Markdown')
    await state.set_state(DeleteBalance.id_balance)

@router_balance.callback_query(F.data == "deletetoken")
async def balance_delete_handler(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer(f"Выберите токен, который вы хотите удалить:", reply_markup=make_token_keyboard(), parse_mode='Markdown')
    await state.set_state(DeleteBalance.id_balance)


@router_balance.callback_query(DeleteBalance.id_balance)
async def balance_delete(callback: CallbackQuery, state: FSMContext):
    code = delete_balance(callback.data)
    await state.clear()
    if (code == '204' or code == 204):
        await callback.message.answer("Удаление завершено!")
    else:
        await callback.message.answer("Что-то пошло не так!")