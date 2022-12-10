import requests
import time
from logger import *
import asyncio


watchers = dict()
counter = 0


def get_binance_url(symbol):
    return 'https://fapi.binance.com/fapi/v1/trades?symbol=' + symbol + '&limit=' + '1'


class InvalidSymbolException(BaseException):
    pass


def get_price(symbol):
    url = get_binance_url(symbol)
    data = requests.get(url).json()
    if 'msg' in data:
        raise InvalidSymbolException
    price = data[-1]['price']
    return price


def watch_instrument(symbol, is_greater, level, userid):
    global counter, watchers
    if userid in watchers:
        user_watchers = watchers[userid]
    else:
        user_watchers = dict()
        watchers[userid] = user_watchers

    counter += 1
    current = counter
    user_watchers[symbol] = current

    local_counter = 0

    while symbol in watchers[userid] and watchers[userid][symbol] == current:
        price = float(get_price(symbol))
        local_counter += 1
        if local_counter > 10:
            text = 'after all this time never reached the level...\n symbol' + ' : ' + str(price)
            return text
        if (is_greater and (price >= level)) or (not is_greater and (price <= level)):
            text = symbol + ' : ' + str(price)
            watchers[hash] = False
            return text
        time.sleep(1)


def stop_watch(symbol, userid):
    global watchers
    if userid in watchers and symbol in watchers[userid]:
        del watchers[userid][symbol]
        return "Watcher stopped"
    else:
        return "Not found watcher for " + symbol


def show_watches(userid):
    global watchers
    if userid in watchers:
        return watchers[userid]
    else:
        return 'You have no active watchers'



