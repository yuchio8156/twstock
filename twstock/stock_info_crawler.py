# -*- coding: utf-8 -*-

import time
import requests
import pandas as pd

from twstock.utils.get_logger import get_logger
info_logger = get_logger(name="info")


class StockInfoCrawler(): 
    
    def __init__(self): 
        
        self.session = requests.Session()
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/101.0.0.0 Safari/537.36", 
            "Referer": "https://www.google.com/", 
            "Accept-Encoding": "gzip, deflate", 
            "Accept": "text/html", 
            }
        
        self.column_dict = {
            "有價證券代號及名稱": "ticker_name", 
            "國際證券辨識號碼(ISIN Code)": "isin_code", 
            "上市日": "listed_at", 
            "市場別": "market", 
            "產業別": "industry", 
            "CFICode": "cfi_code", 
            "備註": "note", 
            }
    
    def get(
            self, 
            retry: int=5, 
            ) -> pd.DataFrame: 
        """
        Request `https://isin.twse.com.tw/isin/C_public.jsp?strMode=2` and 
        parse HTML table to get the stock information dataframe.
        
        Args:
            retry (int): The number of attempts when the request failed
        
        Returns:
            stock_info_df (pd.DataFrame): 
                ticker (str): stock code
                name (str): stock name
                isin_code (str): ISIN code
                listed_at (str): listing date, formatted as yyyy/mm/dd
                market (str): market type
                industry (str): industry type
                cfi_code (str): CFI code
                note (str): note
        """
        
        # request
        url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
        for i in range(retry): 
            try: 
                rsp = self.session.get(url, headers=self.headers)
                break
            except Exception as e: 
                info_logger.error(f"Failed to connect page, {e}")
                time.sleep(i+1)
            if i+1 == retry: 
                raise ConnectionError
        
        # check connection
        if rsp.status_code != 200: 
            info_logger.error(f"Failed to access page, {rsp.status_code}")
            raise ConnectionError
        
        # check if table exists
        try: 
            tables = pd.read_html(rsp.text)
        except: 
            info_logger.error("Failed to fetch html table")
            raise ValueError
        
        # get dataframe
        columns = list(self.column_dict.keys())
        if len(tables) > 1: 
            first_column = columns[0]
            check = [first_column in str(table) for table in tables]
            index = check.index(True)
            df = tables[index]
        else: 
            df = tables[0]
        
        # check dataframe columns
        first_row = df.loc[0].tolist()
        if first_row != columns: 
            info_logger.error("Incorrect dataframe format")
            raise ValueError
        
        # arrange dataframe
        df.columns = first_row # assign colnames
        df = df.rename(columns=self.column_dict) # rename
        df = df.loc[df.market == "上市"] # remove category row
        df = df.dropna(subset=["industry"]) # remove not stock by industry column
        df[["ticker", "name"]] = df["ticker_name"].str.split(r"\s", 1, expand=True) # split ticker and name
        df = df[["ticker", "name", "isin_code", "listed_at", "market", "industry", "cfi_code", "note"]] # select
        df = df.fillna("") # fill missing value (note column)
        stock_info_df = df.reset_index(drop=True).copy() # reset row index
        
        return stock_info_df


if __name__ == "__main__": 
    stock_info_crawler = StockInfoCrawler()
    stock_info_df = stock_info_crawler.get()