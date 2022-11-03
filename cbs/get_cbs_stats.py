from bs4 import BeautifulSoup
from common.io_ops import read_stat_monad
from common.get_html_stats import save_all_players

def get_players():
    save_all_players({"html_stat_getter":  cbs_get_stat_url,
                      "url_counter": cbs_url_counter,
                      "reformat_html": cbs_reformat_html,
                      "player_json": "cbs_players.json",
                      "table_loc": 0})

def cbs_get_stat_url(player_type, page_no):
    return ''.join([
        "https://www.cbssports.com/mlb/stats/player/",
        player_type,
        "/mlb/regular/all-pos/all/?page=",
        str(page_no)
    ])
def cbs_reformat_html(htmldata):
    return str(htmldata)
def cbs_url_counter(player_type):
    return get_set_of_urls(cbs_get_stat_url(player_type, ''), 1)
def get_set_of_urls(url_pattern, page_no):
    if has_no_table(f'{url_pattern}{page_no}'):
        return page_no
    return get_set_of_urls(url_pattern, page_no + 1)
def has_no_table(url_name):
    if ''.join(BeautifulSoup(read_stat_monad(url_name),
            "html.parser").findAll(text=True)).find('Sorry, no results') > 0:
        return True
    return False
if __name__ == "__main__":
    get_players()
