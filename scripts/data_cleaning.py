
import pandas as pd
from pathlib import Path

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the raw dataset
df = pd.read_csv(
    DATA_DIR / "synthetic_raw.csv",
    parse_dates=["ICDT", "VISDT"]
)

# Preserve the original data for review
raw_df = df.copy(deep=True)

issues = []


def add_issue(row_index, check_id, variable, observed_value,
              description, query):
    issues.append({
        "SUBJID": raw_df.loc[row_index, "SUBJID"],
        "CHECK_ID": check_id,
        "VARIABLE": variable,
        "OBSERVED_VALUE": str(observed_value),
        "ISSUE_DESCRIPTION": description,
        "DRAFT_SITE_QUERY": query
    })


# EC01: Missing Subject ID
mask = (
    raw_df["SUBJID"].isna()
    | raw_df["SUBJID"].astype("string").str.strip().eq("")
)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC01", "SUBJID", raw_df.loc[i, "SUBJID"],
        "Subject ID is missing",
        "Please confirm and provide the correct subject identifier."
    )


# EC02: Duplicate Subject ID
mask = (
    raw_df["SUBJID"].notna()
    & raw_df["SUBJID"].duplicated(keep=False)
)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC02", "SUBJID", raw_df.loc[i, "SUBJID"],
        "Subject ID is duplicated",
        "Please verify the identifier and confirm whether this record is a duplicate."
    )


# EC03: Missing consent date
for i in raw_df.index[raw_df["ICDT"].isna()]:
    add_issue(
        i, "EC03", "ICDT", raw_df.loc[i, "ICDT"],
        "Consent date is missing",
        "Please verify the informed consent date against source documentation."
    )


# EC04: Missing visit date
for i in raw_df.index[raw_df["VISDT"].isna()]:
    add_issue(
        i, "EC04", "VISDT", raw_df.loc[i, "VISDT"],
        "Visit date is missing",
        "Please verify the visit date against source documentation."
    )


# EC05: Visit date before consent date
mask = (
    raw_df["ICDT"].notna()
    & raw_df["VISDT"].notna()
    & (raw_df["VISDT"] < raw_df["ICDT"])
)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC05", "VISDT", raw_df.loc[i, "VISDT"],
        "Visit date precedes consent date",
        "Please confirm both dates and clarify the chronology."
    )


# EC06: Missing or out-of-range age
age = pd.to_numeric(raw_df["AGE"], errors="coerce")
mask = age.isna() | ~age.between(18, 75)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC06", "AGE", raw_df.loc[i, "AGE"],
        "Age is missing, invalid, or outside 18-75 years",
        "Please verify the recorded age and confirm the correct value."
    )


# EC07: Non-standard sex coding
sex = raw_df["SEX"].astype("string").str.strip()
mask = sex.isna() | ~sex.isin(["M", "F"])
for i in raw_df.index[mask]:
    add_issue(
        i, "EC07", "SEX", raw_df.loc[i, "SEX"],
        "Sex coding is missing or non-standard",
        "Please confirm the intended coding using the study data conventions."
    )


# EC08: Missing or out-of-range height
height = pd.to_numeric(raw_df["HT"], errors="coerce")
mask = height.isna() | ~height.between(140, 200)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC08", "HT", raw_df.loc[i, "HT"],
        "Height is missing, invalid, or outside 140-200 cm",
        "Please verify the height and confirm the unit is centimetres."
    )


# EC09: Missing or out-of-range weight
weight = pd.to_numeric(raw_df["WT"], errors="coerce")
mask = weight.isna() | ~weight.between(40, 150)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC09", "WT", raw_df.loc[i, "WT"],
        "Weight is missing, invalid, or outside 40-150 kg",
        "Please verify the weight and confirm the unit is kilograms before conversion."
    )


# EC10: Missing or out-of-range systolic blood pressure
sbp = pd.to_numeric(raw_df["SBP"], errors="coerce")
mask = sbp.isna() | ~sbp.between(80, 200)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC10", "SBP", raw_df.loc[i, "SBP"],
        "Systolic blood pressure is missing, invalid, or outside 80-200 mmHg",
        "Please verify the systolic blood pressure against the source record."
    )


# EC11: Missing or invalid diastolic blood pressure
dbp = pd.to_numeric(raw_df["DBP"], errors="coerce")
mask = (
    dbp.isna()
    | ~dbp.between(50, 120)
    | (sbp.notna() & dbp.notna() & (dbp >= sbp))
)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC11", "DBP", raw_df.loc[i, "DBP"],
        "Diastolic BP is missing, outside 50-120 mmHg, or not below SBP",
        "Please verify both blood pressure values and confirm the measurements."
    )


# EC12: Missing or out-of-range haemoglobin
hgb = pd.to_numeric(raw_df["HGB"], errors="coerce")
mask = hgb.isna() | ~hgb.between(8, 18)
for i in raw_df.index[mask]:
    add_issue(
        i, "EC12", "HGB", raw_df.loc[i, "HGB"],
        "Haemoglobin is missing, invalid, or outside 8-18 g/dL",
        "Please verify the haemoglobin result and confirm the unit is g/dL."
    )


# Create and save the discrepancy log
columns = [
    "SUBJID", "CHECK_ID", "VARIABLE",
    "OBSERVED_VALUE", "ISSUE_DESCRIPTION", "DRAFT_SITE_QUERY"
]
discrepancy_df = pd.DataFrame(issues, columns=columns)

discrepancy_df.to_csv(
    OUTPUT_DIR / "discrepancy_log.csv", index=False
)

# Create and save the summary
summary_df = (
    discrepancy_df.groupby("CHECK_ID")
    .size()
    .reset_index(name="DISCREPANCY_COUNT")
    .sort_values("CHECK_ID")
)

summary_df.to_csv(
    OUTPUT_DIR / "edit_check_summary.csv", index=False
)

# Print results
print("DATA CLEANING WORKFLOW COMPLETED")
print("Total records:", len(raw_df))
print("Total variables:", len(raw_df.columns))
print("Discrepancy records:", len(discrepancy_df))
print("Unique subjects affected:", discrepancy_df["SUBJID"].nunique())
print("\nSummary by edit check:")
print(summary_df.to_string(index=False))
print("\nOutput files saved in:", OUTPUT_DIR)
