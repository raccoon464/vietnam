from django.utils.translation import gettext as _, activate
from t_bot.config.main import API
from t_bot.controllers import Menu, InlineBtnController, AppController
from var_dump import var_dump

def reset_message(user, flag_mess=False, delete_markup=True):
    text = ''

    if flag_mess and text:
        try:
            API.bot.send_message(user.telegram_id, text, reply_markup=Menu.markupKeyButtonMenu())
            text = ''
        except Exception as e: print('  !! ERR (reset_message-1)', e)

    if delete_markup:
        try:
            API.bot.edit_message_reply_markup(user.telegram_id, message_id=mess[0].message_id, reply_markup='')
        except Exception as e: print('  !! ERR (reset_message-2)', e)

    return text


def invalid_request(message, user):
    try: API.bot.delete_message(message.chat.id, message_id=message.message_id)
    except: pass
    # Messages.reset_message(user)
    Helper.t_log(API.bot, str(user) + '  ::  !!(invalid_request) ')


def popupMessage(call_id, popup_mess=_("Загрузка...")):
    try:
        API.bot.answer_callback_query(callback_query_id=call_id, show_alert=False, text=popup_mess)
    except Exception as e: print('   !!ERR  popupMessage(e): ', e)


def messLoading(message, text_mess='♻  <b>' + _('Loading, please wait') + '...</b>'):
    try:
        API.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text_mess,
            parse_mode='html',
            reply_markup=''
        )
    except: pass



def foundMessage(message, user):
    last_m = Messages.last_message(user)

    if last_m != False:
        var_dump(last_m.message_text[:15])
        if last_m.message_text == 'addAddress' and last_m.status == 1:
            if last_m.options == Messages.DEFAULT_OPTION:
                Messages.exchange_options(last_m.id, message.text)
                API.bot.send_message(user.telegram_id, "🔖️" +_("Введите адрес"))
            else:
                Messages.exchange_status(last_m, 0)
                Address.addNweAddress(message, user, last_m.options, message.text)


        elif last_m.message_text[:15] == "editNameAddress":
            Address.editAddressName(user, last_m.message_text[15:], message.text)
            Messages.exchange_status(last_m, 0)


    else:API.bot.send_message(user.telegram_id, "❌" + _("Команда не найдена"))