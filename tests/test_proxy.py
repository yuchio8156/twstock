# -*- coding: utf-8 -*-

import re

from twstock.proxy import get_proxy


def test_get_proxy(): 

    proxy_list = get_proxy()

    assert type(proxy_list) == list
    assert re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}", proxy_list[0])