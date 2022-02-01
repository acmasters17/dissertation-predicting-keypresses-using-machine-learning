import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import INPUT_CSV_FILENAME


# I want to see what the data looks like
# I cant visualise 20 d features but can try two for now just to see what it looks like
# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/' + INPUT_CSV_FILENAME)

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values
# y = np.concatenate([y, y])

# 46 classes currently
numClasses = len(np.unique(y))
print("Unique Classes - " + str(numClasses))
# Generate this many colors
colors = ["#808080", "#2f4f4f", "#556b2f", "#8b4513", "#6b8e23", "#2e8b57", "#006400", "#8b0000", "#483d8b", "#b8860b", "#bdb76b", "#008b8b", "#4682b4", "#d2691e", "#9acd32", "#cd5c5c", "#00008b", "#32cd32", "#7f007f", "#8fbc8f", "#b03060", "#ff0000", "#ffa500",
          "#ffd700", "#0000cd", "#00ff00", "#8a2be2", "#00ff7f", "#dc143c", "#00ffff", "#00bfff", "#adff2f", "#ff6347", "#b0c4de", "#ff00ff", "#6495ed", "#dda0dd", "#90ee90", "#ff1493", "#7b68ee", "#ffa07a", "#f5deb3", "#afeeee", "#ee82ee", "#7fffd4", "#ffb6c1"]

counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print(len(counts))


# For every point find colour and marker and plot it?
for i in range(1, 2000):
    currentLabel = y[i]
    searchResult = np.where(np.unique(y) == currentLabel)
    colorIndex = searchResult[0][0]
    counts[colorIndex] = counts[colorIndex] + 1
    plt.plot(X[i, 1], X[i, 7], marker="x", color=colors[colorIndex],
             markersize=2, linewidth=4,
             markerfacecolor=colors[colorIndex],
             markeredgecolor=colors[colorIndex],
             markeredgewidth=2, label=currentLabel)


for x in range(0, len(counts)):
    print(np.unique(y)[x], " : ", counts[x])

# plot x1 against x2
plt.xlabel('X1')
plt.ylabel('X2')
plt.show()