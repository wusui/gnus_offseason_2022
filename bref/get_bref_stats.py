#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE for details)
"""
Offseason data collector -- baseball_reference statistics

bref_get_players -- get player data
"""
from common.get_html_stats import save_all_players
def bref_get_players():
    """
    Write local json file containing player info
    """
    save_all_players({"html_stat_getter":   bref_get_stat_url,
                      "url_counter": bref_url_counter,
                      "reformat_html": bref_reformat_html,
                      "player_json": "bref_players.json",
                      "table_loc": 1})

def bref_get_stat_url(player_type, page_no):
    """
    Construct http address of url that gets players.  Player type is
    "batting" or "pitching".  Page_no is not used
    """
    if not page_no:
        return ''
    return ''.join([
        "https://www.baseball-reference.com/leagues/majors/2022-standard-",
        player_type,
        ".shtml"
    ])
def bref_url_counter(player_type):
    """
    Extract only one table (value returned is upper bound of range call)
    """
    if not player_type:
        return 0
    return 2

def bref_reformat_html(htmldata):
    """
    Once an html file is extracted, remove all comments so that all tables
    can be parsed by pandas
    """
    return str(htmldata).replace("<!--", "").replace("--!>", "")

if __name__ == "__main__":
    bref_get_players()
