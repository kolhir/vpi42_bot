# -*- coding: utf-8 -*-
from telebot import types
token = 'your token here'
admins=('admin','another admin')
alive_message="kill me please "
def getadmins():
	return(admins)

def i_am_alive(bot):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="alive button", callback_data="alive data")
    keyboard.add(callback_button)
    for admin in admins: bot.send_message(admin, alive_message, parse_mode='MARKDOWN',reply_markup=keyboard)
