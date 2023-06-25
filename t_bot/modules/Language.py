
from t_bot.modules import  Helper
from t_bot.controllers import  Menu, StartBotController
from var_dump import var_dump
from t_bot.config.main import API
from django.utils.translation import gettext as _
from django.utils.translation import activate
from telebot import types



def validate_lang(t_id):
    var_dump(User.objects.get(telegram_id=t_id).lang.flag)
    activate(User.objects.get(telegram_id=t_id).lang.flag)
    # try:
    #     activate(User.objects.get(telegram_id=t_id).lang.flag)
    # except: activate('ru')


def language_exchange(call):
    markup = types.InlineKeyboardMarkup(row_width=3)

    l = list(Lang.objects.all())
    for item in l:
        markup.add(types.InlineKeyboardButton(item.icon+ " " +item.name , callback_data='l_'+item.flag))

    # item1 = types.InlineKeyboardButton("🇺🇸 English", callback_data='l_en')
    # item2 = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='l_ru')
    # item3 = types.InlineKeyboardButton("🇻🇳 Vietnam", callback_data='l_vn')


    markup = Menu.inlineButtonMenu(markup, 'settings')
    try:
        API.bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        API.bot.send_message(call.message.chat.id, text='🌐 ' + _('Выбери язык') + ' ', parse_mode='html', reply_markup=markup)
    except: pass

def language_exchange_only(user, flag):
    activate(flag)
    user.lang = Lang.objects.get(flag=flag)
    user.save()


def language_exchange_start(call, user, flag):
    activate(flag)
    user.lang = Lang.objects.get(flag=flag)
    user.save()
    StartBotController.start_m(call)