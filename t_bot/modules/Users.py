from t_bot.config.main import API
from telebot import types
from t_bot.models import User, Admin_rule, Lang

from decimal import Decimal
from var_dump import var_dump



def validate_user(message, lang_code = ''):
    # print(extract_unique_code(message.text))
    try:
        # если  зарегистирован
        return User.objects.get(telegram_id=message.chat.id)
    except:
        # если пользователь не зарегистирован
        # partner_id = get_user_id(extract_unique_code(message.text))
        # lang = get_user_lang(message.from_user.language_code)
        username = get_username(message)
        if lang_code == '':
            lang = get_user_lang(message.from_user.language_code)
        else:
            lang = get_user_lang(lang_code)


        u = User.objects.create(
            telegram_id=message.chat.id,
            name=username,
            lang = lang,
            admin = Admin_rule.objects.get(id=1),
            description= 'usual user'
        )
        return u

def save_number(id, number):
    u = User.objects.get(telegram_id=int(id))
    u.phone = number
    return u.save()

def find_user_t_id(id):
    try:
        return User.objects.get(telegram_id=int(id))
    except:
        return False

def find_user_id(id):
    try:
        return User.objects.get(id=int(id))
    except:
        return False


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def get_user_id(unique_code):
    try:
        return User.objects.get(telegram_id=unique_code)
    except:
        return User.objects.get(id=1)


def get_user_lang(lang):
     try:
         return Lang.objects.get(flag=lang)
     except:
         return Lang.objects.get(flag='en')

def get_username(message):
    if(message.from_user.username == None):
        return message.from_user.id
    else:
        return message.from_user.username


def process_balance_minus(u, amount):
    if is_number(amount):
        if u.process_balance - Decimal(amount) >= 0 and float(amount) > 0:
            u.process_balance -= Decimal(amount)
            u.save()
            return True
        else:
            return False

def mill_balance_minus(u, amount):
    if is_number(amount):
        if u.mill_balance - Decimal(amount) >= 0 and float(amount) > 0:
            u.mill_balance -= Decimal(amount)
            u.save()
            return True
        else:
            return False

def mill_balance_plus(u, amount):
    u.mill_balance += Decimal(amount)
    u.save()
    return True

def work_balance_minus(u, amount):
    if is_number(amount):
        if u.work_balance - Decimal(amount) >= 0 and float(amount) > 0:
            u.work_balance -= Decimal(amount)
            u.save()
            return True
        else:
            return False

def work_balance_plus(u, amount):
    u.work_balance += Decimal(amount)
    u.save()
    return True



def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def validate_amount(amount):
    try:
        if float(amount) > 0:
            return True
        else:
            return False
    except:
        return False


def message_new_ref(chat, user):
    i = 1
    while i<=10:
        # var_dump(chat)chat
        try:
            Language.validate_lang(chat)
            API.bot.send_message(chat, "👔  "+ _("У вас появился новый реферал") + " <b> " + str(i)+ " " + _("уровня")+"</b> - @" + str(user), parse_mode='html')
            chat = User.objects.get(id=User.objects.get(telegram_id=chat).partner.id).telegram_id
        except:
            pass

        i+=1


def find_one_telegram(data):
    try:
        return User.objects.get(telegram_id=int(data))
    except:
        return False


def ref_program(user_id, user_status):
    res = (Ref_line.objects.filter(status_id=user_status))
    text = ''
    i=0
    ref = [list(User.objects.filter(partner=user_id))]

    for a in res:

        try:
            count = 0
            for item in ref[i]:
                count += 1
                try:
                    ref[i+1] += list(User.objects.filter(partner=item.id))
                except:
                    ref += [list(User.objects.filter(partner=item.id))]
            i+=1
        except:
            count = 0

        if count == 1: n = _("партнёр")
        else: n = _("партнёров")

        text += str(a.line) + ' '+_('линия')+' - <b>' + str(count) + ' '+_(n)+' </b> (' + str(float("{0:.2f}".format(a.percent * 100))) + "% )\n"

    return text

def search_sponsor(last_message, user, message):
    Messages.exchange_status(last_message.id, 0)

    u_sponsor = find_one_telegram(message.text)
    if u_sponsor and u_sponsor.telegram_id != message.chat.id:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('✅ ' + _('Продолжить'), callback_data='validate_sponsor_' + message.text)
        btn2 = types.InlineKeyboardButton('❌ ' + _('Отмена'), callback_data='cancellation')
        markup.add(btn1)
        markup.add(btn2)
        API.bot.send_message(message.chat.id, _('Подтвердите действие! Вы назначаете себе спонсора:')+"<b> " + str(u_sponsor.name) + " ?</b>", parse_mode='html', reply_markup=markup)

    else:
        API.bot.send_message(message.chat.id, '<b>'+_("Пользователь не найден")+ '</b>', parse_mode='html')


def change_sponsor(chat, t_id):
    u = User.objects.get(telegram_id=chat)
    u.partner = User.objects.get(telegram_id=t_id)
    u.save()
    message_new_ref(t_id, chat)
    API.bot.send_message(chat, '\u25B6 ' + _('Операция была успешно выполнена!'), parse_mode='html').send_message(message.chat.id, '✅ ' + _('Operation was completed successfully!') + "\nВаш логин обновлён в боте: <b>" + message.from_user.username + "</b>", parse_mode='html')