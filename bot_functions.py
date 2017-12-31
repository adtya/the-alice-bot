import sqlite3
import sql_functions
import alice_vars
from alice_vars import bot

def add_admin(message):
    try:
        admin_id = int(message.text)
        print(admin_id, "will be added to admins.")
        if isinstance(admin_id, int):
            sql_functions.add_admin(alice_vars.db_name, 'Admins', admin_id)
            bot.send_message(message.chat.id, str(admin_id)+" added to Admins.", markup=alice_vars.keyboard_admin)
        else:
            raise Exception()
    except Exception as e:
        bot.send_message(message.chat.id, "oops! something went wrong. try again.", markup=alice_vars.keyboard_admin)

def feedback(message):
    chat_id = message.chat.id
    if sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id):
        keyboard = alice_vars.keyboard_admin
    else:
        keyboard = alice_vars.keyboard_default
    name = message.from_user.first_name+message.from_user.last_name
    text = message.text
    try:
        sql_functions.add_feedback(alice_vars.db_name, 'Feedback', name, text)
        bot.send_message(chat_id, "Thanks! Your feedback has been recorded", reply_markup = keyboard)
    except Exception as e:
        bot.send_message(chat_id, "oops! something went wrong. Try again!", reply_markup = keyboard)
