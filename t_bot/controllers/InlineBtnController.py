from django.utils.translation import gettext as _
from t_bot.config.main import API, Validators
from t_bot.controllers import Menu,  AppController, StartBotController
from var_dump import var_dump
from t_bot.models import User, Admin_rule, Lang
from t_bot.modules import Helper, Coingeco, Cosmos
from t_bot.modules import MP_explorer, File_id, Language, XFI_explorer
from telebot import types

def callData(call, chat_id):
    call_data = call.data.split('#')
    var_dump(call_data)

    if call_data[0] == "appMenu":
        u = User.objects.get(telegram_id=call.message.chat.id)
        Menu.appMenu(call.message, u, first=False)

    elif call_data[0] == "Cosmos":
        AppController.cosmos(call.message, Validators.cosmos )

    elif call_data[0] == "Tezos":
        AppController.tezos(call.message, Validators.tezos)

    elif call_data[0] == "Claim":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('✏️ ' + _('Confirm'), callback_data='Confirm'))
        text = "⚠ " + _('Confirm your action!') + "\n\n"
        text += "<code>" + _('Claim')+" " + Helper.amount_mpx(XFI_explorer.total_claim(), six= True) +" XFI</code>\n\n"
        API.bot.send_message( chat_id, text, parse_mode='html', reply_markup=markup)

    elif call_data[0] == "Confirm":
        try:
            amount = Helper.amount_mpx(XFI_explorer.total_claim(), six= True)
            tx = Cosmos.validator_commission(Cosmos.get_wallet(Validators.mnemo), Validators.cosmos)
            text = XFI_explorer.tx_info(tx, amount)
            API.bot.send_message(chat_id, text , parse_mode='html')
        except Exception as e:
            try:
                print('!ERR ', str(e))
                API.bot.send_message(chat_id, "<b>!ERR</b><code>"+str(e)+"</code>", parse_mode='html')
            except:
                print('!ERR ', str(e)[47:])
                API.bot.send_message(chat_id, "<b>!ERR</b><code>" + str(e)[47:] + "</code>", parse_mode='html')




    elif call_data[0] == "lock":
        API.bot.send_message( chat_id, "⚠ " + _('The section is under development'))

    else: API.bot.send_message( chat_id, "⚠ " + _('The section is under development'))
