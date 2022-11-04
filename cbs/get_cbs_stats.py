#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE for details)
"""
Offseason data collector -- Cbs Sportsline statistics

cbs_get_players -- get player data
"""
from bs4 import BeautifulSoup
from common.io_ops import read_stat_monad
from common.get_html_stats import save_all_players

def cbs_get_players():
    """
    Write local json file containing player info
    """
    save_all_players({"html_stat_getter":  cbs_get_stat_url,
                      "url_counter": cbs_url_counter,
                      "reformat_html": cbs_reformat_html,
                      "player_json": "cbs_players.json",
                      "table_loc": 0})

def cbs_get_stat_url(player_type, page_no):
    """
    Construct http address of url that gets players.  Player type is
    "batting" or "pitching".  Page_no is the specific page number for
    this set of statistics
    """
    return ''.join([
        "https://www.cbssports.com/mlb/stats/player/",
        player_type,
        "/mlb/regular/all-pos/all/?page=",
        str(page_no)
    ])

def cbs_reformat_html(htmldata):
    """
    Return string value of htmldata so later string operations do not fail
    """
    return str(htmldata)

def cbs_url_counter(player_type):
    """
    Scan for page numbers starting with 1
    """
    return get_set_of_urls(cbs_get_stat_url(player_type, ''), 1)

def get_set_of_urls(url_pattern, page_no):
    """
    Recursively search for an invalid url_pattern and page_no combination.
    Return value 1 past the number of valid numbers so that range functions
    will return the correct number
    """
    if has_no_table(f'{url_pattern}{page_no}'):
        return page_no
    return get_set_of_urls(url_pattern, page_no + 1)

def has_no_table(url_name):
    """
    Read the url and return true if this url is beyond the range of valid
    numbered urls.
    """
    if ''.join(BeautifulSoup(read_stat_monad(url_name),
            "html.parser").findAll(text=True)).find('Sorry, no results') > 0:
        return True
    return False

if __name__ == "__main__":
    cbs_get_players()
