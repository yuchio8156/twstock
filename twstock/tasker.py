# -*- coding: utf-8 -*-

import json
import time
import logging
import pandas as pd

from pathlib import Path
from random import randint
from decouple import config
from threading import Thread
from datetime import datetime

from twstock.utils.sort_stock import sort_stock
from twstock.stock_data_crawler import StockDataCrawler
from twstock.stock_info_crawler import StockInfoCrawler

from twstock.utils.get_logger import get_logger
main_logger = get_logger(name="main", level=logging.INFO)


def get_stock_info(
        today: str=datetime.today().strftime("%Y%m%d"), 
        ) -> pd.DataFrame: 
    """
    Get stock information and select the specified field and output json file
    
    Args:
        today (str): the date for retrieve data, formatted as yyyymmdd, default today
    
    Returns:
        stock_info_df (pd.DataFrame): 
            ticker (str): stock code
            name (str): stock name
            listed_at (str): listing date, formatted as yyyy/mm/dd
            industry (str): industry type
    """
    
    # filepath
    Path(f"./{today}").mkdir(parents=True, exist_ok=True)
    
    # fetch stock info
    main_logger.debug("get stock info, start")
    stock_info_crawler = StockInfoCrawler()
    stock_info_df = stock_info_crawler.get()
    stock_info_df = stock_info_df[["ticker", "name", "listed_at", "industry"]]
    
    # save as json
    filename = f"./{today}/listed.json"
    stock_info_json = stock_info_df.to_dict("records")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stock_info_json, f, ensure_ascii=False, indent=4)
    main_logger.info("get stock info, done")
    
    return stock_info_df


def get_top_stock(
        stock_info_df: pd.DataFrame, 
        today: str=datetime.today().strftime("%Y%m%d"), 
        top_n: int=3, 
        use_thread: bool=True, 
        ): 
    """
    Get all the stock price data of the day and sort the top n by industry
    Depends on the result of the `get_stock_info()` function
    There are three processing methods: 
        1. Local: execute sequentially
        2. Airflow: assign different tasks and use `xcom_pull()` function to communicate
        3. Lambda: detect S3 file `listed.json` and run
    
    Args:
        stock_info_df (pd.DataFrame): 
            ticker (str): stock code
            name (str): stock name
            listed_at (str): listing date, formatted as yyyy/mm/dd
            industry (str): industry type
        today (str): the date for retrieve data, formatted as yyyymmdd, default today
        top_n (int): top n stocks, default 3
        use_thread (bool): whether to use multithreading, default True
    
    Returns:
        none
    """
    
    # filepath
    Path(f"./{today}").mkdir(parents=True, exist_ok=True)
    
    # crawler
    stock_data_crawler = StockDataCrawler()
    
    # check if trading day
    stock_data = stock_data_crawler.get(ticker="2330", date=today)
    if len(stock_data) == 0: 
        main_logger.error("Today is not a trading day")
        raise ValueError
    else: 
        main_logger.info("check trading day, done")
    
    # run industries
    thread_list = []
    for industry in stock_info_df.industry.unique(): 
        ticker_list = stock_info_df.loc[stock_info_df.industry == industry, "ticker"].tolist()
        
        if use_thread: 
            thread = Thread(
                target=run_ticker_by_industry, 
                args=(industry, ticker_list, today, top_n, use_thread), 
                )
            thread.start()
            thread_list.append(thread)
        else: 
            run_ticker_by_industry(
                industry=industry, 
                ticker_list=ticker_list, 
                today=today, 
                use_thread=use_thread, 
                )
    
    # thread join
    if thread_list: 
        for thread in thread_list: 
            thread.join()
    
    return None


def run_ticker_by_industry(
        industry: str, 
        ticker_list: list, 
        today: str=datetime.today().strftime("%Y%m%d"), 
        top_n: int=3, 
        use_thread: bool=True, 
        ): 
    """
    Get all stock price data of the industry on the day and sort the top three
    
    Args:
        industry (str): industry type
        ticker_list (list): tickers of the industry
        today (str): the date for retrieve data, formatted as yyyymmdd, default today
        top_n (int): top n stocks, default 3
        use_thread (bool): whether to use multithreading, default True
    
    Returns:
        none
    """
    
    # crawler
    main_logger.debug(f"{industry}, start")
    stock_data_crawler = StockDataCrawler()
    
    # add proxy
    proxy = f"{config('PROXY_USERNAME')}:{config('PROXY_PASSWORD')}@zproxy.lum-superproxy.io:22225"
    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    stock_data_crawler.session.proxies.update(proxies)
    
    # run ticker
    stock_data_df = pd.DataFrame()
    for ticker in ticker_list: 
        stock_data = stock_data_crawler.get(ticker=ticker, date=today)
        main_logger.debug(f"{ticker}, done")
        
        stock_data_df = pd.concat([stock_data_df, stock_data], ignore_index=True)
        
        if not use_thread: 
            time.sleep(randint(2000, 3000)*0.001)
    
    # sort stock
    stock_data_df = stock_data_df[["ticker", "close", "change"]]
    stock_data_list = stock_data_df.to_dict("records")
    stock_data_json = sort_stock(stock_data_list=stock_data_list)
    
    # save as json
    filename = f"./{today}/{industry}_top3.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stock_data_json, f, ensure_ascii=False, indent=4)
    main_logger.info(f"{industry}, done")
    
    return None


if __name__ == "__main__": 
    stock_info_df = get_stock_info()
    get_top_stock(stock_info_df=stock_info_df)