import requests
from t_bot.modules import Helper
from django.utils.translation import gettext as _
from datetime import datetime, timezone

from telebot import types

from t_bot.controllers import Menu

def generate_content():
    text = ''
    text += _("Текущий цикл:") +" <b>" + str(cycle()) + "</b>\n"
    text += _("Сложность сплетения:") +" <b>" + str(Helper.newAmount(complexity())) + "</b>\n"
    text += _("Всего кошельков:") +" <b>" + str(Helper.newAmount(total_wallets())) + "</b>\n\n"


    total_plex = all_plex()
    circulation = plex_in_circulation()
    free = free_plex()
    frozen = frozen_plex()

    text += "⚫️ <b>PLEX</b>\n"
    text += "├ "+_('Всего')+": <b>"+ Helper.newAmount(total_plex) + "</b>  <code>| 100% </code>\n"
    text += "├ "+_('В обороте')+": <b>"+ Helper.newAmount(circulation)+ "</b> <code>| "+Helper.amount_two(circulation/(total_plex/100))+"% </code>\n"
    text += "├ "+_('Заблокировано') + ": <b>" + Helper.newAmount(frozen) + "</b> <code>| " + Helper.amount_two(frozen / (circulation / 100)) + "% </code>\n"
    text += "└ "+_('Свободно')+": <b>"+ Helper.newAmount(free) + "</b> <code>| "+Helper.amount_two(free/(circulation/100))+"% </code>\n\n"


    total = all_mine()
    circulation = mine_in_circulation()
    free = free_mine()
    frozen = frozen_mine()

    text += "⚪️ <b>MINE</b>\n"
    text += "├ "+_('Всего')+": <b>" + Helper.newAmount(total) + "</b> <code>| 100% </code>\n"
    text += "├ "+_('В обороте')+": <b>" + Helper.newAmount(circulation) + "</b> <code>| "+Helper.amount_two(circulation/(total/100))+"% </code>\n"
    text += "├ "+_('Заморожено')+": <b>" + Helper.newAmount(frozen) + "</b> <code>| "+Helper.amount_two(frozen/(circulation/100))+"% </code>\n"
    text += "└ "+_('Свободно') + ": <b>" + Helper.newAmount(free) + "</b> <code>| " + Helper.amount_two(free / (circulation / 100)) + "% </code>\n\n"


    text += "🕒 " + datetime.now(timezone.utc).strftime("%Y-%m-%d (%H:%M UTC)") + " \n"
    return text

def cycle():
    data = requests.get('https://explorer.mineplex.io/api/indexStats').json()
    return data['data'][0]['cycle']

def complexity():
    data = requests.get('https://explorer.mineplex.io/api/plexStats').json()
    return data['data'][0]['currentPricePlexForOneMine']

def reward():
    data = requests.get('https://explorer.mineplex.io/api/plexStats').json()
    return data['data'][0]['rewardPerBlock']

def total_wallets():
    data = requests.get('https://explorer.mineplex.io/api/addresses?isDeleted=false&$limit=1&$select[0]=address').json()
    return data['total']

# PLEX
URL_PLEXSTATS = 'https://explorer.mineplex.io/api/plexStats'

def all_plex():
    data = requests.get(URL_PLEXSTATS).json()
    return data['data'][0]['totalAmount']

def plex_in_circulation():
    data = requests.get(URL_PLEXSTATS).json()
    return data['data'][0]['inCirculationAmount']

def plex_in_circulation():
    data = requests.get(URL_PLEXSTATS).json()
    return data['data'][0]['inCirculationAmount']

def free_plex():
    data = requests.get(URL_PLEXSTATS).json()
    return data['data'][0]['totalFreeBalance']

def frozen_plex():
    data = requests.get(URL_PLEXSTATS).json()
    return data['data'][0]['totalFrozenBalance']

# MINE
URL_MINESTATS = 'https://explorer.mineplex.io/api/mineStats'

def all_mine():
    data = requests.get(URL_MINESTATS).json()
    return data['data'][0]['totalAmount']

def mine_in_circulation():
    data = requests.get(URL_MINESTATS).json()
    return data['data'][0]['inCirculationAmount']

def mine_in_circulation():
    data = requests.get(URL_MINESTATS).json()
    return data['data'][0]['inCirculationAmount']

def free_mine():
    data = requests.get(URL_MINESTATS).json()
    return data['data'][0]['totalFreeBalance']

def frozen_mine():
    data = requests.get(URL_MINESTATS).json()
    return data['data'][0]['totalFrozenBalance']


def address(add):
    data = requests.get('https://explorer.mineplex.io/api/addresses/'+add).json()
    return data


def transaction(t_id='', source='', destination=''):
    if t_id:
        data = requests.get('https://explorer.mineplex.io/api/transactions/'+t_id).json()
    elif source:
        data = requests.get('http://explorer.mineplex.io/api/transactions?%24sort%5BblockLevel%5D=-1&%24limit=1&source=' + source).json()
    elif destination:
        data = requests.get('http://explorer.mineplex.io/api/transactions?%24sort%5BblockLevel%5D=-1&%24limit=1&destination=' + destination).json()
    else: data = requests.get('https://explorer.mineplex.io/api/transactions/').json()
    return data['data'][0]
def pricePlexForOneMine(c = cycle()-8):
    r = requests.get('https://explorer.mineplex.io/api/cycles/' + str(c))
    dict = r.json()
    return dict['pricePlexForOneMine']

def priceMineForOnePlex(c = cycle()):
    r = requests.get('https://explorer.mineplex.io/api/cycles/'+str(c))
    dict = r.json()
    if c < 845  and c > 832  :
        return float(dict['pricePlexForOneMine']) * 2
    else: return dict['pricePlexForOneMine']

def cycleForward():
    text=''
    # text+= "👁‍🗨 <b>" + str(1) + "</b> " + _('цикл') +": " + Helper.amount_two(priceMineForOnePlex(1)) + "\n"
    # text+= "👁‍🗨 <b>" + str(100) + "</b> " + _('цикл') +": " + Helper.amount_two(priceMineForOnePlex(100)) + "\n"
    # text+= "👁‍🗨 <b>" + str(500) + "</b> " + _('цикл') +": " + Helper.amount_two(priceMineForOnePlex(500)) + "\n\n"

    text += "📕<b>"+ _('Прошедшие')+ ":</b>\n"
    c = cycle()
    i = 15
    while i != 0:
        if i==9:
            text += "└ <b>" + str(c - i+ 8) + "</b>: " + Helper.newAmount(priceMineForOnePlex(c - i)) + "\n\n"
        elif i>8:
            text+= "├ <b>" + str(c-i+ 8) + "</b>: " + Helper.newAmount(priceMineForOnePlex(c-i)) + "\n"
        elif i==8:
            text += "📗<b>"+ _('Текущий')+  " — " + str(c - i + 8) + "</b>: " + Helper.newAmount( priceMineForOnePlex(c - i)) + "\n\n"
            text += "📘<b>" + _('Грядущие')+ ":</b>\n"
        elif i==1:
            text += "└  <b>" + str(c - i+ 8) + "</b>: " + Helper.newAmount(priceMineForOnePlex(c - i)) + "\n\n"
        else:
            text += "├  <b>" + str(c - i+ 8) + "</b>: " + Helper.newAmount( priceMineForOnePlex(c - i)) + "\n"
        i-=1

    return text