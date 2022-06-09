# -*- coding: utf-8 -*-

import twstock as tw

from pathlib import Path
from datetime import datetime
from twstock import config as c
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BlockingScheduler


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
    
    # fetch top 3 for each industry
    tw.get_top_stock(stock_info_df=stock_info_df, today=today, top_n=c.TOPN, use_thread=c.USE_THREAD)
    
    return None


if __name__ == "__main__": 
    scheduler = BlockingScheduler()
    scheduler.add_job(run, CronTrigger.from_crontab(expr=c.CRONTAB, timezone=c.TIMEZONE), misfire_grace_time=300)
    scheduler.start()