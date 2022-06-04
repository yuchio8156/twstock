# -*- coding: utf-8 -*-

import os
import re
import json
import pytest
import pandas as pd

from twstock.tasker import get_stock_info, get_top_stock


@pytest.fixture(scope="module")
def test_get_stock_info(): 

    today = "20220601"
    stock_info_df = get_stock_info(today=today)
    assert type(stock_info_df) == pd.DataFrame
    assert stock_info_df.iloc[0].to_dict() == {
        "ticker": "1101", 
        "name": "台泥", 
        "listed_at": "1962/02/09", 
        "industry": "水泥工業", 
        }

    filename = f"./{today}/listed.json"
    assert os.path.isfile(filename)

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    assert type(data) == list
    assert data[0] == {
        "ticker": "1101", 
        "name": "台泥", 
        "listed_at": "1962/02/09", 
        "industry": "水泥工業", 
        }

    return stock_info_df


def test_get_top_stock(test_get_stock_info): 

    today = "20220601"
    use_thread = True
    top_n = 3
    get_top_stock(stock_info_df=test_get_stock_info, today=today, top_n=top_n, use_thread=use_thread)
    
    industry_list = [
        "光電業", "其他業", "其他電子業", "化學工業", "半導體業", "塑膠工業", "建材營造業", 
        "橡膠工業", "水泥工業", "汽車工業", "油電燃氣業", "玻璃陶瓷", "生技醫療業", "紡織纖維", 
        "航運業", "觀光事業", "貿易百貨業", "資訊服務業", "通信網路業", "造紙工業", "金融保險業", 
        "鋼鐵工業", "電器電纜", "電子通路業", "電子零組件業", "電機機械", "電腦及週邊設備業", "食品工業"
        ]
    for industry in industry_list: 
        assert os.path.isfile(f"./{today}/{industry}_top3.json")