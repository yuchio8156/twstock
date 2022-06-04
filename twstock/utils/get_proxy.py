# -*- coding: utf-8 -*-

import re
import requests

from typing import List
from twstock.stock_data_crawler import StockDataCrawler


def get_proxy() -> List: 
    """
    Get free proxy
    
    Args:
        none
        
    Returns:
        proxy_list (list): list of proxy string
    """
    
    url = "https://free-proxy-list.net/"
    rsp = requests.get(url)
    proxy_list = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}", rsp.text)
    
    # # verify that the proxy is available
    # stock_data_crawler = StockDataCrawler()
    # for proxy in proxy_list: 
    #     try: 
    #         proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    #         stock_data_crawler.session.proxies.update(proxies)
    #         stock_data_crawler.visit()
    #     except: 
    #         proxy_list.remove(proxy)
    
    return proxy_list


if __name__ == "__main__": 
    get_proxy()