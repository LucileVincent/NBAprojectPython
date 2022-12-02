import json
from bs4 import BeautifulSoup
import requests


def get_match_data(match, array):
    url = "https://www.nba.com/game/" + match["awayTeam"]["teamTricode"].lower() + "-vs-" + match["homeTeam"][
        "teamTricode"].lower() + "-" + str(match["gameId"])
    payload = {}
    headers = {
        'Referer': 'https://www.nba.com/',
        'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36 '
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_data = soup.find_all('script', {'id': '__NEXT_DATA__'})
    try:
        data = json.loads(match_data[0].text)
        new_data = {"game": data["props"]["pageProps"]["game"], "playByPlay": data["props"]["pageProps"]["playByPlay"],
                    "analytics": data["props"]["pageProps"]["analyticsObject"]}
        new_data["game"]["officials"] = None
        new_data["game"]["broadcasters"] = None
        new_data["game"]["homeTeamPlayers"] = None
        new_data["game"]["awayTeamPlayers"] = None
        array.append(new_data)
    # transform data into dictionary
    except:
        print("error on " + url)


def get_data(url, is_nba=False):
    payload = {}
    if is_nba:

        headers = {
            'Referer': 'https://www.nba.com/',
            'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.159 Safari/537.36 '
        }
    else:
        headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if is_nba:
        return dict(response.json())
    else:
        return response


