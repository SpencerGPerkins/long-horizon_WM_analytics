from pyalex import Works
import pandas as pd
from tqdm import tqdm

# Configuration
SEARCH_TERMS = [
    "robotic world models",
    "long horizon robot manipulation planning",
    "robot manipulation planning",
    "JEPA world models robotic manipulation",
    "latent dynamics robot manipulation planning",
]

START_YEAR = 2021
RESULTS_PER_QUERY = 50
# Helper: reconstruct abstract
def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return None

    words = []

    for word, positions in inverted_index.items():
        for pos in positions:
            words.append((pos, word))

    words.sort()

    return " ".join(
        [word for _, word in words]
    )

# Collect papers
papers = {}
for term in SEARCH_TERMS:
    print(f"\nSearching: {term}")
    results = (
        Works()
        .search(term)
        .filter(
            publication_year=f">{START_YEAR-1}"
        )
        .get(
            per_page=RESULTS_PER_QUERY
        )
    )

    for paper in tqdm(results):
        pid = paper["id"]
        if pid in papers:
            continue
        # Venue
        venue = None
        if paper.get("primary_location"):
            source = paper["primary_location"].get("source")

            if source:
                venue = source.get("display_name")
        # Abstract
        abstract = reconstruct_abstract(
            paper.get(
                "abstract_inverted_index"
            )
        )
        # Open access
        oa = paper.get(
            "open_access",
            {}
        )
        papers[pid] = {

            "openalex_id": pid,

            "title": paper.get(
                "display_name"
            ),

            "year": paper.get(
                "publication_year"
            ),

            "venue": venue,

            "doi": paper.get(
                "doi"
            ),

            "citations": paper.get(
                "cited_by_count"
            ),

            "abstract": abstract,

            "is_open_access": oa.get(
                "is_oa"
            ),

            "openalex_oa_url": oa.get(
                "oa_url"
            ),

            "type": paper.get(
                "type"
            )
        }
# Save
df = pd.DataFrame(
    papers.values()
)
df = df.sort_values(
    [
        "year",
        "citations"
    ],
    ascending=[
        False,
        False
    ]
)

df.to_csv(
    "papers_openalex.csv",
    index=False
)
print(
    f"\nCollected {len(df)} papers"
)
print(
    df[
        [
            "title",
            "year",
            "citations"
        ]
    ].head(10)
)