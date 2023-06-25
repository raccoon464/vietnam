from django.shortcuts import render

# Create your views here.
import time

from django.db import connection, reset_queries
from django.http import HttpResponse
from django.utils.translation import gettext as _, activate
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from t_bot.config.main import API
from t_bot.controllers import Menu, InlineBtnController, MessageController, StartBotController
from t_bot.modules import Users, Language

@csrf_exempt
def bot(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        API.bot.process_new_updates([update])

    return HttpResponse("vietnam bot")


@API.bot.message_handler(commands=['start', 'home'])
def send_welcome(message):
    u = Users.validate_user(message)
    Menu.appMenu(message, u)

@API.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.message:
        InlineBtnController.callData(call, call.message.chat.id)