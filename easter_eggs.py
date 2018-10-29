import telebot
import sql_functions
import urllib.request
import json
import alice_vars
from alice_vars import bot
import bot_functions


def cat(message):
    chat_id = message.chat.id
    if sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id):
        keyboard = alice_vars.keyboard_admin
    else:
        keyboard = alice_vars.keyboard_default
    try:
        f_name = message.from_user.first_name
        print(f_name, "requested for a kitty")
        photo = urllib.request.urlopen(
            'http://www.thecatapi.com/api/images/get')
        if chat_id < 0:
            bot.send_photo(chat_id, photo)
            print("Kitty launched.\n")
        elif chat_id > 0:
            bot.send_photo(chat_id, photo, reply_markup=keyboard)
            print("Kitty launched.\n")
    except Exception as e:
        bot.send_message(
            chat_id, "oops! something went wrong! try again.", reply_markup=keyboard)


def quote(message):
    chat_id = message.chat.id
    if sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id):
        keyboard = alice_vars.keyboard_admin
    else:
        keyboard = alice_vars.keyboard_default
    try:
        quote = urllib.request.urlopen(
            'http://quotes.rest/qod.json').read().decode('utf-8')
        quote_json = json.loads(quote)
        bot.send_message(chat_id, "Quote of the day:\n\n", quote_json['contents']['quotes'][0]
                         ['quote'], "\n", quote_json['contents']['quotes'][0]['author'], reply_markup=keyboard)
    except Exception as e:
        bot.send_message(
            chat_id, "oops! something went wrong! try again.", reply_markup=keyboard)
