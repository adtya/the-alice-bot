import telebot
import sql_functions


db_name = "alice.db"
sql = """create table Users(
        ID integer,
        Name text,
        primary key(ID))"""
sql_functions.create_table(db_name, 'Users', sql)


bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather


@bot.message_handler(commands = ['start','hello']) # Reply to /start or /hello command
def welcome(message):
    chat_type = message.chat.type
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    name = f_name+" "+l_name

    if chat_type == "private":
        print(f_name,"with id",chat_id,"is a user.")
        user_exist = sql_functions.check_user(db_name, 'Users', chat_id)
        if user_exist == True:
            print("User already exists in db.")
            bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help")
        else:
            print("Adding",f_name,"to db.")
            sql_functions.add_user(db_name, 'Users', chat_id, name)
            bot.send_message(chat_id, "It appears you are new here. send /help to get help.")

    elif (chat_type == "group") | (chat_type == "supergroup"):
        print(chat_id,"is a group\n")
        bot.send_message(chat_id, 'This is a group, and I hate crowd. PM me for a better bot experience.')

    # keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.row('\U0001F4D7 Documents', '\U0001F4D7 Reminders')
    # keyboard.row('\U0001F4D7 Today\'s Schedule', '\U0001F4D7 Attendance')
    # bot.send_message(chat_id, 'Hello, What can I help you with?', reply_markup=keyboard)
    # print("welcome message send to",f_name)

bot.polling(none_stop=True)
