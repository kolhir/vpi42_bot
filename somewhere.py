# -*- coding: utf-8 -*-
from telebot import types
token = '' #test4
admins=('148964502','65353297')
alive_message="...em lliK lol kek cheboureck "
def getadmins():
	return(admins)

def i_am_alive(bot):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="git gud", callback_data="test")
    keyboard.add(callback_button)
    for admin in admins: bot.send_message(admin, alive_message, parse_mode='MARKDOWN',reply_markup=keyboard)
