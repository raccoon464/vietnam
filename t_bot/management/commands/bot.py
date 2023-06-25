from django.core.management.base import BaseCommand
from django.conf import settings

from var_dump import var_dump


# telegram.conf
from telebot import types
from t_bot.config.main import API
from t_bot.controllers import Menu, InlineBtnController, MessageController
from t_bot.modules import Users

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner



@log_errors
def do_echo():
    @API.bot.message_handler(commands=['start', 'home'])
    def send_welcome(message):
        pass
        # API.bot.reply_to(message, "Howdy, how are you doing?")
        # u = Users.validate_user(message)
        # Menu.appMenu(message, u)

        # Если нажата Inline-кнопка

    @API.bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):

        if call.message:
            InlineBtnController.callData(call, call.message.chat.id)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        API.bot.remove_webhook()
        do_echo()
        API.bot.polling()

