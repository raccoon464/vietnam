import datetime

def data_pars(data):
    d1 = datetime.strptime(data,"%Y-%m-%dT%H:%M:%S.%fZ")
    new_format = "%Y-%m-%d (%H:%M)"

    return d1.strftime(new_format)

def data_pars_xfi(data):
    d1 = datetime.strptime(data,"%Y-%m-%dT%H:%M:%SZ")
    new_format = "%Y-%m-%d (%H:%M)"

    return d1.strftime(new_format)

def amount(data):
    try:
        n = str(data)
        dot = n.index('.')
        return float(f'{n[:dot]}{n[dot:len(n[:dot]) + 4]}')
    except:
        return str(float("{0:.5f}".format(data)))

def amount_two(data):
   try:
       n = str(data)
       dot = n.index('.')
       return str(float(f'{n[:dot]}{n[dot:len(n[:dot]) + 3]}'))
   except:
       return str(float("{0:.3f}".format(data)))



def newAmount(data):
    return str(f'{int(data):,} ')

def amount_four(data):
   try:
       n = str(data)
       dot = n.index('.')
       return float(f'{n[:dot]}{n[dot:len(n[:dot]) + 5]}')
   except:
       return str(float("{0:.5f}".format(data)))

def amount_rounding(data):
    if data >= 10000:
        return int(data)
    elif data >= 100:
        return float("{0:.1f}".format(data))
    elif data >= 1:
        return float("{0:.3f}".format(data))
    elif data >= 0.01:
        return float("{0:.4f}".format(data))
    elif data >= 0.001:
        # return float("{0:.5f}".format(data))
        return format(data, '.5f')
    elif data >= 0.00001:
        return format(data, '.6f')
    elif data >= 0.00000001:
        return format(data, '.8f')
    elif data >= 0.000000000001:
        return format(data, '.12f')
    else:
        # return format(data, '.18f')
        return float("{0:.2f}".format(data))


# from django.utils.translation import gettext as _
from datetime import datetime, timezone

from telebot import types


def replace_tag(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")  #


def t_log(bot, text='', send_admin=False):
    print('  >', text)
    try:
        if send_admin:
            bot.send_message(T_ADMIN, ' 🆘  ' + text, parse_mode='html')
    except Exception as e: print('   !!error helper.t_log(e): ', e)


def technical_works_message(chat_id, bot):
    try:
        bot.send_message(chat_id,
                         "🚧  Attention, technical work is underway in the project!\nTry to come back later.\n"
                         "🚧  Внимание, в проекте ведутся технические работы!\nПопробуйте зайти позднее.",
                         # "🚧  " + _('Внимание, в проекте ведутся технические работы') + '!\n' + _('Попробуйте зайти позднее') + '.',
                         parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
    except: pass


def title_bot(text):
    return ' <b>-<u>' + text + '</u>-</b>\n\n'


def date_time():
    return "-------\n<pre>in " + datetime.now(timezone.utc).strftime("%Y/%m/%d %H:%M") + "(+0)</pre>"


def delta_hour(date_start, date_end):
    delta = date_end - date_start
    return (delta.days * 24) + (delta.seconds / 3600)


def validate_amount(data):
    try:  # Валидность суммы
        data = float(str(data).replace(',', '.').replace(' ', '').replace(' ', ''))
        if data > 0:
            return data
    except: pass
    return False


def amount(data):
    try:
        if data == 0 or data is None:
            return '0.0'
        elif data < 0.000001:
            return format(data, '.8f')  # Вывод 8 символов после точки
        n = str(data)
        dot = n.index('.')
        if data >= 1000 or data < 0:
            return '{0:,}'.format(float(f'{n[:dot]}{n[dot:len(n[:dot]) + 6]}')).replace(',', ' ')  # Вывод 5 символов после точки
        # elif data >= 10:
        #     return str(float(f'{n[:dot]}{n[dot:len(n[:dot]) + 6]}'))  # Вывод 5 символов после точки
        elif data >= 0.0001:
            return str(float(f'{n[:dot]}{n[dot:len(n[:dot]) + 7]}'))  # Вывод 6 символов после точки
        elif data >= 0.00001:
            return f'{n[:dot]}{n[dot:len(n[:dot]) + 7]}'  # Вывод 6 символов после точки
        elif data >= 0.000001:
            return f'{n[:dot]}{n[dot:len(n[:dot]) + 9]}'  # Вывод 8 символов после точки
        else:
            return '0.00'
    except:
        try:
            return '{0:,.2f}'.format(data)  # Вывод 2 символов после точки
        except:
            # except Exception as e:
            #     print('   !! err amount', e)
            return '0'


def amount_8(data):
    try:
        if data == 0:
            return '0.0'
        elif data < 0.0001:
            return '{0:,.9f}'.format(data)
            # return format(data, '.8f')  # Вывод 8 символов после точки
        elif data >= 1000:
            return '{0:,}'.format(float(data)).replace(',', ' ')  # замена разделения тысяч на неразрывный пробел &#160;
        else:
            return str(float(data))
    except:
        try:
            return str('{0:,.2f}'.format(data))  # Вывод 2 символов после точки
        except:
            # except Exception as e:
            #     print('   !! err amount', e)
            return '0'


def build_menu_buttons_cols(buttons,
                            n_cols,
                            header_buttons=None,
                            footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu



def amount_mpx(data, six = False):

    data = float(data)/1000000000000000000
    if data > 100:
        return newAmount(data)
    elif data < 10 and six:
        return str(float("{0:.7f}".format(data)))
    else:
        return amount_two(data)




def create_amount_mpx(data):
    data = data * 1000000000000000000
    return data