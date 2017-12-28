import telebot

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

tables = {'Admins': sql_admins, 'Users': sql_users, 'Docs': sql_docs, 'Reminders': sql_remind}


bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather

keyboard_default = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_default.row('/help')
keyboard_default.row('/reminders')
keyboard_default.row('/attendance')
keyboard_default.row('/documents')

superuser = 371847809
