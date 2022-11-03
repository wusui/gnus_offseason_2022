import json
import requests
def read_stat_monad(url_page):
    return requests.get(url_page).text
def write_players_monad(file_name, out_dict):
    with open(file_name, "w", encoding="utf8") as ofd:
        json.dump(out_dict, ofd)
