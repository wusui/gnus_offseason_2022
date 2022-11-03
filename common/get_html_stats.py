import pandas as pd
from common.io_ops import read_stat_monad, write_players_monad

def save_all_players(packet):
    write_players_monad(packet['player_json'], get_all_players(packet))
def get_all_players(packet):
    return list(map(convert_dataframe, merge_all_tables(packet)))
def convert_dataframe(info):
    return info.to_dict('records')
def merge_all_tables(packet):
    return list(map(pd.concat, get_all_tables(packet)))
def get_all_tables(packet):
    return list(map(ptype_level(packet), get_all_html_stats(packet)))
def get_all_html_stats(packet):
    return list(map(get_html_stats(packet), ['batting', 'pitching']))
def get_html_stats(packet):
    def read_html_stats(plyr_type):
        return list(map(get_raw_html_data(packet)(plyr_type),
               list(range(1, packet['url_counter'](plyr_type)))))
    return read_html_stats
def get_raw_html_data(packet):
    def get_raw_request(plyr_type):
        def get_request_data(counter):
            return packet['reformat_html'](read_stat_monad
                    (packet['html_stat_getter'](plyr_type, counter)))
        return get_request_data
    return get_raw_request
def ptype_level(packet):
    def ptype_level_inner(one_table):
        return list(map(get_dataframe(packet), one_table))
    return ptype_level_inner
def get_dataframe(packet):
    def get_dataframe_inner(one_table):
        return pd.read_html(one_table)[packet["table_loc"]]
    return get_dataframe_inner
