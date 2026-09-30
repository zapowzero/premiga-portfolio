"""
Which road features are linked to high-impact accidents?
Compares road-feature shares for high-impact (Severity 3-4) vs low-impact (Severity 1-2)
accidents in the US Accidents dataset (March 2023).

Note: in this dataset, Severity measures impact on traffic (length of delay),
not injury severity.

Dataset: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
Put US_Accidents_March23.csv in the data/ folder, or pass its path when running:
    python "<this script>.py" "path/to/US_Accidents_March23.csv"
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
OUTPUT_PATH = HERE / "comparison of severe vs minor accidents by road feature.png"

ROAD_FEATURES = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                 'Traffic_Signal', 'Turning_Loop']

df = pd.read_csv(DATA_PATH, usecols=['Severity'] + ROAD_FEATURES)

severe = df[df['Severity'].isin([3, 4])]
minor = df[df['Severity'].isin([1, 2])]
print(f"High-impact accidents (3-4): {len(severe):,}")
print(f"Low-impact accidents (1-2):  {len(minor):,}")

severe_counts = severe[ROAD_FEATURES].sum()
minor_counts = minor[ROAD_FEATURES].sum()

comparison = pd.DataFrame({
    'Severe Accidents (%)': severe_counts / severe_counts.sum() * 100,
    'Minor Accidents (%)': minor_counts / minor_counts.sum() * 100,
})
# Positive = feature is over-represented among high-impact accidents
comparison['Difference (pp)'] = comparison['Severe Accidents (%)'] - comparison['Minor Accidents (%)']
comparison = comparison.sort_values('Severe Accidents (%)', ascending=True)

# Chart
fig, ax = plt.subplots(figsize=(16, 10))
bar_width = 0.35
index = np.arange(len(comparison))

bars_severe = ax.barh(index - bar_width / 2, comparison['Severe Accidents (%)'],
                      height=bar_width, color='#8B0000', alpha=0.8,
                      label='High impact (Severity 3-4)')
bars_minor = ax.barh(index + bar_width / 2, comparison['Minor Accidents (%)'],
                     height=bar_width, color='#000066', alpha=0.8,
                     label='Low impact (Severity 1-2)')

for bar in list(bars_severe) + list(bars_minor):
    width = bar.get_width()
    ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f'{width:.1f}%',
            ha='left', va='center', fontweight='bold')

ax.set_yticks(index)
ax.set_yticklabels(comparison.index)
ax.set_xlabel("Share of road-feature flags (%)", fontsize=12, fontweight='bold')
ax.set_ylabel("Road Feature", fontsize=12, fontweight='bold')
ax.set_title("Comparison of Severe vs. Minor Accidents by Road Feature (%)",
             fontsize=14, fontweight='bold')
ax.legend(title='Accident Severity', loc='lower right')
ax.set_xlim(0, comparison[['Severe Accidents (%)', 'Minor Accidents (%)']].max().max() + 5)
ax.grid(axis='x', linestyle='--', alpha=0.7)
fig.tight_layout()
fig.savefig(OUTPUT_PATH, dpi=150)
plt.show()

print("\nRoad Feature Severity Comparison (sorted by difference):")
print(comparison.sort_values('Difference (pp)', ascending=False).round(1))