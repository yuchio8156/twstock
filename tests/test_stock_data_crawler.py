# -*- coding: utf-8 -*-

import re
import pytest
import requests
import pandas as pd

from twstock.stock_data_crawler import StockDataCrawler


@pytest.fixture()
def stock_data_crawler():
    stock_data_crawler = StockDataCrawler()
    return stock_data_crawler


def test_cookie_maker(stock_data_crawler): 

    session = requests.Session()
    cookie = stock_data_crawler.cookie_maker(session=session)
    assert type(cookie) == str
    assert cookie == ""

    stock_data_crawler.visit()
    cookie = stock_data_crawler.cookie_maker(session=stock_data_crawler.session)
    assert type(cookie) == str
    assert re.match(r"JSESSIONID=.*", cookie)


def test_headers_maker(stock_data_crawler): 

    added = {}
    headers = stock_data_crawler.headers_maker(added=added)
    assert type(headers) == dict
    assert headers == {
        "Host": "www.twse.com.tw", 
        "Connection": "keep-alive", 
        "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'", 
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-platform": "'Windows'", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6", 
        "Cookie": "", 
        }

    added = {"Cookie": "123"}
    headers = stock_data_crawler.headers_maker(added=added)
    assert type(headers) == dict
    assert headers == {
        "Host": "www.twse.com.tw", 
        "Connection": "keep-alive", 
        "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'", 
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-platform": "'Windows'", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6", 
        "Cookie": "123", 
        }


def test_get(stock_data_crawler): 

    ticker = "2330"
    date = "20220601"
    stock_data_df = stock_data_crawler.get(ticker=ticker, date=date)
    assert type(stock_data_df) == pd.DataFrame
    assert len(stock_data_df) == 1
    assert stock_data_df.equals(
        pd.DataFrame([{
            "ticker": "2330", 
            "date": "2022/06/01", 
            "trade_volume": "32,970,903", 
            "trade_value": "18,171,598,472", 
            "open": "550.00", 
            "high": "555.00", 
            "low": "548.00", 
            "close": "549.00", 
            "change": "-11.00", 
            "transaction": "33,456"
            }])
        )

    ticker = "2330"
    date = "20770707"
    stock_data_df = stock_data_crawler.get(ticker=ticker, date=date)
    assert type(stock_data_df) == pd.DataFrame
    assert len(stock_data_df) == 0
    assert stock_data_df.equals(
        pd.DataFrame()
        )