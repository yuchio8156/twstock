# -*- coding: utf-8 -*-

import twstock as tw

from pathlib import Path
from datetime import datetime


def run(
        today: str=datetime.today().strftime("%Y%m%d"), 
        ): 
    """
    For local execution, combine `get_top3_stock_by_industry` and `get_top3_stock_by_industry`
    
    Args:
        today (str): the date for retrieve data, formatted as yyyymmdd, default today
    
    Returns:
        none
    """
    
    # filepath
    Path(f"./{today}").mkdir(parents=True, exist_ok=True)
    
    # fetch stock info
    stock_info_df = tw.get_stock_info(today=today)
    
    # fetch top3 for each industry
    tw.get_stock_top3(stock_info_df=stock_info_df, today=today, use_thread=True)
    
    return None


if __name__ == "__main__": 
    run()