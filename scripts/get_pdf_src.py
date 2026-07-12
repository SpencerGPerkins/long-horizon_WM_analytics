import pandas as pd
import requests
import re
from tqdm import tqdm


INPUT_FILE = "papers_openalex.csv"
OUTPUT_FILE = "papers_with_pdf.csv"

# Extract arXiv ID
def find_arxiv_id(text):

    if not text:
        return None

    match = re.search(
        r"(?:arxiv\.org/abs/|arXiv:)(\d+\.\d+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None

# Query Unpaywall
def get_unpaywall_pdf(doi):

    if not doi:
        return None

    url = (
        f"https://api.unpaywall.org/v2/"
        f"{doi}"
        f"?email=your_email@example.com"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()


        best = data.get(
            "best_oa_location"
        )

        if best:

            return (
                best
                .get("url_for_pdf")
            )

    except Exception:

        return None

# arXiv PDF lookup
def get_arxiv_pdf(arxiv_id):

    if not arxiv_id:
        return None

    return (
        f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    )

# Main
df = pd.read_csv(INPUT_FILE)
pdf_urls = []
sources = []

for _, row in tqdm(
    df.iterrows(),
    total=len(df)
):
    pdf = None
    source = None
    # OpenAlex OA URL

    if (
        pd.notna(
            row.get(
                "openalex_oa_url"
            )
        )
    ):

        pdf = row["openalex_oa_url"]
        source = "openalex"

    # Unpaywall
    if pdf is None:

        pdf = get_unpaywall_pdf(
            row.get("doi")
        )

        if pdf:
            source = "unpaywall"

    # arXiv
    if pdf is None:

        arxiv_id = find_arxiv_id(
            str(row["title"])
            + " "
            + str(row.get("doi"))
        )
        pdf = get_arxiv_pdf(
            arxiv_id
        )
        if pdf:
            source = "arxiv"
    pdf_urls.append(pdf)
    sources.append(source)
df["pdf_url"] = pdf_urls
df["pdf_source"] = sources
df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Finished PDF source discovery"
)
print(
    df["pdf_source"].value_counts()
)