from common.get_html_stats import save_all_players
def get_players():
    save_all_players({"html_stat_getter":   bref_get_stat_url,
                      "url_counter": bref_url_counter,
                      "reformat_html": bref_reformat_html,
                      "player_json": "bref_players.json",
                      "table_loc": 1})

def bref_get_stat_url(player_type, page_no):
    if not page_no:
        return ''
    return ''.join([
        "https://www.baseball-reference.com/leagues/majors/2022-standard-",
        player_type,
        ".shtml"
    ])
def bref_url_counter(player_type):
    if not player_type:
        return 0
    return 2
def bref_reformat_html(htmldata):
    return str(htmldata).replace("<!--", "").replace("--!>", "")

if __name__ == "__main__":
    get_players()
