# -*- coding: utf-8 -*-

import time
import requests
import pandas as pd

from typing import Dict
from urllib import parse
from datetime import datetime
from twstock import config as c
from lxml.html import fromstring
from twstock.logger import get_logger
data_logger = get_logger(name="data")


class StockDataCrawler(): 
    
    def __init__(self): 
        
        self.session = requests.Session()
        
        self.cookie = ""
        
        self.column_dict = {
            "Date": "date", 
            "Trade Volume": "trade_volume", 
            "Trade Value": "trade_value", 
            "Opening Price": "open", 
            "Highest Price": "high", 
            "Lowest Price": "low", 
            "Closing Price": "close", 
            "Change": "change", 
            "Transaction": "transaction", 
            }
        
        self.column_dict_for_batch = {
            "Security Code": "ticker", 
            "Trade Volume": "trade_volume", 
            "Transaction": "transaction",
            "Trade Value": "trade_value", 
            "Opening Price": "open", 
            "Highest Price": "high", 
            "Lowest Price": "low", 
            "Closing Price": "close", 
            "Dir(+/-)": "direction", 
            "Change": "change", 
            "Last Best Bid Price": "last_bid_price", 
            "Last Best Bid Volume": "last_bid_volume", 
            "Last Best Ask Price": "last_ask_price", 
            "Last Best Ask Volume": "last_ask_volume", 
            "Price-Earning ratio": "pe_ratio", 
            }
    
    def cookie_maker(
            self, 
            session: requests.Session, 
            ) -> str: 
        """
        Get session cookie
        
        Args:
            session (requests.Session)
                
        Returns:
            cookie (str)
        """
        
        cookie_dict = session.cookies.get_dict()
        cookie_list = [k + "=" + v for k, v in cookie_dict.items()]
        cookie = "; ".join(item for item in cookie_list)
        
        return cookie
    
    def headers_maker(
            self, 
            added: Dict, 
            ) -> Dict: 
        """
        Manage common headers and add others for special use
        
        Args:
            added (dict): additional headers
                
        Returns:
            headers (dict): final headers
        """
        
        headers = {
            "Host": "www.twse.com.tw", 
            "Connection": "keep-alive", 
            "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'", 
            "sec-ch-ua-mobile": "?0", 
            "sec-ch-ua-platform": "'Windows'", 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6", 
            "Cookie": self.cookie, 
            }
        headers.update(added)
        
        return headers
    
    def visit(
            self, 
            retry: int=c.RETRY, 
            ): 
        """
        Request stock search page and get the initial cookie to simulate real visit
        
        Args:
            retry (int): The number of attempts when the request failed
        
        Returns:
            none
        """
        
        # request
        url = "https://www.twse.com.tw/en/page/trading/exchange/STOCK_DAY.html"
        headers = self.headers_maker({
            "Cache-Control": "max-age=0", 
            "Upgrade-Insecure-Requests": "1", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Sec-Fetch-Site": "none", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-User": "?1", 
            "Sec-Fetch-Dest": "document", 
            })
        for i in range(retry): 
            try: 
                rsp = self.session.get(url, headers=headers)
                break
            except Exception as e: 
                data_logger.error(f"Failed to connect page, {e}")
                time.sleep(i+1)
            if i+1 == retry: 
                raise ConnectionError
        
        # check connection
        if rsp.status_code != 200: 
            data_logger.error(f"Failed to access page, {rsp.status_code}")
            raise ConnectionError
        
        # update cookie
        self.cookie = self.cookie_maker(session=self.session)
        
        return None
    
    def get(
            self, 
            ticker: str="2330", 
            date: datetime="20220601", 
            retry: int=c.RETRY, 
            ) -> pd.DataFrame: 
        """
        Get single stock data on a specified date
        
        Args:
            ticker (str): stock code, default 2330
            date (str): the date to fetch stock data, formatted as yyyymmdd, default 20220601
            retry (int): The number of attempts when the request failed
                
        Returns:
            stock_data_df (pd.DataFrame): 
                ticker (str): stock code
                date (str)
                trade_volume (str)
                trade_value (str)
                open (str)
                high (str)
                low (str)
                close (str)
                change (str)
                transaction (str)
        """
        
        # convert date to datetime
        date = datetime.strptime(date, "%Y%m%d")
        
        # check if weekend
        if date.strftime("%a") in ["Sat", "Sun"]: 
            data_logger.warning("Today is not a trading day")
            return pd.DataFrame()
        
        # make query string
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        data = {
            "response": "json", 
            "date": date.strftime("%Y%m%d"), 
            "stockNo": ticker, 
            "_": int(timestamp * 1000), 
            }
        query_string = parse.urlencode(data)
        
        # request
        url = f"https://www.twse.com.tw/en/exchangeReport/STOCK_DAY?{query_string}"
        headers = self.headers_maker({
            "Accept": "application/json, text/javascript, */*; q=0.01", 
            "Sec-Fetch-Site": "same-origin", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Dest": "empty", 
            "X-Requested-With": "XMLHttpRequest", 
            "Referer": "https://www.twse.com.tw/en/page/trading/exchange/STOCK_DAY.html", 
            })
        for i in range(retry): 
            try: 
                rsp = self.session.get(url, headers=headers, timeout=3)
                break
            except Exception as e: 
                data_logger.error(f"{ticker}, failed to connect page, {e}")
                time.sleep(i+1)
            if i+1 == retry: 
                raise ConnectionError
        
        # check connection
        if rsp.status_code != 200: 
            data_logger.error(f"{ticker}, failed to access page, {rsp.status_code}")
            raise ConnectionError
        
        # check if json exists
        try: 
            data = rsp.json()
        except: 
            data_logger.warning(f"{ticker}, failed to fetch json")
            return pd.DataFrame()
        
        # check if data exists
        if data["stat"] != "OK": 
            data_logger.warning(f"{ticker}, failed to fetch data, {data['stat']}")
            return pd.DataFrame()
        
        # check if data exists
        if len(data["data"]) == 0: 
            data_logger.warning(f"{ticker}, failed to fetch data, data not updated")
            return pd.DataFrame()
        
        # check data format
        columns = list(self.column_dict.keys())
        if data["fields"] != columns: 
            data_logger.error(f"{ticker}, Incorrect dataframe format")
            raise ValueError
        
        # check data format
        first_record = data["data"][0]
        if len(columns) != len(first_record): 
            data_logger.error(f"{ticker}, incorrect dataframe format")
            raise ValueError
        
        # convert data to dataframe
        df = pd.DataFrame(data=data["data"], columns=columns)
        
        # arrange dataframe
        df = df.loc[df.Date == date.strftime("%Y/%m/%d")] # filter date
        df = df.rename(columns=self.column_dict) # rename
        df["ticker"] = ticker # add ticker
        df = df[["ticker", "date", "trade_volume", "trade_value", "open", "high", "low", "close", "change", "transaction"]] # select
        stock_data_df = df.reset_index(drop=True).copy() # reset row index
        
        return stock_data_df
    
    def get_industry_type_dict(
            self, 
            retry: int=c.RETRY, 
            ): 
        """
        TWSE provides batch retrieval of stocks by industry, and its query index is industry type.
        The purpose of this function is to access the mapping table of industry type.
        
        Args:
            retry (int): The number of attempts when the request failed
                
        Returns:
            industry_type_dict (dict): mapping table of industry type
        """
        
        # request
        url = "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html"
        headers = self.headers_maker({
            "Upgrade-Insecure-Requests": "1", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Sec-Fetch-Site": "cross-site", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-User": "?1", 
            "Sec-Fetch-Dest": "document", 
            "Referer": "https://www.google.com/", 
            })
        for i in range(retry): 
            try: 
                rsp = self.session.get(url, headers=headers)
                break
            except Exception as e: 
                data_logger.error(f"Failed to connect page, {e}")
                time.sleep(i+1)
            if i+1 == retry: 
                raise ConnectionError
        
        # check connection
        if rsp.status_code != 200: 
            data_logger.error("Try to get industry type mapping table, failed to access page, {rsp.status_code}")
            raise ConnectionError
        
        # parse (find <select>)
        root = fromstring(rsp.text)
        path = root.xpath(".//*[@id='main-form']/div/div/form/select")
        
        # check if data exists
        if path: 
            industry_type_dict = {}
            
            for p in path: 
                # parse (find <option>)
                options = p.xpath(".//option")
                
                for opt in options: 
                    # parse (find text(key) and value)
                    industry_type_key = opt.text_content()
                    industry_type_val = opt.get("value")
                    industry_type_pair = {industry_type_key: industry_type_val}
                    
                    # update industry_type_dict
                    industry_type_dict.update(industry_type_pair)
        else: 
            data_logger.error("Try to get industry type mapping table, failed to parse page")
            raise ValueError
        
        return industry_type_dict
    
    def get_batch(
            self, 
            industry_type: str="01", 
            date: datetime="20220601", 
            retry: int=c.RETRY, 
            ) -> pd.DataFrame: 
        """
        TWSE provides batch retrieval of stocks by industry, and its query index is industry type.
        The purpose of this function is to grab all stocks in the industry at once to save time and reduce requests.
        
        Args:
            industry_type (str): industry type, default `01` equivalent `cement`
            date (str): the date to fetch stock data, formatted as yyyymmdd, default 20220601
            retry (int): The number of attempts when the request failed
                
        Returns:
            stock_data_df (pd.DataFrame): 
                ticker (str): stock code
                trade_volume (str)
                transaction (str)
                trade_value (str)
                open (str)
                high (str)
                low (str)
                close (str)
                direction (str)
                change (str)
                last_bid_price (str)
                last_bid_volume (str)
                last_ask_price (str)
                last_ask_volume (str)
                pe_ratio (str)
        """
        
        # convert date to datetime
        date = datetime.strptime(date, "%Y%m%d")
        
        # check if weekend
        if date.strftime("%a") in ["Sat", "Sun"]: 
            data_logger.warning("Today is not a trading day")
            return pd.DataFrame()
        
        # make query string
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        data = {
            "response": "json", 
            "date": date.strftime("%Y%m%d"), 
            "type": industry_type, 
            "_": int(timestamp * 1000), 
            }
        query_string = parse.urlencode(data)
        
        # request
        url = f"https://www.twse.com.tw/en/exchangeReport/MI_INDEX?{query_string}"
        headers = self.headers_maker({
            "Accept": "application/json, text/javascript, */*; q=0.01", 
            "Sec-Fetch-Site": "same-origin", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Dest": "empty", 
            "X-Requested-With": "XMLHttpRequest", 
            "Referer": "https://www.twse.com.tw/en/page/trading/exchange/MI_INDEX.html", 
            })
        for i in range(retry): 
            try: 
                rsp = self.session.get(url, headers=headers, timeout=3)
                break
            except Exception as e: 
                data_logger.error(f"Industry {industry_type}, failed to connect page, {e}")
                time.sleep(i+1)
            if i+1 == retry: 
                raise ConnectionError
        
        # check connection
        if rsp.status_code != 200: 
            data_logger.error(f"Industry {industry_type}, failed to access page, {rsp.status_code}")
            raise ConnectionError
        
        # check if json exists
        try: 
            data = rsp.json()
        except: 
            data_logger.warning(f"Industry {industry_type}, failed to fetch json")
            return pd.DataFrame()
        
        # check if data exists
        if data["stat"] != "OK": 
            data_logger.warning(f"Industry {industry_type}, failed to fetch data, {data['stat']}")
            return pd.DataFrame()
        
        # check if data exists
        if len(data["data1"]) == 0: 
            data_logger.warning(f"Industry {industry_type}, failed to fetch data, data not updated")
            return pd.DataFrame()
        
        # check data format
        columns = list(self.column_dict_for_batch.keys())
        if data["fields1"] != columns: 
            data_logger.error(f"Industry {industry_type}, Incorrect dataframe format")
            raise ValueError
        
        # check data format
        first_record = data["data1"][0]
        if len(columns) != len(first_record): 
            data_logger.error(f"Industry {industry_type}, incorrect dataframe format")
            raise ValueError
        
        # convert data to dataframe
        df = pd.DataFrame(data=data["data1"], columns=columns)
        
        # arrange dataframe
        df = df.rename(columns=self.column_dict_for_batch) # rename
        df["direction"] = [
            fromstring(direction).text_content() if "</p>" in direction else "" 
            for direction in df["direction"]
            ] # deformat direction to +/-
        df["change"] = df["direction"] + df["change"]
        stock_data_df = df.reset_index(drop=True).copy() # reset row index
        
        return stock_data_df


if __name__ == "__main__": 
    stock_data_crawler = StockDataCrawler()
    stock_data_crawler.visit()
    stock_data_df = stock_data_crawler.get(ticker="2330", date="20220601")