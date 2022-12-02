from time import sleep
import pandas as pd
from threading import Thread
from nba.api import *

# get data of players from the website
url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division" \
      "=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base" \
      "&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience" \
      "=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Regular " \
      "Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight= "

players = get_data(url, True)

df = pd.DataFrame(players['resultSets'][0]['rowSet'], columns=players['resultSets'][0]['headers'])

player_pos = []

url = "https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division" \
      "=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0" \
      "&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=2022-23" \
      "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision" \
      "=&Weight= "

players = get_data(url, True)

df2 = pd.DataFrame(players['resultSets'][0]['rowSet'], columns=players['resultSets'][0]['headers'])
df = df.merge(df2[["PLAYER_ID",'PLAYER_HEIGHT_INCHES',"PLAYER_WEIGHT"]], on='PLAYER_ID', how='left')


# get the position of each player
for pos in ["pg", "sg", "sf", "pf", "c"]:
    url = "http://www.espn.com/nba/players/_/position/" + pos

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    doc = BeautifulSoup(response.text, 'html.parser')
    rows = doc.find_all('tr', {'class': 'evenrow'})

    for r in rows:
        player = r.find_all('a')[0].text.split(",")
        player_pos.append((player[1].replace(" ", "") + " " + player[0], pos.upper()))
    rows = doc.find_all('tr', {'class': 'oddrow'})

    for r in rows:
        player = r.find_all('a')[0].text.split(",")
        player_pos.append((player[1].replace(" ", "") + " " + player[0], pos.upper()))



# create the dataframe of positions
df_position = pd.DataFrame(player_pos, columns=['PLAYER_NAME', 'POSITION'])
df_position = df_position.sort_values(by=['PLAYER_NAME']).drop_duplicates(subset=['PLAYER_NAME'], keep='first')

# merge the two dataframes to add the position of each player
df = df.merge(df_position, on="PLAYER_NAME", how="left")

# save the dataframe to a csv file
df.to_csv('Data/NBA_Players_Stats.csv', index=False)

# get data of teams from the website
url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment" \
      "=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
      "&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23" \
      "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference" \
      "=&VsDivision="

teams = get_data(url, True)

df = pd.DataFrame(teams['resultSets'][0]['rowSet'], columns=teams['resultSets'][0]['headers'])

url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment" \
      "=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
      "&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23" \
      "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference" \
      "=&VsDivision="

teams2 = get_data(url, True)
df =df.merge(pd.DataFrame(teams2['resultSets'][0]['rowSet'], columns=teams2['resultSets'][0]['headers']), on="TEAM_ID",how="left")
# save the dataframe to a csv file
df.to_csv('Data/NBA_Teams_Stats.csv', index=False)

# get the match list

url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_13.json"

Matches = get_data(url, True)

matchesData = []

threads = []

# get the data of each match
# we use threading to speed up the process and not wait for each request to finish
for m in Matches['leagueSchedule']["gameDates"]:
    for match in m['games']:
        if match['gameStatus'] > 1:
            threads.append(Thread(target=get_match_data, args=(match, matchesData)))

# start all threads
for t in threads:
    t.start()
    sleep(0.1)

# wait for all threads to finish
for t in threads:
    t.join()

# write the data to a json file
# it can take a while to write all the data (100mb of data)
with open('Data/NBA_Matches_Stats.json', 'w') as outfile:
    json.dump(matchesData, outfile)
