import sqlite3
import sql_functions
import alice_vars

def get_admin_id(messasge):
    try:
        admin_id = message.text
        if admin_id.is_integer():
            sql_functions.add_admin(alice_vars.db_name, 'Admins', admin_id)
            bot.send_message(message.chat.id, admin_id+" added to Adminsself.")
        else:
            raise Exception()
    except Exception as e:
        bot.send_message(message.chat.id, "oops! something went wrong.")
