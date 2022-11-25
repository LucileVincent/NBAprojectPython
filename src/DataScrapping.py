from time import sleep

import pandas as pd
from threading import Thread
from src.Functions.functions import *

# get data of players from the website
url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division" \
      "=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base" \
      "&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience" \
      "=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Regular " \
      "Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight= "

players = get_data(url, True)

df = pd.DataFrame(players['resultSets'][0]['rowSet'], columns=players['resultSets'][0]['headers'])

playerPos = []

for pos in ["pg", "sg", "sf", "pf", "c"]:
    url = "http://www.espn.com/nba/players/_/position/" + pos

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    doc = BeautifulSoup(response.text, 'html.parser')
    rows = doc.find_all('tr', {'class': 'evenrow'})

    for r in rows:
        player = r.find_all('a')[0].text.split(",")
        playerPos.append((player[1].replace(" ", "") + " " + player[0], pos.upper()))
    rows = doc.find_all('tr', {'class': 'oddrow'})

    for r in rows:
        player = r.find_all('a')[0].text.split(",")
        playerPos.append((player[1].replace(" ", "") + " " + player[0], pos.upper()))

df = pd.DataFrame(players['resultSets'][0]['rowSet'], columns=players['resultSets'][0]['headers'])
test = pd.DataFrame(playerPos, columns=['PLAYER_NAME', 'POSITION'])
test = test.sort_values(by=['PLAYER_NAME']).drop_duplicates(subset=['PLAYER_NAME'], keep='first')
df = df.merge(test, on="PLAYER_NAME", how="left")
df.to_csv('Data/NBA_Players_Stats.csv', index=False)

# get data of teams from the website

url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment" \
      "=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
      "&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23" \
      "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference" \
      "=&VsDivision="

teams = get_data(url, True)

df = pd.DataFrame(teams['resultSets'][0]['rowSet'], columns=teams['resultSets'][0]['headers'])

df.to_csv('Data/NBA_Teams_Stats.csv', index=False)

# get data of all the matches from the beginning of the season


url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_13.json"

Matches = get_data(url, True)

matchesData = []

threads = []

for m in Matches['leagueSchedule']["gameDates"]:
    for match in m['games']:
        if match['gameStatus'] > 1:
            threads.append(Thread(target=get_match_data, args=(match, matchesData)))

for t in threads:
    t.start()
    sleep(0.1)

for t in threads:
    t.join()


with open('Data/NBA_Matches_Stats.json', 'w') as outfile:
    json.dump(matchesData, outfile)


