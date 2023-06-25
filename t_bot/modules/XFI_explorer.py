import requests
from t_bot.modules import Helper, Coingeco
from django.utils.translation import gettext as _
from datetime import datetime, timezone
from var_dump import var_dump
import json
import os
from t_bot.config.main import Validators

S = 1000000000000000000

def coins():
    data = requests.get('https://explorer-api.mineplex.io/coins').json()
    return data

def address(add):
    data = requests.get('https://explorer-api.mineplex.io/address/'+add).json()
    return data

def validator(mxvaloper):
    data = requests.get('https://explorer-api.mineplex.io/validator/'+mxvaloper).json()
    return data

def status():
    data = requests.get('https://explorer-api.mineplex.io/status').json()
    return data

def tx(tx):
    data = requests.get('https://explorer-api.mineplex.io/tx/'+tx).json()
    return data

def total_claim():
    key = json.loads(os.popen('/root/./mineplex-chaind query distribution commission '+Validators.cosmos+' --output json').read())
    var_dump(key)
    return key['commission'][1]['amount']

def generate_keys():
    key = json.loads(os.popen('/root/./mineplex-chaind keys add aaa --dry-run --output json').read())
    return key

def price_xfi_exchange():
    data = requests.get('https://mineplex.cash/api/2.0/payment/currency?limit=2').json()
    return 1/float(data['docs'][1]['rate'])


def price_xfi():
    c = coins()
    M = float(c['coins'][0]['amount'])/S
    E = 5
    B = 518400
    # P = 7
    P = 100/12 - 100/12*0.165
    var_dump(P)
    return ((P/100)*(M/E))/B/100


def search(data):
    var_dump(data[:9])
    if data[:9] == 'mxvaloper':
        return validator_info(data)
    elif data[:3] == 'mx1':
        return address_info(data)
    else:
        try:
            return tx_info(data)
        except: return 'ошибка'


def address_info(add):
    data = address(add)
    var_dump(data)
    text = "🗄 <a href='https://explorer.mineplex.io/mx/address/" + add + "'>" + add[:10] + "....." + add[30:] + "</a>\n\n"
    text +="🏦 Баланс:\n"
    l = len(data['coins'])
    for i in data['coins']:
        if l == 2:
            text += "├ <b>" + i['denom'].upper() + ": " + Helper.amount_mpx(i['amount']) + "</b>\n"
        else: text += "└ <b>" + i['denom'].upper() + ": " +  Helper.amount_mpx(i['amount']) + "</b>\n\n"
        l-=1

    text += "🔰 Cтейкинг:\n"
    l = len(data['delegations'])
    for i in data['delegations']:
        if l >= 2:
            text += "├ " + i['delegation']['validator_address'][:5] + "..."+ i['delegation']['validator_address'][40:] + ": <b>" + Helper.amount_mpx(i['balance']['amount']) + i['balance']['denom'].upper() + "</b>\n"
        else:
            text += "└ " + i['delegation']['validator_address'][:5] + "..."+ i['delegation']['validator_address'][40:] + ": <b>" + Helper.amount_mpx(i['balance']['amount']) + i['balance']['denom'].upper() + "</b>\n\n"
        l -= 1

    # text += "💰 Rewards: <b>" + Helper.amount_mpx(data['rewards']['total'][1]['amount']) + data['rewards']['total'][1]['denom'].upper() + "</b>"
    return text


def validator_info(data_val):
    data = validator(data_val)
    text= ''
    text += "🔗 <a href='https://explorer.mineplex.io/mx/validator/" + data_val + "'>" + data_val[:10] + "....." + data_val[30:] + "</a> \n\n"

    text += '⛓ <b>' + data['validator']['description']['moniker'] + '</b><code> ('+Helper.newAmount(float(data['validator']['commission']['commission_rates']['rate'])*100)+'%)</code>\n'
    text += '├ '+_('General stake')+'<b>: '+Helper.amount_mpx(data['validator']['delegator_shares'])+'MPX</b>\n'
    text += '├ '+_('Number of delegates')+'<b>: '+data['delegators_count']+' </b>\n'
    text += '├ '+_('Total claimed now') + '<b>: ' + Helper.amount_mpx(total_claim(), six=True) + ' XFI </b>\n'
    if data['validator']['status'] == 'BOND_STATUS_BONDED': status = 'set on 🔋'
    else: status = 'set off 🪫'
    text += '└ '+_('Status')+'<b>: '+status+'</b> \n'
    return text

def tx_type(tx):
    try:
        if tx['isReward'] == True:
            return _('reword')
    except: return _('transfer')


def generate_content():
    c = coins()
    s = status()
    text = '📡 Cтатус сети\n\n' \
    '📊 Стоимость XFI — $1,1354\n\n' \
    '⚫️ XFI\n' \
    '├ Всего: <b>'+Helper.amount_mpx(c['coins'][1]['amount'])+'</b>\n' \
    '└ В обороте: <b>'+Helper.amount_mpx(c['unclaimed_coins'][1]['amount'])+'</b>\n\n' \
    '⚪️ MPX\n' \
    '├ Всего: ∞\n' \
    '├ В обороте: <b>'+Helper.amount_mpx(c['coins'][0]['amount'])+'</b>\n' \
    '└ Застейкано: <b>'+Helper.amount_mpx(c['staked_coins'][0]['amount'])+'</b>\n\n' \
    '♻️Общее\n' \
    '├ Высота блоков: <b>' + Helper.newAmount(s['latest_block_height']) + '</b>\n'\
    '├ Всего аккаунтов: <b>' + Helper.newAmount(s['total_accounts']) + '</b>\n'\
    '└ Вcего транзакций: <b>' + Helper.newAmount(s['total_txs']) + '</b>\n\n'\
    '🕒 2023-04-22 (09:04 UTC)\n'


    return text


def tx_info(tx, amount):
    text= ''
    text += "🗄 <a href='https://explorer.mineplex.io/mx/txs/" + tx.hash + "'>" + tx.hash[:10] + "....." + tx.hash[50:] + "</a>\n\n"

    text += '📂️ <b>' + _('Transaction:') + '</b>\n'
    text += '├ '+_('Type')+': <b>'+_("Claim")+' </b>\n'
    text += '├ '+_('Validator') + ': ' + "<a href='https://explorer.mineplex.io/mx/validators/" + Validators.cosmos + "'>" + Validators.cosmos[:10] + "....." + Validators.cosmos[30:] + "</a>" + '\n'
    text += '├ '+_('Address')+': '+ "<a href='https://explorer.mineplex.io/mx/addresses/" + Validators.addres_cosmos+ "'>" + Validators.addres_cosmos[:10] + "....." + Validators.addres_cosmos[30:] + "</a>" +'\n'
    text += '├ '+_('Amount') + ': <b>'+ amount + ' XFI</b>\n'
    text += '└ '+_('Data')+': <b>'+str(tx.timestamp)+'</b>\n'
    return text