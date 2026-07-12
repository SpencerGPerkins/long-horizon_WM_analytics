import pandas as pd


INPUT = "papers_openalex.csv"
OUTPUT = "papers_filtered.csv"


df = pd.read_csv(INPUT)


# Terms that indicate robotics relevance
robot_terms = [
    "robot",
    "robotic",
    "manipulation",
    "embodied",
    "agent",
    "arm",
    "grasp",
    "dexterous",
    "sawyer",
    "franka",
    "simulator",
    "metaworld",
    "rlbench",
    "calvin"
]


# Terms that indicate planning/world model relevance
planning_terms = [
    "planning",
    "planner",
    "trajectory",
    "world model",
    "latent dynamics",
    "predictive model",
    "model-based",
    "decision making",
    "control",
    "policy"
]


def contains_terms(text, terms):

    if pd.isna(text):
        return False

    text = text.lower()

    return any(
        t in text
        for t in terms
    )

def relevance(row):

    text = (
        str(row["title"])
        + " "
        + str(row["abstract"])
    )

    return (
        contains_terms(text, robot_terms)
        and
        contains_terms(text, planning_terms)
    )
df["relevant"] = df.apply(
    relevance,
    axis=1
)
filtered = df[
    df["relevant"]
]
filtered.to_csv(
    OUTPUT,
    index=False
)
print(
    f"{len(filtered)} / {len(df)} papers retained"
)