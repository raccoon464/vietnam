from datetime import datetime, timezone
import math

from django.db.models import Q
from django.utils.translation import gettext as _
from telebot import types

from t_bot.modules import Helper, Coingeco
from t_bot.modules import MP_explorer, File_id, Language, XFI_explorer
from t_bot.controllers import Menu,  MessageController
from t_bot.config.main import API
from t_bot.modules.telegrambotpagination import InlineKeyboardPaginator, InlineKeyboardButton, InlineKeyboardButtonUrl
from var_dump import var_dump
from t_bot.models import User


def tezos(message, address):

    text = "🔖 <b>"+_('Validator <code>(MinePlex blockchain)</code>') + "</b>\n\n"
    text += "🔗 <a href='https://explorer.mineplex.io/mp/addresses/"+ address+"'>" + address[:10]+"....."+address[30:]+"</a>\n\n"
    data = MP_explorer.address(address)
    text += '⛓ <b>Node</b>\n'
    text += '├ '+_('General stake')+': <b>'+ Helper.newAmount(data['mineStakingBalance'])+ 'MINE</b>\n'
    text += '├ '+_('Mine Frozen Balance')+': <b>'+ Helper.newAmount(data['mineFrozenBalance'])+ '</b>\n'
    text += '└ '+_('Plex Frozen Balance') + ': <b>' + Helper.newAmount(data['plexFrozenBalance']) + '</b>\n\n'

    plex_price = Coingeco.price('plex')
    text += '🏦 <b>' + _('Wallet') + '</b>:\n'
    text += '├ PLEX: <b>' + Helper.newAmount(data['plexBalance']) + ' </b><code>| $'+Helper.newAmount(plex_price*data['plexBalance'])+' </code>\n'
    text += '└ MINE: <b>' + Helper.newAmount(data['mineBalance']) + ' </b> <code>| $'+Helper.newAmount(data['mineBalance']*(plex_price/MP_explorer.pricePlexForOneMine()))+'</code>\n'


    markup = types.InlineKeyboardMarkup(row_width=2)
    markup = Menu.inlineButtonMenuBack(markup)

    API.bot.delete_message(message.chat.id, message_id=message.message_id)
    API.bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)



def cosmos(message, address):
    text = "🔖 <b>"+_('Validator <code>(XFI blockchain)</code>') + "</b>\n\n"
    text += XFI_explorer.validator_info(address)

    u = User.objects.get(telegram_id=message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    if u.admin.id == 3:
        markup.add(types.InlineKeyboardButton('📤 ' + _('Claim'), callback_data='Claim'))
    markup = Menu.inlineButtonMenuBack(markup)

    API.bot.delete_message(message.chat.id, message_id=message.message_id)
    API.bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)
