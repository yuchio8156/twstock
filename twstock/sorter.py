# -*- coding: utf-8 -*-

import heapq

from typing import List


def sort_stock(
        stock_data_list: List, 
        top_n: int = 3, 
        ) -> List: 
    """
    Sort and pick the top n stocks with the largest price change
    Required input keys are ticker, close and change
    Return is a list of dictionary containing ticker and diff
    
    Args:
        stock_data_list (list): list of dict
            dict (required): 
                ticker (str): stock code
                close (str): closing price of the day
                change (str): price difference from the previous day
        top_n (int): top n stocks, default 3
        
    Returns:
        result (list): list of dict
            dict: 
                ticker (str): stock code
                diff (str): string of price change percentage
    """
    
    # calc diff and foramt diff
    for stock_data in stock_data_list: 
        if "X" in stock_data["change"]: 
            # Not compared, instructions on the official website
            stock_data["real_diff"] = -999
        elif stock_data["change"] == " 0.00": 
            # If no change, diff assign zero
            stock_data["real_diff"] = 0
        elif stock_data["close"] == "--": 
            # If no change, diff assign zero
            stock_data["real_diff"] = 0
        else: 
            change = float(stock_data["change"].replace(",", ""))
            close = float(stock_data["close"].replace(",", ""))
            stock_data["real_diff"] = change / (close - change)
        stock_data["diff"] = "{:.2%}".format(stock_data["real_diff"])
    
    # heapq sort 
    stock_data_list_sorted = heapq.nlargest(top_n, stock_data_list, lambda x: x["real_diff"])
    
    # filter key
    result = [{
        k: v 
        for k, v in stock_data.items() if k in ["ticker", "diff"]
        } for stock_data in stock_data_list_sorted]
    
    return result


if __name__ == "__main__": 
    stock_data_list = [
        {"ticker": "2332", "close": "1,080", "change": "80"}, 
        {"ticker": "2331", "close": "1,090", "change": "90"}, 
        {"ticker": "2330", "close": "1,100", "change": "100"}, 
        ]
    sort_stock(stock_data_list=stock_data_list, top_n=3)