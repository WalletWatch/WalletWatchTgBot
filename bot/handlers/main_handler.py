from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from text import GREETING, INFO_COMPACT
from kb import make_kb_main

router_main = Router()

@router_main.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(GREETING)
    await msg.answer("Выберите команду:", reply_markup=make_kb_main())

@router_main.message(Command("help"))
async def help_hendler(msg: Message):
    await msg.answer(INFO_COMPACT, parse_mode='Markdown')
    await msg.answer("Выберите команду:", reply_markup=make_kb_main())

@router_main.callback_query(F.data == "help")
async def help_hendler(callback: CallbackQuery):
    await callback.message.answer(INFO_COMPACT, parse_mode='Markdown')
    await callback.message.answer("Выберите команду:", reply_markup=make_kb_main())

@router_main.callback_query(F.data == "menu")
async def help_hendler(callback: CallbackQuery):
    await callback.message.answer("Выберите команду:", reply_markup=make_kb_main())

@router_main.message(Command("menu"))
async def help_hendler(msg: Message):
    await msg.answer("Выберите команду:", reply_markup=make_kb_main())
