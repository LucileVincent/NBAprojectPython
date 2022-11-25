
from functions import *




# get data of players from the website
url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division" \
      "=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType" \
      "=Regular&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience" \
      "=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Regular " \
      "Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight= "

players = get_data(url)

df = pd.DataFrame(players['resultSets'][0]['rowSet'], columns=players['resultSets'][0]['headers'])

df.to_csv('NBA_Players_Stats.csv', index=False)

# get data of teams from the website

url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment" \
      "=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
      "&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Regular " \
      "Season&ShotClockRange=&TeamID=0&VsConference=&VsDivision= "

payload = {}
headers = {
    'Referer': 'https://www.nba.com/',
    'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36 '
}

response = requests.request("GET", url, headers=headers, data=payload)

Players = dict(response.json())

df = pd.DataFrame(Players['resultSets'][0]['rowSet'], columns=Players['resultSets'][0]['headers'])

df.to_csv('NBA_Teams_Stats.csv', index=False)

# get data of all the matches from the beginning of the season


url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_13.json"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

Matches = dict(response.json())

matchesData = []
threads = []

for m in Matches['leagueSchedule']["gameDates"]:
    for match in m['games']:
        if match['gameStatus'] > 1:
            get_data_from_matches(match, matchesData)

with open('NBA_Matches_Stats.json', 'w') as outfile:
    json.dump(matchesData, outfile)
