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
            "transaction": "33,456", 
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

def test_get_industry_type_dict(stock_data_crawler): 

    industry_type_dict = stock_data_crawler.get_industry_type_dict()
    assert industry_type_dict == {
        "大盤統計資訊": "MS", 
        "收盤指數資訊": "IND", 
        "委託及成交統計資訊": "MS2", 
        "全部": "ALL", 
        "全部(不含權證、牛熊證、可展延牛熊證)": "ALLBUT0999", 
        "封閉式基金": "0049", 
        "ETF": "0099P", 
        "ETN": "029999", 
        "受益證券": "019919T", 
        "認購權證(不含牛證)": "0999", 
        "認售權證(不含熊證)": "0999P", 
        "牛證(不含可展延牛證)": "0999C", 
        "熊證(不含可展延熊證)": "0999B", 
        "可展延牛證": "0999X", 
        "可展延熊證": "0999Y", 
        "附認股權特別股": "0999GA", 
        "附認股權公司債": "0999GD", 
        "認股權憑證": "0999G9", 
        "可轉換公司債": "CB", 
        "創新板股票": "TIB", 
        "水泥工業": "01", 
        "食品工業": "02", 
        "塑膠工業": "03", 
        "紡織纖維": "04", 
        "電機機械": "05", 
        "電器電纜": "06", 
        "化學生技醫療": "07", 
        "化學工業": "21", 
        "生技醫療業": "22", 
        "玻璃陶瓷": "08", 
        "造紙工業": "09", 
        "鋼鐵工業": "10", 
        "橡膠工業": "11", 
        "汽車工業": "12", 
        "電子工業": "13", 
        "半導體業": "24", 
        "電腦及週邊設備業": "25", 
        "光電業": "26", 
        "通信網路業": "27", 
        "電子零組件業": "28", 
        "電子通路業": "29", 
        "資訊服務業": "30", 
        "其他電子業": "31", 
        "建材營造": "14", 
        "航運業": "15", 
        "觀光事業": "16", 
        "金融保險": "17", 
        "貿易百貨": "18", 
        "存託憑證": "9299", 
        "油電燃氣業": "23", 
        "綜合": "19", 
        "其他": "20", 
        }

def test_get_batch(stock_data_crawler): 

    industry_type = "08"
    date = "20220601"
    stock_data_df = stock_data_crawler.get_batch(industry_type=industry_type, date=date)
    assert type(stock_data_df) == pd.DataFrame
    assert len(stock_data_df) == 5
    assert stock_data_df.equals(
        pd.DataFrame([
            {
                "ticker": "1802",
                "trade_volume": "3,406,054",
                "transaction": "2,228",
                "trade_value": "76,741,638",
                "open": "22.55",
                "high": "22.80",
                "low": "22.35",
                "close": "22.35",
                "direction": "-",
                "change": "-0.45",
                "last_bid_price": "22.35",
                "last_bid_volume": "55",
                "last_ask_price": "22.40",
                "last_ask_volume": "10",
                "pe_ratio": "5.99"
                },
            {
                "ticker": "1806",
                "trade_volume": "436,417",
                "transaction": "205",
                "trade_value": "5,049,072",
                "open": "11.55",
                "high": "11.70",
                "low": "11.40",
                "close": "11.50",
                "direction": "-",
                "change": "-0.10",
                "last_bid_price": "11.50",
                "last_bid_volume": "23",
                "last_ask_price": "11.55",
                "last_ask_volume": "6",
                "pe_ratio": "4.34"
                },
            {
                "ticker": "1809",
                "trade_volume": "158,814",
                "transaction": "99",
                "trade_value": "2,051,104",
                "open": "12.95",
                "high": "13.00",
                "low": "12.80",
                "close": "12.90",
                "direction": "-",
                "change": "-0.05",
                "last_bid_price": "12.85",
                "last_bid_volume": "19",
                "last_ask_price": "12.95",
                "last_ask_volume": "16",
                "pe_ratio": "47.78"
                },
            {
                "ticker": "1810",
                "trade_volume": "218,338",
                "transaction": "104",
                "trade_value": "2,805,184",
                "open": "12.90",
                "high": "12.90",
                "low": "12.80",
                "close": "12.85",
                "direction": "",
                "change": "0.00",
                "last_bid_price": "12.85",
                "last_bid_volume": "10",
                "last_ask_price": "12.90",
                "last_ask_volume": "17",
                "pe_ratio": "3.55"
                },
            {
                "ticker": "1817",
                "trade_volume": "46,568",
                "transaction": "34",
                "trade_value": "1,623,861",
                "open": "34.80",
                "high": "35.00",
                "low": "34.80",
                "close": "34.95",
                "direction": "+",
                "change": "+0.15",
                "last_bid_price": "34.95",
                "last_bid_volume": "1",
                "last_ask_price": "35.00",
                "last_ask_volume": "8",
                "pe_ratio": "11.24"
                }
            ])
        )

    industry_type = "08"
    date = "20770707"
    stock_data_df = stock_data_crawler.get_batch(industry_type=industry_type, date=date)
    assert type(stock_data_df) == pd.DataFrame
    assert len(stock_data_df) == 0
    assert stock_data_df.equals(
        pd.DataFrame()
        )