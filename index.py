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
        if user_exist == True:
            print("User already exists in db.")
            bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help", reply_markup=alice_vars.keyboard_default)
        else:
            print("Adding",f_name,"to db.")
            sql_functions.add_user(alice_vars.db_name, 'Users', chat_id, name)
            bot.send_message(chat_id, "It appears you are new here. send /help to get help.", reply_markup=alice_vars.keyboard_default)


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
        bot.send_message(chat_id, alicevars.helpmsg_default+alice_vars.helpmsg_feedback, reply_markup=keyboard_default)

@bot.message_handler(commands = ['addadmin'])
def addadmin(message):
    chat_id = message.chat.id
    if chat_id in alice_vars.superuser:
        msg = bot.reply_to(message, "What's the ID you want to add to Admins?")
        bot.register_next_step_handler(msg, bot_functions.add_admin)


@bot.message_handler(commands = ['addreminder'])
def addremind(message):
    chat_id = message.chat.id
    user_exist = sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id)
    if user_exist == False:
        bot.send_message(chat_id, "Oops! You're not a bot Admin. This incident will be reported.", markup=alice_vars.keyboard_default)
        print(message.from_user.first_name, "thinks he's an admin.")
    else:
        print("Adding new reminder.")

@bot.message_handler(commands = ['feedback'])
def sendfeedback(message):
    chat_id = message.chat.id
    with open("feedback.txt",'a+') as feedback_file:
        if chat_id == alice_vars.superuser:
           feedback_file.read()
        else:
           feedback_text = input("You were saying?")
           feedback_file.write(chat_id + " said " + feedback_text)


bot.polling(none_stop=True)
