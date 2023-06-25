from t_bot.config.main import API
import telebot
from telebot import types

from django.core.management.base import BaseCommand
from var_dump import var_dump

def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


class Command(BaseCommand):
    help = 'setWebhook'

    def handle(self, *args, **options):
        var_dump(API.bot.set_webhook(url=API.url))