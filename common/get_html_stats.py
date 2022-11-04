#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE for details)
"""
Offseason data collector -- Common statistics

save_all_players -- collect and write player statistics
"""
import pandas as pd
from common.io_ops import read_stat_monad, write_json_monad

def save_all_players(packet):
    """
    Write a json file containing all the collected dict records

    packet is a dict whose entries contain are used as parameters in this
    module.  The fields are indexed by strings and contain numbers, strings,
    or function names.  The packet fields in use are:
        table_loc -- Integer representing the index of the table inside an
                     html file
        player_json -- String value of the file name for the json file created
        url_counter -- Function that calculates the maximum index number
                       for each web page type.
        reformat_html -- Function that acts as a filter to change html text
                         before processing
        html_stats_getter -- Function that is used to generate the exact
                             URL for each web page
    """
    write_json_monad(packet['player_json'], get_all_players(packet))

def get_all_players(packet):
    """
    Take all the table pandas records and convert them to dict entries
    """
    return list(map(convert_dataframe, merge_all_tables(packet)))

def convert_dataframe(info):
    """
    Convert one pandas table into a list of dict entries
    """
    return info.to_dict('records')

def merge_all_tables(packet):
    """
    Concatenate all the table records together (useful when more than one web
    page is found)
    """
    return list(map(pd.concat, get_all_tables(packet)))

def get_all_tables(packet):
    """
    Collect the stats from the html files, and read the appropriate table
    (indexed by the packet's table_loc value).
    """
    return list(map(ptype_level(packet), get_all_html_stats(packet)))

def get_all_html_stats(packet):
    """
    Set up stat collection for both batting and pitching tables
    """
    return list(map(get_html_stats(packet), ['batting', 'pitching']))

def get_html_stats(packet):
    """
    Group read operations so that all pages get read
    """
    def read_html_stats(plyr_type):
        return list(map(get_raw_html_data(packet)(plyr_type),
               list(range(1, packet['url_counter'](plyr_type)))))
    return read_html_stats

def get_raw_html_data(packet):
    """
    Perform the actual read of the data from the website
    """
    def get_raw_request(plyr_type):
        def get_request_data(counter):
            return packet['reformat_html'](read_stat_monad
                    (packet['html_stat_getter'](plyr_type, counter)))
        return get_request_data
    return get_raw_request

def ptype_level(packet):
    """
    Wrap the collection of a single pandas table (needed because this is
    called from a map function)
    """
    def ptype_level_inner(one_table):
        return list(map(get_dataframe(packet), one_table))
    return ptype_level_inner

def get_dataframe(packet):
    """
    Read the correct table location (index of table numbers on the page)
    and create a pandas representation
    """
    def get_dataframe_inner(one_table):
        return pd.read_html(one_table)[packet["table_loc"]]
    return get_dataframe_inner
