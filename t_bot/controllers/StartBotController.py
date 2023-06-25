from django.utils.translation import gettext as _, activate
from t_bot.models import User
from telebot import types
from t_bot.config.main import API
from t_bot.modules import Users, Language

def start_reg1(message):
    try:

        markup = types.InlineKeyboardMarkup(row_width=3)

        l = list(Lang.objects.all())
        for item in l:
            markup.add(types.InlineKeyboardButton(item.icon + " " + item.name, callback_data='langStart_' + item.flag))

        # item1 = types.InlineKeyboardButton("🇺🇸 English", callback_data='l_en')
        # item2 = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='l_ru')
        # item3 = types.InlineKeyboardButton("🇻🇳 Vietnam", callback_data='l_vn')

        API.bot.send_message(message.chat.id, 'Choose a language to work with the bot  🔻',  reply_markup=markup)


    except Exception as e: print('   !! ERROR start_reg1():', e)


def start_m(message):
    Language.validate_lang(message.chat.id)
    text = "📲  <b>"+_('Блокчейн MinePlex в Telegram') +"!</b>\n\n"
    text += _('Экономь своё время, получая одним кликом структурированные данные об операциях по заданным адресам.') + '\n\n'
    text += "✅ "+ _('Канал: @InfoBot_MinePlex')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚡ "+_('Меню'))
    markup.add(item1)
    API.bot.send_photo(message.chat.id, _("MAIN"), caption=text, parse_mode='html', reply_markup=markup)


