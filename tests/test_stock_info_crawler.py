# -*- coding: utf-8 -*-

import pytest
import pandas as pd

from twstock.stock_info_crawler import StockInfoCrawler


@pytest.fixture()
def stock_info_crawler():
    stock_info_crawler = StockInfoCrawler()
    return stock_info_crawler


def test_get(stock_info_crawler): 

    stock_info_df = stock_info_crawler.get()
    assert type(stock_info_df) == pd.DataFrame
    assert stock_info_df.iloc[0].to_dict() == {
        "ticker": "1101", 
        "name": "台泥", 
        "isin_code": "TW0001101004", 
        "listed_at": "1962/02/09", 
        "market": "上市", 
        "industry": "水泥工業", 
        "cfi_code": "ESVUFR", 
        "note": ""
        }