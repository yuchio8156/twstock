# -*- coding: utf-8 -*-

import pytz
import logging


RETRY = 5
LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

TOPN = 3
USE_THREAD = True
TIMEZONE = pytz.timezone("Asia/Taipei")
CRONTAB = "0 15 * * *" # min hour day month week