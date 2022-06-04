# -*- coding: utf-8 -*-

import re
import logging
import os.path

from datetime import datetime
from twstock.utils.get_logger import get_logger


def test_get_logger(): 

    today = datetime.today().strftime("%Y%m%d")
    filename = f"./{today}.log"

    name = "test"
    level = logging.WARNING
    test_logger = get_logger(name=name, level=level)
    assert os.path.isfile(filename) # check file

    test_logger.critical("critical message")
    with open(filename) as f: 
        for line in f: 
            pass
        last_line = line
    assert re.match(r".* test CRITICAL: critical message", last_line) # check file content