import pandas as pd
import seaborn as sns
from src.Functions.functions import *

df = pd.read_csv("Data/NBA_Players_Stats.csv")
df = df[df["MIN"] != 0]

teams = pd.read_csv("Data/NBA_Teams_Stats.csv")

df = df.merge(teams[["AST", "FGM","PACE","TEAM_ID"]], on="TEAM_ID", how="left", suffixes=("", "_TEAM"))

df = df[df["MIN"] >30]

# calculate player efficiency rating


factor = 2 / 3 - (0.5 * (df["AST"].mean() / df["FGM"].mean())) / (2 * df["FGM"].mean() / df["FTM"].mean())
VOP = df["PTS"].mean() / ( df["FGA"].mean()- df["OREB"].mean() + df["TOV"].mean() + 0.44 * df["FTA"].mean() )
DRBP = df["REB"].mean() - df["OREB"].mean() / (df["REB"].mean())
uPER = 1 / (df["MIN"]) * (df["FG3M"] + (df["AST"] * 2 / 3) + ((2 - factor * df["AST_TEAM"] / df["FGM_TEAM"])
        * df["FGM"]) + (0.5 * df["FTM"] * (2-1/3 * df["AST_TEAM"] / df["FGM_TEAM"]))-VOP *(DRBP *(2*df["OREB"]+ df["BLK"]
        - 0.2464 *(df["FTA"]-df["FTM"])-(df["FGA"]-df["FGM"])- df["REB"]) + (0.44 * df["FTA"].mean()*df["PFD"])/df["PFD"].mean()
        -(df["TOV"]-df["OREB"])-df["STL"] + df["REB"]-1.936*(df["FTA"]-df["FTM"])) + df["PFD"]*df["FTM"].mean()/df["PFD"].mean())

df["PER"] = (uPER * df["PACE"].mean()/ df["PACE"])* 15/uPER.mean()


print(df["PER"].max())
print(df["PER"].min())

df = df.sort_values(by="PER", ascending=False)
print(df.head(10))

df = df.sort_values(by="PER", ascending=True)
print(df.head(10))

# plot the distribution of PER

plt.hist(df["PER"], bins=100)
plt.show()

# plot the distribution of PER for the top 10 players

sns.histplot(df["PER"], bins=20, kde=True)
plt.show()
