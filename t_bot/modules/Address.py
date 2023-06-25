from t_bot.models import User
from t_bot.models import Address, Transaction
from t_bot.modules import MP_explorer
from datetime import datetime, timezone
from t_bot.config.main import API
from telebot import types
from django.utils.translation import gettext as _
from t_bot.controllers import AppController, Menu
from var_dump import var_dump

def protect(user, address):
    if Address.objects.filter(profile=user).count() >= 3 and int(user.admin) != 1:
        return {"err": _("Превышен допустимый лемит кошельков: 3"), "return": False}

    if address[:3] != 'mp1':
        return {"err": _("Некорректно введён кошелёк"), "return": False}

    try:
        Address.objects.get(profile=user, address=address)
        return {"err": _("Адрес уже существует"), "return": False}
    except:pass
    try:
        MP_explorer.transaction(source=address)
    except: return {"err": _("Адрес адрес является неактивным"), "return": False}


    return {"return": True}


def addNweAddress(message, user, name, address):
    res = protect(user, address)

    if res["return"] == True:
        createNewObject(user, name, address)
        API.bot.send_message(user.telegram_id, "📮 "+_('Добавлен адрес')+": <code>" + message.text + "</code> ",parse_mode='html')
        AppController.myAddress(1, user.telegram_id, user, message.text)
    else:
        API.bot.send_message(user.telegram_id, "❌ " + res["err"], parse_mode='html')

def createNewObject(user, name, address):
    a = Address.objects.create(
        profile=user,
        name=name,
        address=address,
        date=datetime.now(timezone.utc)
    )
    addNweTransactions(a)
    return a

def addNweTransactions(data):
    arr = MP_explorer.transaction(source=data.address)
    Transaction.objects.create(
        address=data,
        id_t=arr['_id'],
        name="source",
    )

    arr = MP_explorer.transaction(destination=data.address)
    Transaction.objects.create(
        address=data,
        id_t=arr['_id'],
        name="destination",
    )


def editAddress(message, chat_id,address):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('📝 ' + _("Поменять Имя"), callback_data='editNameAddress' + address))
    markup.add(types.InlineKeyboardButton('🖍 ' + _("Удалить Адрес"), callback_data='deleteAddress' + address))
    markup = Menu.inlineButtonMenuBack(markup)

    API.bot.delete_message(message.chat.id, message_id=message.message_id)
    API.bot.send_message(chat_id, "🔖 " + _("Редактирование Адреса") + ' ' + address + '\n' , parse_mode='html', reply_markup=markup )

def editAddressName(user, address, name):
    a = Address.objects.get(profile=user, address=address)
    a.name = name
    a.save()
    API.bot.send_message(user.telegram_id, "✅ " + _("Успешно") )
    AppController.myAddress(1, user.telegram_id ,user, address)


def deleteAddress(user, address):
    a = Address.objects.get(profile=user, address=address)
    Transaction.objects.filter(address=a).delete()
    a.delete()
    API.bot.send_message(user.telegram_id, "✅ " + _("Адрес") +" <b> "+ address  +"</b> "+ _("удалён"), parse_mode='html')
    AppController.address(1, user.telegram_id, user)
