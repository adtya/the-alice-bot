import telebot
import sql_functions
import urllib.request
import alice_vars
from alice_vars import bot
import bot_functions
import easter_eggs

for table in alice_vars.tables.keys():
    sql_functions.create_table(alice_vars.db_name, table, alice_vars.tables[table])


@bot.message_handler(commands = ['start']) # Reply to /start command
def welcome(message):
    chat_type = message.chat.type
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    name = f_name+" "+l_name

    if chat_type == "private":
        print(f_name,"with id",chat_id,"is a user.")
        user_exist = sql_functions.check_user(alice_vars.db_name, 'Users', chat_id)
        admin_exist = sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id)
        if user_exist == True:
            print("User already exists in db.")
            if admin_exist == True:
                bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help", reply_markup=alice_vars.keyboard_admin)
            else:
                bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help", reply_markup=alice_vars.keyboard_default)
        else:
            print("Adding",f_name,"to db.")
            msg = bot.send_message(chat_id, "Hi, "+f_name+" May I know your class?", reply_markup=alice_vars.keyboard_classes)
            bot.register_next_step_handler(msg, bot_functions.add_user)


    elif (chat_type == "group") | (chat_type == "supergroup"):
        print(chat_id,"is a group\n")
        bot.send_message(chat_id, 'This is a group, and I hate crowd. PM me for a better bot experience.')

# This launches kitties into orbit.
@bot.message_handler(commands = ['cat']) # Reply to /cat command (#EASTEREGG)
def cat(message):
    easter_eggs.cat(message)

# how about some motivation?
@bot.message_handler(commands = ['quote'])
def quote(message):
    easter_eggs.quote(message)

# wanna know your telegram ID?
@bot.message_handler(commands = ['whatsmytelegramid'])
def telegramid(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"asked for telegram ID.\n")
    bot.send_message(chat_id, chat_id, reply_markup=alice_vars.keyboard_default)

@bot.message_handler(commands = ['help'])
def helper(message):
    chat_id = message.chat.id
    print("Help requested.")
    if sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id):
        bot.send_message(chat_id, alice_vars.helpmsg_default+ alice_vars.helpmsg_admin+ alice_vars.helpmsg_feedback, reply_markup=alice_vars.keyboard_admin)
    else:
        bot.send_message(chat_id, alice_vars.helpmsg_default+alice_vars.helpmsg_feedback, reply_markup=alice_vars.keyboard_default)

@bot.message_handler(commands = ['addadmin'])
def addadmin(message):
    chat_id = message.chat.id
    if chat_id in alice_vars.superuser:
        msg = bot.reply_to(message, "What's the ID you want to add to Admins?")
        bot.register_next_step_handler(msg, bot_functions.add_admin)
    else:
        bot.send_message(chat_id, "oops! you're not a superuser. Only a superuser can add new admins.")


@bot.message_handler(commands = ['addreminder'])
def addremind(message):
    chat_id = message.chat.id
    user_exist = sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id)
    if user_exist == False:
        bot.send_message(chat_id, "Oops! You're not a bot Admin.", markup=alice_vars.keyboard_default)
        print(message.from_user.first_name, "thinks he's an admin.")
    else:
        print("Adding new reminder.")

@bot.message_handler(commands = ['adddocs'])
def adddocs(message):
    chat_id = message.chat.id
    user_exist = sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id)
    if user_exist == False:
        bot.send_message(chat_id, "Oops! You're not a bot Admin.", markup=alice_vars.keyboard_default)
        print(message.from_user.first_name, "thinks he's an admin.")
    else:
        msg = bot.send_message(chat_id, "Select the Department: ", reply_markup=bot_functions.create_keyboard(alice_vars.depts))
        bot.register_next_step_handler(msg, bot_functions.docs_dept)

@bot.message_handler(commands = ['documents'])
def docs(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Select the department:", reply_markup=bot_functions.create_keyboard(alice_vars.depts))
    bot.register_next_step_handler(msg, bot_functions.dept)

@bot.message_handler(commands = ['feedback'])
def sendfeedback(message):
    chat_id = message.chat.id
    if chat_id in alice_vars.superuser:
        result = sql_functions.read_feedback(alice_vars.db_name, 'Feedback')
        if result == False:
            bot.send_message(chat_id, "No feedbacks recorded yet!", reply_markup = alice_vars.keyboard_admin)
        else:
            feedback_msg = ""
            for entry in result:
                feedback_msg = feedback_msg+"\n"+str(entry)+": "+sql_functions.feedback_fetch(alice_vars.db_name+"\n\n", 'Feedback', entry)
            bot.send_message(chat_id, feedback_msg, reply_markup = alice_vars.keyboard_admin)
    else:
        msg = bot.send_message(chat_id, "So, What do you think about me ?")
        bot.register_next_step_handler(msg, bot_functions.feedback)




bot.polling(none_stop=True)
