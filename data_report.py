import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from matplotlib.path import Path

# load json
with open('NBA_Matches_Stats.json') as f:
    data = json.load(f)

points = []
df = pd.DataFrame()
for d in data:
    for action in d["playByPlay"]["actions"]:
        if "Shot" in action['actionType']:
            if action["playerNameI"] == "S. Curry":
                df = pd.concat([df, pd.DataFrame(action, index=[0])], ignore_index=True)

df = df.rename(columns={"actionType": "Shot Type"})

# add image in the background

# change palette


fig, ax = plt.subplots(figsize=(12, 11))
img = plt.imread("court.png")
ax.imshow(img, extent=[-270, 270, -67.5, 442.5])

img2 = plt.imread("court-bottom-left.png")
for i in img2:
    for j in i:
        if j[3] != 0:
            #check for average

            j[1] = j[2] = 0
ax.imshow(img2, extent=[-270, 270, -67.5, 442.5])



plt.xlim(-250, 250)
plt.ylim(-47.5, 422.5)

plt.show()

# create a graph with polygons for the court
