import telebot
import functions


if __name__ == "__main__":
    db_name = "alice.db"
    sql = """create table Responses(
            ID integer,
            Name text,
            desc text,
            primary key(ID))"""
    functions.create_table(db_name, 'Responses', sql)

    bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms') # Bot Token, obtained from @botfather

    @bot.message_handler(commands = ['start']) # Reply to /start command
    def welcome(message):
        bot.send_message(message.chat.id, "Hello, How can I help?")

    bot.polling(none_stop=True)
