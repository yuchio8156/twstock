# -*- coding: utf-8 -*-

from twstock.utils.sort_stock import sort_stock


def test_sort_stock(): 

    stock_data_list = [
        {"ticker": "2334", "close": "--", "change": " 0.00"}, 
        {"ticker": "2333", "close": "1,080", "change": "X0.00"}, 
        {"ticker": "2332", "close": "1,080", "change": "80"}, 
        {"ticker": "2331", "close": "1,090", "change": "90"}, 
        {"ticker": "2330", "close": "1,100", "change": "100"}, 
        ]
    top_n = 2
    result = sort_stock(stock_data_list=stock_data_list, top_n=top_n)
    assert type(result) == list
    assert len(result) == 2
    assert result == [{"ticker": "2330", "diff": "10.00%"}, {"ticker": "2331", "diff": "9.00%"}]

    stock_data_list = [
        {"ticker": "2334", "close": "--", "change": " 0.00"}, 
        {"ticker": "2333", "close": "1,080", "change": "X0.00"}, 
        {"ticker": "2332", "close": "1,080", "change": "80"}, 
        {"ticker": "2331", "close": "1,090", "change": "90"}, 
        {"ticker": "2330", "close": "1,100", "change": "100"}, 
        ]
    top_n = 0
    result = sort_stock(stock_data_list=stock_data_list, top_n=top_n)
    assert type(result) == list
    assert len(result) == 0
    assert result == []

    stock_data_list = []
    top_n = 2
    result = sort_stock(stock_data_list=stock_data_list, top_n=top_n)
    assert type(result) == list
    assert len(result) == 0
    assert result == []