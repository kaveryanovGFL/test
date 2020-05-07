#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def price(coins, names):
    '''Create price to show by names coins'''
    remote_data = requests.get('https://api.exmo.com/v1.1/ticker').json()
    data = remote_data[coins]
    value = '''Стоимость {} к доллару:
    {} - максимальная цена сделки за 24 часа
    {} - минимальная цена сделки за 24 часа
    {} - средняя цена сделки за 24 часа
    {} - объем всех сделок за 24 часа
    {} - сумма всех сделок за 24 часа
    {} - цена последней сделки
    {} - текущая максимальная цена покупки
    {} - текущая минимальная цена продажи'''.format(
        names,
        data['high'],
        data['low'],
        data['avg'],
        data['vol'],
        data['vol_curr'],
        data['last_trade'],
        data['buy_price'],
        data['sell_price'])
    return value


def etherium():
    '''Return ETH price in good view'''
    return price('ETH_USD', 'Эфира')


def bitcoin():
    '''Return BTC price in good view'''
    return price('BTC_USD', 'Биткоина')
