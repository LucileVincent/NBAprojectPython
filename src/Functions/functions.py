import pandas as pd
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests


def is_above_the_break(x, y):
    if y < 95:
        return False
    if x ** 2 + y ** 2 < 225 ** 2:
        return False

    return True


def is_in_paint(x, y):
    if abs(x) > 70:
        return False
    if y > 150:
        return False
    if x ** 2 + y ** 2 < 50 ** 2 and y > 0:
        return False

    return True


def is_right_corner(x, y):
    if x > 220 and y < 95:
        return True
    return False


def is_left_corner(x, y):
    if x < -220 and y < 95:
        return True
    return False


def is_resticted_area(x, y):
    if x ** 2 + y ** 2 <= 50 ** 2 and y > 0:
        return True
    return False


def get_zone_(row):
    x = row["xLegacy"]
    y = row["yLegacy"]

    if is_above_the_break(x, y):
        return "Above the Break 3"
    elif is_in_paint(x, y):
        return "In The Paint (Non-RA)"
    elif is_right_corner(x, y):
        return "Right Corner 3"
    elif is_left_corner(x, y):
        return "Left Corner 3"
    elif is_resticted_area(x, y):
        return "Restricted Area"
    else:
        return "Mid-Range"


def clean_league_avg(league_avg):
    data = league_avg["resultSets"][0]["rowSet"]
    df = pd.DataFrame(data, columns=league_avg["resultSets"][0]["headers"])

    df = df.groupby("SHOT_ZONE_BASIC").agg({"FGA": "sum", "FGM": "sum"})
    df.loc["Above the Break 3", "FGA"] += df.loc["Backcourt", "FGA"]
    df["FG%"] = df["FGM"] / df["FGA"]
    df.drop("Backcourt", inplace=True)

    return df.loc[:, "FG%"]


def add_text(ax, zone, league_avg, percent):
    points = [(-22, 250), (-22, 100), (-250, 0), (-22, 170), (-22, 0), (200, 0)]
    print(percent)
    zone = zone["Shot Type"].unstack()
    for i in range(len(zone)):
        text = "   " + str(int(zone["Made Shot"][i])) + "/" + str(
            int(zone["Missed Shot"][i]) + int(zone["Made Shot"][i]))
        text += '\nPA: ' + str(round(percent[i] * 100, 1)) + "%\n"
        text += "LA: {:.2f}%".format(float(league_avg[percent.index.values[i]]) * 100)
        ax.text(points[i][0], points[i][1], text, bbox=dict(facecolor='white', alpha=0.7))


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
