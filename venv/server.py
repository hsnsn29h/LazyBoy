import logging
from random import randrange
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_markdown

from bot_database import BotDatabase
from constants import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

db = BotDatabase('database.db')


def start_command(update, context):
    message = 'Hello World!. \
Everyone type  /in  so i can register you in the system.\
 After that you can use  /all  to mention everyone.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def in_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or 'anonymous'
    db.add_user(user.id, user_name)
    db.add_user_to_chat(chat_id, user.id)
    case = randrange(11)
    if case == 0:
        message = f'I do what I must, You are in {user_name}'
    else:
        if case == 1:
            message = f'Watch and learn, You are in {user_name}'
        else:
            if case == 2:
                message = f'Was that all?, You are in {user_name}'
            else:
                if case == 3:
                    message = f'Too easy, You are in {user_name}'
                else:
                    if case == 4:
                        message = f'I’ve still got it, You are in {user_name}'
                    else:
                        if case == 5:
                            message = f'I’m an army of one, You are in {user_name}'
                        else:
                            if case == 6:
                                message = f'Watch and learn, You are in {user_name}'
                            else:
                                if case == 7:
                                    message = f'You got it!, You are in {user_name}'
                                else:
                                    if case == 8:
                                        message = f'The world could always use more heroes, You are in {user_name}'
                                    else:
                                        if case == 9:
                                            message = f'I have this under control, You are in {user_name}'
                                        else:
                                            if case == 10:
                                                message = f'Expect nothing less, You are in {user_name}'


    context.bot.send_message(chat_id=chat_id, text=message)


def out_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or 'anonymous'
    db.delete_user_from_chat(chat_id, user.id)
    message = f'You\' ve been opted out {user_name}'
    context.bot.send_message(chat_id=chat_id, text=message)


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


def all_command(update, context):
    chat_id = update.effective_chat.id
    user_list = db.get_users_from_chat(chat_id)
    if not user_list:
        message = 'There are no users. To opt in type /in command'
        context.bot.send_message(chat_id=chat_id, text=message)
    else:
        user_list = [mention_markdown(user_id, unicode_truncate(user_name, 100), version=2)
                     for user_id, user_name in user_list]
        for chunk in chunks(user_list, 4):
            message = ' '.join(chunk)
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def stats_command(update, context):
    message = f'user_count: {db.count_users()[0]}\n' \
              f'chat_count: {db.count_chats()[0]}\n' \
              f'group_count: {db.count_groups()[0]}'
    context.bot.send_message(update.effective_chat.id, text=message)


def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


updater = Updater(token="1335586344:AAGz2WrM4_z1DnZXsqh5uwAH0lv5Ky8k-jw", use_context=True)
dispatcher = updater.dispatcher

in_handler = CommandHandler('in', in_command)
all_handler = CommandHandler('all', all_command)
# out_handler = CommandHandler('out', out_command)
start_handler = CommandHandler('start', start_command)
# stats_handler = CommandHandler('stats', stats_command)
unknown_command = MessageHandler(Filters.command, unknown_command)

dispatcher.add_handler(in_handler)
dispatcher.add_handler(all_handler)
# dispatcher.add_handler(out_handler)
dispatcher.add_handler(start_handler)
# dispatcher.add_handler(stats_handler)
dispatcher.add_handler(unknown_command)

updater.start_polling()
updater.idle()

db.close()