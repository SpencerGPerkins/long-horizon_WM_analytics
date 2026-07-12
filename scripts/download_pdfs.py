import os
import pandas as pd
import requests
from tqdm import tqdm

INPUT_FILE = "papers_with_pdf.csv"
PDF_FOLDER = "data/pdfs"

os.makedirs(
    PDF_FOLDER,
    exist_ok=True
)
# Filename helper
def clean_filename(name):

    invalid = [
        "/",
        "\\",
        ":",
        "*",
        "?",
        "\"",
        "<",
        ">",
        "|"
    ]

    for char in invalid:
        name = name.replace(
            char,
            "_"
        )
    return name[:120]

# Download
df = pd.read_csv(INPUT_FILE)
success = 0
for _, row in tqdm(
    df.iterrows(),
    total=len(df)
):
    url = row["pdf_url"]
    if pd.isna(url):
        continue
    filename = (
        clean_filename(
            row["title"]
        )
        +
        ".pdf"
    )
    filepath = os.path.join(
        PDF_FOLDER,
        filename
    )
    # Skip existing
    if os.path.exists(filepath):
        success += 1
        continue
    try:
        r = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )
        r.raise_for_status()
        # Check actually got PDF
        if (
            "application/pdf"
            not in r.headers.get(
                "Content-Type",
                ""
            )
        ):
            print(
                f"Not PDF: {row['title']}"
            )

            continue
        with open(
            filepath,
            "wb"
        ) as f:

            f.write(
                r.content
            )
        success += 1

    except Exception as e:
        print(
            f"\nFailed: {row['title']}"
        )

        print(e)

print(
    f"\nDownloaded {success} PDFs"
)