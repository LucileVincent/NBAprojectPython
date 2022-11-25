
from src.Functions.functions import *

# load json
with open('Data/NBA_Matches_Stats.json') as f:
    data = json.load(f)

points = []
df = pd.DataFrame()

for d in data:
    for action in d["playByPlay"]["actions"]:
        if "Shot" in action['actionType']:
            if action["playerNameI"] == "S. Curry":
                df = pd.concat([df, pd.DataFrame(action, index=[0])], ignore_index=True)

df = df.rename(columns={"actionType": "Shot Type"})

# add if the shot is a 3 pointer or not
df["zone"] = df.apply(lambda r: get_zone_(r), axis=1)

images = [(plt.imread("court-top.png")), plt.imread("court-2points.png"),
          plt.imread("court-bottom-left.png"), plt.imread("court-inside.png"),
          plt.imread("court-hoop.png"), plt.imread("court-bottom-right.png")]

# check the accuracy of each zones
zones = df.groupby(["zone", "Shot Type"]).agg({"Shot Type": "count"})

percent = zones["Shot Type"].unstack()["Made Shot"] / (
        zones["Shot Type"].unstack()["Missed Shot"] + zones["Shot Type"].unstack()["Made Shot"])

with open('Data/LeagueAverage.json') as f:
    league_avg = json.load(f)

league_avg = clean_league_avg(league_avg)

fig, ax = plt.subplots(figsize=(10, 10))
img = plt.imread("court.png")
ax.imshow(img, extent=[-270, 270, -67.5, 442.5])

for id in range(len(images)):
    try:
        for i in images[id]:
            for j in i:
                if j[3] != 0:
                    if (float(percent[id])) > (float(league_avg[percent.index.values[id]])):
                        j[0] = j[2] = 0
                    else:
                        j[2] = j[1] = 0

        ax.imshow(images[id], extent=[-270, 270, -67.5, 442.5])

    except:
        pass

add_text(ax, zones, league_avg, percent)

ax.legend('PA = Player Average\nLA = League Average', loc="upper left", bbox_to_anchor=(1, 1))
plt.xlim(-250, 250)
plt.ylim(-47.5, 422.5)

plt.show()

# create a graph with polygons for the court
