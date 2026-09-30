"""
Where do US road accidents happen?
Share of road-feature flags among recorded accidents (US Accidents, March 2023).

Dataset: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
Put US_Accidents_March23.csv in the data/ folder, or pass its path when running:
    python "<this script>.py" "path/to/US_Accidents_March23.csv"
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CSV_NAME = "US_Accidents_March23.csv"
HERE = Path(__file__).resolve().parent
# Places to look for the CSV, in order (first match wins)
CANDIDATES = [
    HERE / "data" / CSV_NAME,             # zapow dataviz/data/
    HERE.parent.parent / "datasets" / CSV_NAME,  # Desktop/datasets/ (next to "projects portfolio")
]
if len(sys.argv) > 1:
    CANDIDATES.insert(0, Path(sys.argv[1]))
DATA_PATH = next((p for p in CANDIDATES if p.exists()), None)
if DATA_PATH is None:
    sys.exit("CSV not found. Looked in:\n  " + "\n  ".join(str(p) for p in CANDIDATES) +
             "\nPut the CSV in one of these places, or pass its path: python script.py path/to/" + CSV_NAME)
print(f"Using data: {DATA_PATH}")
OUTPUT_PATH = HERE / "percentage of accidents by road infrastructure.png"

ROAD_FEATURES = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                 'Traffic_Signal', 'Turning_Loop']

# Load only the columns we need (the full CSV is ~3 GB)
df = pd.read_csv(DATA_PATH, usecols=['Start_Time'] + ROAD_FEATURES)
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce', format='mixed')
df = df.dropna(subset=['Start_Time'])

print(f"Data covers {df['Start_Time'].min():%Y-%m-%d} to {df['Start_Time'].max():%Y-%m-%d}")
print(f"Accidents analysed: {len(df):,}")

# Note: one accident can carry several flags, and accidents with no flag are not counted.
# Percentages are shares of all feature flags, not accident rates.
flag_counts = df[ROAD_FEATURES].sum()
flagged_accidents = df[ROAD_FEATURES].any(axis=1).sum()
print(f"Accidents with at least one road feature: {flagged_accidents:,} "
      f"({flagged_accidents / len(df):.1%})")

result = pd.DataFrame({
    'Flag Count': flag_counts,
    'Share of Flags (%)': flag_counts / flag_counts.sum() * 100,
}).sort_values('Flag Count', ascending=False)

print("\n===== Summary of shares (%) =====")
print(result['Share of Flags (%)'].describe()[['mean', '50%', 'max', 'min']].round(2))
print("\n===== Detail =====")
print(result.round(2))

# Chart
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(result.index, result['Share of Flags (%)'], color='darkblue', height=0.6)
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f'{bar.get_width():.2f}%', va='center', fontsize=10)

ax.set_xlabel("Share of road-feature flags (%)", fontsize=12)
ax.set_ylabel("Road Feature", fontsize=12)
ax.set_title("Percentage of Accidents by Road Infrastructure Type", fontsize=14, fontweight='bold')
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.7)
fig.tight_layout()
fig.savefig(OUTPUT_PATH, dpi=150)
plt.show()