import pandas as pd

df = pd.read_csv("papers_with_pdf.csv")

print(df[["title", "pdf_url"]].head(10))