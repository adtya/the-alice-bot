import telebot

bot = telebot.TeleBot('501737753:AAH_xjdeSe1pUg5cEBazOAFRTaYuqZUzbms')

@bot.message_handler(commands = ['start']) // Reply to /start command
def welcome(message):
    bot.reply_to(message, "Hello, How can I help?")


bot.polling()
