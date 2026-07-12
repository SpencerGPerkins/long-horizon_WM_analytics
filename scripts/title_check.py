import pandas as pd

df = pd.read_csv("papers_filtered.csv")
for i, title in enumerate(df["title"]):
    print(i, title)