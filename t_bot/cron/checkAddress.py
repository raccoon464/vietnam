from t_bot.models import Address, Transaction
from t_bot.modules import MP_explorer, Helper, Language
from var_dump import var_dump
from t_bot.config.main import API
from django.utils.translation import gettext as _

def updateTransaction(address, last_id, new_id, name):
    t = Transaction.objects.get(address=address, id_t=last_id, name=name)
    t.id_t = new_id
    t.save()


def checkSource():
    address = list(Address.objects.all())
    for i in address:
        Language.validate_lang(i.profile.telegram_id)
        t = MP_explorer.transaction(source=i.address)
        last_id = Transaction.objects.get(address=i, name='source')
        if last_id.id_t != t['_id'] and t['type'] != "delegation":
            if t['type'] == 'plex':
                cur = "PLEX"
            else: cur = "MINE"
            try:
                API.bot.send_message(i.profile.telegram_id,
                                 "🔗 <a href='https://explorer.mineplex.io/operations/"+t['operationHash']+"' >"+_('Отправка')+ "</a> <b>"+Helper.newAmount(t['amount']) + cur +"</b>\n\n"
                                 "💼 <a href='https://explorer.mineplex.io/addresses/"+ t['source']+"' >" + last_id.address.name + "</a> →  <a href='https://explorer.mineplex.io/addresses/"+t['destination']+"' >" + t['destination'][:6]+"..."+t['destination'][32:]+"</a>\n\n"
                                 "🕑 "+  Helper.data_pars(t['createdAt']) + "\n"
                                 ,parse_mode='html')
                updateTransaction(i, last_id.id_t , t['_id'], 'source')
            except: pass

        else:
            var_dump('не  Исполняю')


def checkDestination():
    address = list(Address.objects.all())
    for i in address:
        Language.validate_lang(i.profile.telegram_id)
        t = MP_explorer.transaction(destination=i.address)
        last_t = Transaction.objects.get(address=i, name='destination')
        if last_t.id_t != t['_id']:
            if t['type'] == "plex":
                cur = "PLEX"
                if t['isReward'] == True:
                    reword(i, last_t, t, cur)
                    var_dump('Награда')
                else:
                    receive(i, last_t, t, cur)
            elif['type'] == "mine":
                cur = "MINE"
                receive(i, last_t, t, cur)

def reword(i, last_id , t, cur):
    try:
        API.bot.send_message(i.profile.telegram_id,
                             "🔗 <a href='https://explorer.mineplex.io/operations/"+t['operationHash']+"' >"+_('Награда')+ "</a> <b>"+Helper.newAmount(t['amount']) +cur+"</b>\n\n"
                             "💼 <a href='https://explorer.mineplex.io/addresses/"+ t['destination']+"' >" + last_id.address.name + "</a>\n\n"
                             "🕑 "+  Helper.data_pars(t['createdAt']) + "\n"
                             , parse_mode='html')
        updateTransaction(i, last_id.id_t, t['_id'] , 'destination')
    except:pass

def receive(i, last_id , t, cur):
    try:
        API.bot.send_message(i.profile.telegram_id,
                             "🔗 <a href='https://explorer.mineplex.io/operations/" + t['operationHash'] + "' >" +_('Получение') + "</a> <b>" + Helper.newAmount(t['amount']) +cur+ "</b>\n\n"
                             "💼 <a href='https://explorer.mineplex.io/addresses/"+t['source']+"' >" + t['source'][:6]+"..."+t['source'][32:]+"</a> → <a href='https://explorer.mineplex.io/addresses/" +t['destination'] + "' >" + last_id.address.name + "</a>\n\n"
                             "🕑 " + Helper.data_pars(t['createdAt']) + "\n"
                             , parse_mode='html')
        updateTransaction(i, last_id.id_t, t['_id'], 'destination')
    except: pass