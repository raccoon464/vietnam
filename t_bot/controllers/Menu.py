from django.utils.translation import gettext as _
from telebot import types

from t_bot.modules import  File_id, Language
from t_bot.config.main import API, Contacts
from t_bot.modules import Coingeco

NAME_BUTTON_MENU = "⚡ " + _("Главная")  # "⋮☰"
NAME_BUTTON_BACK = "🔙"
NAME_BUTTON_CANCEL = "✖"


def appMenu(message, u, text='', first = True):

    if u.admin.id != 1:
        text += '🔰 <b>' + _("Main menu") + '</b>\n\n'
        text+=Coingeco.generate_message()
        item1 = types.InlineKeyboardButton('🔘️ ' + _("Cosmos"), callback_data='Cosmos')
        item2 = types.InlineKeyboardButton('🔘️ ' + _("Tezos"), callback_data='Tezos')
        inline_markup = types.InlineKeyboardMarkup(row_width=2)
        inline_markup.add(item1, item2)
        if first:
            API.bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=inline_markup, disable_web_page_preview=True)
        else:
            API.bot.delete_message(message.chat.id, message_id=message.message_id)
            API.bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=inline_markup, disable_web_page_preview=True)
    else:
        text += '❌ <b>' + _("No access") + '</b>\n\n'
        text += '<code>' + _("Write to ") +Contacts.admin +'</code>\n\n'
        API.bot.send_message(message.chat.id, text, parse_mode='html')





def markupKeyButtonMenu():  # Кнопка Меню
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(NAME_BUTTON_MENU))
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(types.KeyboardButton(NAME_BUTTON_MENU))
    # return markup

def markupKeyButtonCancel():  # Кнопка Отмена
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(NAME_BUTTON_CANCEL))  # types.KeyboardButton(NAME_BUTTON_MENU)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(types.KeyboardButton(NAME_BUTTON_CANCEL))
    # return markup

def markupKeyButtonConfirm():  # Кнопка Отмена+Подтвердить
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(NAME_BUTTON_CANCEL), types.KeyboardButton("✔️"))

def inlineButtonMenu(markup, callback_data=''):  # Кнопки inline меню
    mMenu = types.InlineKeyboardButton("⚡ " + _("Главная"), callback_data='appMenu')
    if callback_data:
        mBack = types.InlineKeyboardButton(NAME_BUTTON_BACK, callback_data=callback_data)
        markup.add(mBack, mMenu)
    else:
        markup.add(types.InlineKeyboardButton(NAME_BUTTON_BACK, callback_data=callback_data))
    return markup

def inlineButtonMenuBack(markup, callback_data='appMenu'):  # Кнопки inline меню
    markup.add(types.InlineKeyboardButton(NAME_BUTTON_BACK, callback_data=callback_data))
    return markup


def deleteInlineButton(message):  # Удаление инлайн кнопок
    try:
        API.bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id, reply_markup='')
    except: pass

