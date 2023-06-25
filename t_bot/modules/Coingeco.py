from pycoingecko import CoinGeckoAPI
from t_bot.modules import MP_explorer, Helper, XFI_explorer
from var_dump import var_dump
from decimal import *

from django.utils.translation import gettext as _


cg = CoinGeckoAPI()
def test():
    pass
    # return  cg.get_price(ids='plex', vs_currencies='usd') ['market_data']

def price(coin):
    data = cg.get_price(coin, vs_currencies='usd')
    return data[coin]['usd']


def percent():
    data = cg.get_coin_by_id('plex')
    return data['market_data']


def exchanges():
    data = cg.get_coin_by_id('plex')
    # var_dump(data)
    return data['tickers']


def id_coin():
    coins = cg.get_coins_list()
    for i in coins:
        if i['symbol'] == 'plex':
            return i['id']


def capitalization():
    data = cg.get_coin_by_id('plex')
    cap = 0
    for item in data['tickers']:
        cap += item['volume']
    return str(float("{0:.1f}".format(cap / 2)))

def generate_message():

    mine_price= price('plex')/MP_explorer.priceMineForOnePlex(MP_explorer.cycle()-8)
    var_dump(1)
    data = exchanges()

    text = '<b>MINE:</b> $' + str(Helper.amount(Decimal(mine_price))) + "\n"
    text += '<b>PLEX:</b> $' + str(price('plex'))+ "\n"
    text += "📊 PLEX/USDT <a href='https://www.mexc.com/exchange/PLEX_USDT?_from=market'><b>MEXC Global</b></a>" '\n\n'

    text += '<b>MPX:</b> $' + str(0.01)  + "\n"
    text += '<b>XFI:</b> $' + str(Helper.amount(Decimal(XFI_explorer.price_xfi_exchange())))+ "\n"

    text += "📊 XFI/USDT <a href='https://www.mexc.com/exchange/XFI_USDT?_from=market'><b>MEXC Global</b></a> " '\n'
    return text