# -*- coding: utf-8 -*-

import pytz
import logging

from decouple import config


RETRY = 5
LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

TOPN = 3
TIMEZONE = pytz.timezone("Asia/Taipei")
CRONTAB = "0 15 * * mon-fri" # min hour day month week
USE_INDUSTRY = True

if config("USE_PROXY").upper() == "TRUE": 
    USE_THREAD = True
else: 
    USE_THREAD = False