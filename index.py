import telebot
import sqlite3

def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute(sql)
            db.commit();

if __name__ == "__main__":
    db_name = "alice.db"
    sql = """create table Responses(
            ID integer,
            Name text,
            desc text,
            primary key(ID))"""
    create_table(db_name, 'Responses', sql)

    bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather

    @bot.message_handler(commands = ['start']) # Reply to /start command
    def welcome(message):
        bot.send_message(chat_id, "Hello, How can I help?")

    bot.polling()
