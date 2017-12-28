import sqlite3
import sql_functions
import alice_vars

def add_admin(message):
    try:
        admin_id = int(message.text)
        print(admin_id, "will be added to admins.")
        if isinstance(admin_id, int):
            sql_functions.add_admin(alice_vars.db_name, 'Admins', admin_id)
            alice_vars.bot.send_message(message.chat.id, str(admin_id)+" added to Admins.", markup=alice_vars.keyboard_admin)
        else:
            raise Exception()
    except Exception as e:
        alice_vars.bot.send_message(message.chat.id, "oops! something went wrong. try again.", markup=alice_vars.keyboard_admin)
