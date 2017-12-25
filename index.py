import telebot
import sql_functions
import urllib.request


db_name = "alice.db"

sql_users = """create table Users(
        ID integer,
        Name text,
        Class text,
        Score integer,
        primary key(ID))"""

sql_docs = """create table Docs(
        ID integer,
        link text,
        Subject text,
        Module integer,
        Department text,
        primary key(ID))"""


sql_functions.create_table(db_name, 'Users', sql_users)


bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather

keyboard_private = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_private.row('/help','/catphoto','/whatsmytelegramid')
keyboard_private.row('/reminders')
keyboard_private.row('/attendance')
keyboard_private.row('/documents')


@bot.message_handler(commands = ['start']) # Reply to /start command
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
            bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help", reply_markup=keyboard_private)
        else:
            print("Adding",f_name,"to db.")
            # sql_functions.add_user(db_name, 'Users', chat_id, name)
            bot.send_message(chat_id, "It appears you are new here. send /help to get help.", reply_markup=keyboard_private)


    elif (chat_type == "group") | (chat_type == "supergroup"):
        print(chat_id,"is a group\n")
        bot.send_message(chat_id, 'This is a group, and I hate crowd. PM me for a better bot experience.')

    # bot.send_message(chat_id, 'Hello, What can I help you with?', reply_markup=keyboard)
    # print("welcome message send to",f_name)

# This launches kitties into orbit.
@bot.message_handler(commands = ['catphoto']) # Reply to /catphoto command
def cat(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"requested for a kitty")
    photo = urllib.request.urlopen('http://thecatapi.com/api/images/get').read()
    if chat_id < 0:
        bot.send_photo(chat_id, photo)
        print("Kitty launched.\n")
    elif chat_id > 0:
        bot.send_photo(chat_id, photo, reply_markup=keyboard_private)
        print("Kitty launched.\n")

@bot.message_handler(commands = ['whatsmytelegramid'])
def telegramid(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"asked for telegram ID.\n")
    bot.send_message(chat_id,chat_id, reply_markup=keyboard_private)


bot.polling(none_stop=True)
