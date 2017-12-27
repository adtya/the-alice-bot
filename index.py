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

sql_remind = """create table Reminders(
        ID integer,
        title text,
        description text,
        class text,
        date text,
        primary key(ID))"""

sql_admins = """create table Admins(
        ID integer,
        primary key(ID))"""

sql_functions.create_table(db_name, 'Users', sql_users)
sql_functions.create_table(db_name, 'Reminders', sql_remind)
sql_functions.create_table(db_name, 'Docs', sql_docs)


bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather

keyboard_default = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_default.row('/help')
keyboard_default.row('/reminders')
keyboard_default.row('/attendance')
keyboard_default.row('/documents')


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
            bot.send_message(chat_id, "Hi, Welcome back. If you want any help, just send /help", reply_markup=keyboard_default)
        else:
            print("Adding",f_name,"to db.")
            sql_functions.add_user(db_name, 'Users', chat_id, name)
            bot.send_message(chat_id, "It appears you are new here. send /help to get help.", reply_markup=keyboard_default)


    elif (chat_type == "group") | (chat_type == "supergroup"):
        print(chat_id,"is a group\n")
        bot.send_message(chat_id, 'This is a group, and I hate crowd. PM me for a better bot experience.')



# This launches kitties into orbit.
@bot.message_handler(commands = ['cat']) # Reply to /cat command (#EASTEREGG)
def cat(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"requested for a kitty")
    photo = urllib.request.urlopen('http://thecatapi.com/api/images/get').read()
    if chat_id < 0:
        bot.send_photo(chat_id, photo)
        print("Kitty launched.\n")
    elif chat_id > 0:
        bot.send_photo(chat_id, photo, reply_markup=keyboard_default)
        print("Kitty launched.\n")

@bot.message_handler(commands = ['whatsmytelegramid'])
def telegramid(message):
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    print(f_name,"asked for telegram ID.\n")
    bot.send_message(chat_id, chat_id, reply_markup=keyboard_default)

@bot.message_handler(commands = ['help'])
def helper(message):
    chat_id = message.chat.id
    print("Help requested.")
    bot.send_message(chat_id, "You can send\n1. /reminders to get ")

@bot.message.message_handler(commands = ['addadmin'])
def addadmin(message):
    chat_id = message.chat.id
    admin_exist = sql_functions.check_user(db_name, )


@bot.message_handler(commands = ['addreminder'])
def addremind(message):
    chat_id = message.chat.id
    user_exist = sql_functions.check_user(db_name, 'Admins', chat_id)
    if user_exist == False:
        bot.send_message(chat_id, "Oops! You're not a bot Admin. This incident will be reported.", markup=keyboard_default)
        print(message.from_user.first_name, "thinks he's an admin.")
    else:
        print("Adding new reminder.")


bot.polling(none_stop=True)
