#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE for details)
"""
Offseason data collector -- I/O operations

read_stat_monad -- get text from a url
write_json_monad -- write dict data as a json file
"""
import json
import requests

def read_stat_monad(url_page):
    """
    Get text of the url_page passed
    """
    return requests.get(url_page).text

def write_json_monad(file_name, out_dict):
    """
    Output data in out_dict as a json file to file_name
    """
    with open(file_name, "w", encoding="utf8") as ofd:
        json.dump(out_dict, ofd)
