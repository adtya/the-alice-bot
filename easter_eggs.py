import telebot
import sql_functions
import urllib.request
import json
import alice_vars
from alice_vars import bot
import bot_functions

@bot.message_handler(commands = ['cat']) # Reply to /cat command (#EASTEREGG)
def cat(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"requested for a kitty")
    photo = urllib.request.urlopen('http://www.thecatapi.com/api/images/get')
    if chat_id < 0:
        bot.send_photo(chat_id, photo)
        print("Kitty launched.\n")
    elif chat_id > 0:
        bot.send_photo(chat_id, photo, reply_markup=alice_vars.keyboard_default)
        print("Kitty launched.\n")

@bot.message_handler(commands = ['quote'])
def quote(message) :
    chat_id = message.chat.id
    quote = open("http://quotes.rest/qod.json")
    quote_json = json.loads(quote)
    print("Quote of the day " + quote_json["content"]["quotes"]["quote"])