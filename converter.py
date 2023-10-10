# ----------------------------------------------- #
# Project Name          : Study bot		  #
# Author Name           : Leo Shizaki             #
# File Name             : converter.py		  #
# ----------------------------------------------- #
import telebot
from currency_converter import CurrencyConverter
from telebot import types
bot = telebot.TeleBot('') #insert your bot key
currency = CurrencyConverter()
amount = 0
# ----------------------------------------------- #
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'inter your ammount')
    bot.register_next_step_handler(message, summ)
def summ(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'try again')
        bot.register_next_step_handler(message, summ)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('usd/ils', callback_data='usd/ils')
        btn2 = types.InlineKeyboardButton('ils/usd', callback_data='ils/usd')
        btn3 = types.InlineKeyboardButton('ils/eur', callback_data='ils/eur')
        btn4 = types.InlineKeyboardButton('other', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'pick your own pair', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'should be more that zero')
        bot.register_next_step_handler(message,summ)
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'will be: {round(res, 2)}, feel free to send next')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, 'send me pair with / (like eur/usd)')
        bot.register_next_step_handler(call.message, my_currency)
def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'will be: {round(res, 2)}, feel free to cnvrt again')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send.message(message.chat.id, 'smth went wrong, try again')
        bot. register_next_step_handler(message, my_currency)
bot.polling(non_stop=True)