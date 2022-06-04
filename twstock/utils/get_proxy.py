# -*- coding: utf-8 -*-

import re
import requests


def get_proxy() -> list: 
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
    
    return proxy_list


if __name__ == "__main__": 
    get_proxy()