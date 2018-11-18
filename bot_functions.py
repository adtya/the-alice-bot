import telebot
import sqlite3
import sql_functions
import alice_vars
from alice_vars import bot

adddocs = {'dept': "", 'subject': "", 'module': "", 'id': ""}
docs = {'dept': "", 'subject': "", 'module': ""}


def add_user(message):
    user_class = message.text
    chat_id = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    name = f_name+" "+l_name
    sql_functions.add_user(alice_vars.db_name, 'Users',
                           chat_id, name, user_class)
    bot.send_message(chat_id, "It appears you are new here. send /help to get help.",
                     reply_markup=alice_vars.keyboard_default)


def add_admin(message):
    try:
        admin_id = int(message.text)
        print(admin_id, "will be added to admins.")
        if isinstance(admin_id, int):
            sql_functions.add_admin(alice_vars.db_name, 'Admins', admin_id)
            bot.send_message(message.chat.id, str(
                admin_id)+" added to Admins.", reply_markup=alice_vars.keyboard_admin)
        else:
            raise Exception()
    except Exception as e:
        bot.send_message(message.chat.id, "oops! something went wrong. try again.",
                         reply_markup=alice_vars.keyboard_admin)


def feedback(message):
    chat_id = message.chat.id
    if sql_functions.check_user(alice_vars.db_name, 'Admins', chat_id):
        keyboard = alice_vars.keyboard_admin
    else:
        keyboard = alice_vars.keyboard_default
    name = message.from_user.first_name+" "+message.from_user.last_name
    text = message.text
    try:
        sql_functions.add_feedback(alice_vars.db_name, 'Feedback', name, text)
        bot.send_message(
            chat_id, "Thanks! Your feedback has been recorded", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(
            chat_id, "oops! something went wrong. Try again!", reply_markup=keyboard)

#Creates Reminders. Debug with the help of Adithya
def createReminder(message):
    bot.send_message(message.chat_id,"Enter Title of the Reminder")
    reminder_id = message.message_id
    msg=bot.send_message(message.chat_id,"Describe the Reminder")
    reminder_=description=gatherDescription(msg)
    bot.send_message(message.chat_id,"Enter Date")
    
#Wrote this function because Hari is unable to understand how to take data from a message
def gatherDescription(message):
    return message.text

def create_keyboard(items):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for item in items:
        keyboard.add(item)
    return keyboard


def docs_dept(message):
    chat_id = message.chat.id
    adddocs['dept'] = message.text
    msg = bot.send_message(chat_id, "Select a subject: ", reply_markup=create_keyboard(
        alice_vars.subjects[adddocs['dept']]))
    bot.register_next_step_handler(msg, docs_subject)


def docs_subject(message):
    adddocs['subject'] = message.text
    msg = bot.send_message(message.chat.id, "Select a module(0 to upload the syllabus)",
                           reply_markup=alice_vars.keyboard_modules)
    bot.register_next_step_handler(msg, docs_module)


def docs_module(message):
    adddocs['module'] = int(message.text)
    msg = bot.send_message(message.chat.id, "send me the document(pdf)")
    bot.register_next_step_handler(msg, docs_upload)


def docs_upload(message):
    doc_type = message.document.mime_type.split('/')[-1]
    if not (doc_type == 'pdf'):
        bot.send_message(message.chat.id, "Please send a pdf file",
                         reply_markup=alice_vars.keyboard_admin)
    else:
        adddocs['id'] = message.document.file_id
        sql_functions.add_docs(alice_vars.db_name, adddocs)
        bot.send_message(message.chat.id, "Document uploaded successfully.",
                         reply_markup=alice_vars.keyboard_admin)


def dept(message):
    docs['dept'] = message.text
    msg = bot.send_message(message.chat.id, "Select a subject:",
                           reply_markup=create_keyboard(alice_vars.subjects[docs['dept']]))
    bot.register_next_step_handler(msg, subject)


def subject(message):
    docs['subject'] = message.text
    msg = bot.send_message(message.chat.id, "Select a module(0 for syllabus)",
                           reply_markup=alice_vars.keyboard_modules)
    bot.register_next_step_handler(msg, module)


def module(message):
    if sql_functions.check_user(alice_vars.db_name, 'Admins', message.chat.id):
        keyboard = alice_vars.keyboard_admin
    else:
        keyboard = alice_vars.keyboard_default
    docs['module'] = int(message.text)
    results = sql_functions.get_docs(alice_vars.db_name, docs)
    for result in results:
        bot.send_document(message.chat.id, result, reply_markup=keyboard)
